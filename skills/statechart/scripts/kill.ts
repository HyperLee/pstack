import { spawn } from "node:child_process";
import path from "node:path";

export const groupOutlivesWorker = process.platform !== "win32";

export async function killGroup(pid: number) {
  if (!Number.isSafeInteger(pid) || pid <= 0) return;
  if (!groupOutlivesWorker) {
    const systemRoot = process.env.SystemRoot ?? process.env.WINDIR;
    const executable = systemRoot
      ? path.win32.join(systemRoot, "System32", "taskkill.exe")
      : "taskkill.exe";
    await new Promise<void>((resolve, reject) => {
      const taskkill = spawn(executable, ["/pid", String(pid), "/t", "/f"], {
        stdio: "ignore",
        windowsHide: true,
      });
      taskkill.once("error", reject);
      taskkill.once("exit", (code, signal) => {
        if (code === 0) resolve();
        else reject(new Error(`taskkill could not stop worker ${pid} (exit ${code ?? signal}).`));
      });
    });
    return;
  }
  try {
    process.kill(-pid, "SIGKILL");
  } catch (error) {
    if (!(error && typeof error === "object" && "code" in error && error.code === "ESRCH"))
      throw error;
  }
}
