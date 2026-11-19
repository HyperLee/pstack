#!/usr/bin/env python3
"""Invoke TLC through JNI so Windows ANSI launcher arguments cannot corrupt paths.

Python loads jvm.dll by its Unicode path. Paths/properties reach Java as
UTF-16 JNI strings; no native launcher command line or shell is involved.
This process remains a descendant of the statechart Job Object.
"""
import ctypes as c
import json
import os
from pathlib import Path
import shutil
import sys


class Option(c.Structure):
    _fields_ = [("optionString", c.c_char_p), ("extraInfo", c.c_void_p)]


class InitArgs(c.Structure):
    _fields_ = [("version", c.c_int), ("nOptions", c.c_int),
                ("options", c.POINTER(Option)), ("ignoreUnrecognized", c.c_ubyte)]


class Value(c.Union):
    _fields_ = [("l", c.c_void_p), ("j", c.c_int64)]


class JavaException(RuntimeError):
    """An uncaught Java exception has the launcher's exit code 1."""


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    java = Path(shutil.which(data["java"]) or data["java"]).resolve()
    home = java.parent.parent
    dll = home / "bin/server/jvm.dll"
    if not dll.is_file():
        candidates = list((home / "bin").rglob("jvm.dll"))
        if not candidates:
            raise ValueError(f"Cannot locate jvm.dll beside {java}; use a Windows Java 11+ runtime")
        dll = candidates[0]
    directories = [os.add_dll_directory(str(folder)) for folder in {java.parent, dll.parent}]
    library = c.WinDLL(str(dll))
    args = data["args"]
    cp = args.index("-cp")
    properties = {}
    options = ["-Dfile.encoding=UTF-8", "-Dsun.stdout.encoding=UTF-8", "-Dsun.stderr.encoding=UTF-8"]
    for arg in args[:cp]:
        if arg.startswith("-D"):
            key, _, value = arg[2:].partition("=")
            properties[key] = value
        elif arg.isascii():
            options.append(arg)
        else:
            raise ValueError("Non-ASCII JVM options must be supplied as -D properties")
    encoded = [option.encode("ascii") for option in options]
    native_options = (Option * len(options))(*(Option(value, None) for value in encoded))
    init = InitArgs(0x00010008, len(options), native_options, False)
    vm, env = c.c_void_p(), c.c_void_p()
    create = library.JNI_CreateJavaVM
    create.argtypes = [c.POINTER(c.c_void_p), c.POINTER(c.c_void_p), c.POINTER(InitArgs)]
    create.restype = c.c_int
    status = create(c.byref(vm), c.byref(env), c.byref(init))
    if status:
        raise RuntimeError(f"JNI_CreateJavaVM failed ({status})")
    table = c.cast(env, c.POINTER(c.POINTER(c.c_void_p))).contents

    def function(index, result, *types):
        return c.WINFUNCTYPE(result, c.c_void_p, *types)(table[index])

    find = function(6, c.c_void_p, c.c_char_p)
    method = function(33, c.c_void_p, c.c_void_p, c.c_char_p, c.c_char_p)
    static = function(113, c.c_void_p, c.c_void_p, c.c_char_p, c.c_char_p)
    construct = function(30, c.c_void_p, c.c_void_p, c.c_void_p, c.POINTER(Value))
    call = function(36, c.c_void_p, c.c_void_p, c.c_void_p, c.POINTER(Value))
    static_call = function(116, c.c_void_p, c.c_void_p, c.c_void_p, c.POINTER(Value))
    void_call = function(63, None, c.c_void_p, c.c_void_p, c.POINTER(Value))
    static_void = function(143, None, c.c_void_p, c.c_void_p, c.POINTER(Value))
    new_string = function(163, c.c_void_p, c.POINTER(c.c_uint16), c.c_int)
    new_array = function(172, c.c_void_p, c.c_int, c.c_void_p, c.c_void_p)
    set_element = function(174, None, c.c_void_p, c.c_int, c.c_void_p)
    exception = function(228, c.c_ubyte)
    describe = function(16, None)

    def checked(value):
        if exception(env):
            describe(env)
            raise JavaException("Java invocation failed; see the exception above")
        return value

    def string(value):
        raw = value.encode("utf-16-le", errors="surrogatepass")
        units = (c.c_uint16 * (len(raw) // 2)).from_buffer_copy(raw)
        return checked(new_string(env, units, len(units)))

    def values(*objects):
        return (Value * len(objects))(*(Value(l=obj) for obj in objects))

    def klass(name):
        return checked(find(env, name.encode("ascii")))

    def mid(owner, name, signature, is_static=False):
        return checked((static if is_static else method)(env, owner, name.encode("ascii"), signature.encode("ascii")))

    system = klass("java/lang/System")
    set_property = mid(system, "setProperty", "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;", True)
    for key, value in properties.items():
        checked(static_call(env, system, set_property, values(string(key), string(value))))
    file_class = klass("java/io/File")
    uri_class = klass("java/net/URI")
    url_class = klass("java/net/URL")
    loader_class = klass("java/net/URLClassLoader")
    file = checked(construct(env, file_class, mid(file_class, "<init>", "(Ljava/lang/String;)V"),
                             values(string(args[cp + 1]))))
    uri = checked(call(env, file, mid(file_class, "toURI", "()Ljava/net/URI;"), None))
    url = checked(call(env, uri, mid(uri_class, "toURL", "()Ljava/net/URL;"), None))
    urls = checked(new_array(env, 1, url_class, None))
    checked(set_element(env, urls, 0, url))
    loader = checked(static_call(env, loader_class,
                     mid(loader_class, "newInstance", "([Ljava/net/URL;)Ljava/net/URLClassLoader;", True), values(urls)))
    thread_class = klass("java/lang/Thread")
    thread = checked(static_call(env, thread_class, mid(thread_class, "currentThread", "()Ljava/lang/Thread;", True), None))
    checked(void_call(env, thread, mid(thread_class, "setContextClassLoader", "(Ljava/lang/ClassLoader;)V"), values(loader)))
    main_class = checked(call(env, loader, mid(loader_class, "loadClass", "(Ljava/lang/String;)Ljava/lang/Class;"),
                              values(string(args[cp + 2]))))
    arguments = args[cp + 3:]
    array = checked(new_array(env, len(arguments), klass("java/lang/String"), None))
    for index, arg in enumerate(arguments):
        checked(set_element(env, array, index, string(arg)))
    checked(static_void(env, main_class, mid(main_class, "main", "([Ljava/lang/String;)V", True), values(array)))
    vm_table = c.cast(vm, c.POINTER(c.POINTER(c.c_void_p))).contents
    destroy = c.WINFUNCTYPE(c.c_int, c.c_void_p)(vm_table[3])
    return destroy(vm)


if __name__ == "__main__":
    try:
        status = main()
    except JavaException:
        status = 1
    except Exception as error:
        print(f"Windows Java bridge failed: {error}", file=sys.stderr, flush=True)
        status = 2
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(status)
