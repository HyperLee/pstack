import { existsSync } from "node:fs";
import { join } from "node:path";

export function ensureDependenciesInstalled(): void {
  const scripts = import.meta.dir;
  if (!existsSync(join(scripts, "node_modules", "commander", "package.json"))) {
    throw new Error(
      `watch-pr dependencies are not prepared. Run bun install --frozen-lockfile in ${scripts}. ` +
      "This command does not install dependencies or modify the skill source automatically.",
    );
  }
}
