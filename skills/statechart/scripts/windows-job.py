#!/usr/bin/env python3
"""Run a suspended child in a kill-on-close Win32 Job Object.

stdin is a lifetime pipe owned by the caller, not the worker's input. EOF
terminates only this job. A killed supervisor closes the last job handle,
so descendants cannot outlive it. No filesystem cleanup is performed.
"""
import ctypes as c
from ctypes import wintypes as w
import msvcrt
import os
import shutil
import signal
import subprocess
import sys
import threading


class BasicLimits(c.Structure):
    _fields_ = [("PerProcessUserTimeLimit", c.c_int64), ("PerJobUserTimeLimit", c.c_int64),
                ("LimitFlags", w.DWORD), ("MinimumWorkingSetSize", c.c_size_t),
                ("MaximumWorkingSetSize", c.c_size_t), ("ActiveProcessLimit", w.DWORD),
                ("Affinity", c.c_size_t), ("PriorityClass", w.DWORD),
                ("SchedulingClass", w.DWORD)]


class IoCounters(c.Structure):
    _fields_ = [(name, c.c_uint64) for name in
                ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                 "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]


class ExtendedLimits(c.Structure):
    _fields_ = [("BasicLimitInformation", BasicLimits), ("IoInfo", IoCounters),
                ("ProcessMemoryLimit", c.c_size_t), ("JobMemoryLimit", c.c_size_t),
                ("PeakProcessMemoryUsed", c.c_size_t), ("PeakJobMemoryUsed", c.c_size_t)]


class StartupInfo(c.Structure):
    _fields_ = [("cb", w.DWORD), ("lpReserved", w.LPWSTR), ("lpDesktop", w.LPWSTR),
                ("lpTitle", w.LPWSTR)] + [(name, w.DWORD) for name in
                ("dwX", "dwY", "dwXSize", "dwYSize", "dwXCountChars", "dwYCountChars",
                 "dwFillAttribute", "dwFlags")] + [("wShowWindow", w.WORD),
                ("cbReserved2", w.WORD), ("lpReserved2", c.POINTER(c.c_byte)),
                ("hStdInput", w.HANDLE), ("hStdOutput", w.HANDLE), ("hStdError", w.HANDLE)]


class ProcessInfo(c.Structure):
    _fields_ = [("hProcess", w.HANDLE), ("hThread", w.HANDLE),
                ("dwProcessId", w.DWORD), ("dwThreadId", w.DWORD)]


def main():
    if len(sys.argv) < 2:
        raise ValueError("Usage: windows-job.py EXECUTABLE [ARGS...]")
    kernel = c.WinDLL("kernel32", use_last_error=True)
    signatures = {
        "CreateJobObjectW": ([c.c_void_p, w.LPCWSTR], w.HANDLE),
        "SetInformationJobObject": ([w.HANDLE, c.c_int, c.c_void_p, w.DWORD], w.BOOL),
        "CreateProcessW": ([w.LPCWSTR, w.LPWSTR, c.c_void_p, c.c_void_p, w.BOOL,
                            w.DWORD, c.c_void_p, w.LPCWSTR, c.POINTER(StartupInfo),
                            c.POINTER(ProcessInfo)], w.BOOL),
        "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
        "ResumeThread": ([w.HANDLE], w.DWORD),
        "TerminateProcess": ([w.HANDLE, w.UINT], w.BOOL),
        "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
        "WaitForSingleObject": ([w.HANDLE, w.DWORD], w.DWORD),
        "GetExitCodeProcess": ([w.HANDLE, c.POINTER(w.DWORD)], w.BOOL),
        "SetHandleInformation": ([w.HANDLE, w.DWORD, w.DWORD], w.BOOL),
        "CloseHandle": ([w.HANDLE], w.BOOL),
    }
    for name, (args, result) in signatures.items():
        function = getattr(kernel, name)
        function.argtypes, function.restype = args, result

    def checked(value):
        if not value:
            raise c.WinError(c.get_last_error())
        return value

    executable = shutil.which(sys.argv[1]) or sys.argv[1]
    if not executable.lower().endswith(".exe"):
        raise ValueError("Job executable must resolve to an .exe (use a real Node/Python executable)")
    job = checked(kernel.CreateJobObjectW(None, None))
    process = ProcessInfo()
    assigned = False
    try:
        limits = ExtendedLimits()
        limits.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        checked(kernel.SetInformationJobObject(job, 9, c.byref(limits), c.sizeof(limits)))
        startup = StartupInfo()
        startup.cb, startup.dwFlags = c.sizeof(startup), 0x100  # STARTF_USESTDHANDLES
        with open(os.devnull, "rb") as null:
            startup.hStdInput = msvcrt.get_osfhandle(null.fileno())
            startup.hStdOutput = msvcrt.get_osfhandle(sys.stdout.fileno())
            startup.hStdError = msvcrt.get_osfhandle(sys.stderr.fileno())
            for handle in (startup.hStdInput, startup.hStdOutput, startup.hStdError):
                checked(kernel.SetHandleInformation(handle, 1, 1))
            command = c.create_unicode_buffer(subprocess.list2cmdline([executable, *sys.argv[2:]]))
            checked(kernel.CreateProcessW(executable, command, None, None, True,
                                          0x4 | 0x200, None, None,
                                          c.byref(startup), c.byref(process)))
        checked(kernel.AssignProcessToJobObject(job, process.hProcess))
        assigned = True
        if kernel.ResumeThread(process.hThread) == 0xFFFFFFFF:
            raise c.WinError(c.get_last_error())
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, signal.SIG_IGN)
        # Only the main thread closes the job; the watcher cannot race handle reuse.
        cancelled = threading.Event()
        def watch():
            try:
                while sys.stdin.buffer.read(1):
                    pass
            finally:
                cancelled.set()
        threading.Thread(target=watch, daemon=True).start()
        while kernel.WaitForSingleObject(process.hProcess, 50) == 258:
            if cancelled.is_set():
                checked(kernel.TerminateJobObject(job, 2))
                checked(kernel.WaitForSingleObject(process.hProcess, 5000) == 0)
                return 2
        code = w.DWORD()
        checked(kernel.GetExitCodeProcess(process.hProcess, c.byref(code)))
        return code.value if code.value < 256 else 2
    finally:
        if process.hProcess and not assigned:
            kernel.TerminateProcess(process.hProcess, 2)
        kernel.CloseHandle(job)
        for handle in (process.hThread, process.hProcess):
            if handle:
                kernel.CloseHandle(handle)


if __name__ == "__main__":
    try:
        result = main()
    except Exception as error:
        print(f"Windows job failed: {error}", file=sys.stderr, flush=True)
        result = 2
    # Avoid joining a daemon reader blocked in buffered stdin at interpreter shutdown.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(result)
