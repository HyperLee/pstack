import { finished } from "node:stream/promises";
import { groupOutlivesWorker, killGroup } from "./kill.ts";

// The pipe closes even if the parent is killed before it can stop the worker.
let input = "";
process.stdin.setEncoding("utf8").on("data", (chunk: string) => (input += chunk));
await finished(process.stdin).catch(() => {});

// Windows can reuse the PID once the worker exits. POSIX groups can still have members.
if (groupOutlivesWorker || !input.includes("exited\n"))
  await killGroup(Number(process.argv[2]));
