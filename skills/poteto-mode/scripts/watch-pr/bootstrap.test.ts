import { describe, expect, it } from "bun:test";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

describe("read-only dependency preflight", () => {
  for (const prepared of [false, true]) {
    it(prepared ? "uses prepared dependencies without source writes" : "reports preparation without installing", () => {
      const root = mkdtempSync(join(tmpdir(), "pstack-bootstrap-"));
      copyFileSync(join(import.meta.dir, "../bootstrap.ts"), join(root, "bootstrap.ts"));
      if (prepared) {
        mkdirSync(join(root, "node_modules/commander"), { recursive: true });
        writeFileSync(join(root, "node_modules/commander/package.json"), "{}");
      }
      const before = readdirSync(root, { recursive: true }).sort();
      const result = spawnSync(process.execPath, ["-e",
        `import {ensureDependenciesInstalled} from ${JSON.stringify(join(root, "bootstrap.ts"))}; ensureDependenciesInstalled();`],
        { encoding: "utf8" });
      expect(result.status).toBe(prepared ? 0 : 1);
      if (!prepared) expect(result.stderr).toContain("bun install --frozen-lockfile");
      expect(readdirSync(root, { recursive: true }).sort()).toEqual(before);
    });
  }
});
