import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";
import { pathToFileURL } from "node:url";

const here = import.meta.dirname;
const corpus = path.join(here, "corpus");
const entry = path.join(here, "../statechart.ts");
const windows = process.platform === "win32";
const read = (file: string) => fs.readFileSync(file, "utf8");

for (const name of fs.readdirSync(corpus)) {
  test(`Windows replay ${name}: publishes committed chart and report`, { skip: !windows }, () => {
    const dir = path.join(corpus, name);
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack 中文 replay-"));
    const out = path.join(root, "output with spaces");
    const view = path.join(dir, "view.mjs");
    const r = spawnSync(process.execPath, [entry, path.join(dir, `${name}.tla`),
      ...(fs.existsSync(view) ? ["--view", view] : []), "--out", out, "--timeout-ms", "30000"], {
      encoding: "utf8", timeout: 40000,
      env: { ...process.env, JAVA: process.execPath, TLA2TOOLS: "replay.jar",
        STATECHART_JAVA_MODE: "direct", STATECHART_JAVA_ARGS: JSON.stringify([path.join(here, "java.ts")]), STATECHART_REPLAY: dir },
    });
    assert.ifError(r.error);
    assert.equal(r.stderr, "");
    const first = path.join(dir, "verdict-1.exit");
    const code = fs.existsSync(first) ? Number(read(first)) : 0;
    assert.equal(r.status, code === 0 ? 0 : [11, 12, 13].includes(code) ? 1 : 2);
    assert.equal(read(path.join(out, "report.md")), read(path.join(dir, "report.md")));
    assert.equal(read(path.join(out, "chart.mmd")), read(path.join(dir, "chart.mmd")));
  });
}

test("Windows timeout stops Java and publishes no output", { skip: !windows }, () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-timeout-"));
  const fake = path.join(root, "java.mjs");
  const pid = path.join(root, "pid");
  fs.writeFileSync(fake, `import fs from 'node:fs';fs.writeFileSync(${JSON.stringify(pid)},String(process.pid));setInterval(()=>{},1000);`);
  const out = path.join(root, "out");
  const r = spawnSync(process.execPath, [entry, path.join(corpus, "Login/Login.tla"),
    "--out", out, "--timeout-ms", "2000"], { encoding: "utf8", timeout: 15000,
    env: { ...process.env, JAVA: process.execPath, TLA2TOOLS: "fake.jar",
      STATECHART_JAVA_MODE: "direct", STATECHART_JAVA_ARGS: JSON.stringify([fake]) } });
  assert.ifError(r.error);
  assert.equal(r.status, 2);
  assert.match(r.stderr, /timed out/);
  assert.equal(fs.existsSync(out), false);
  assert.ok(fs.existsSync(pid));
  assert.throws(() => process.kill(Number(read(pid)), 0), /ESRCH/);
});

for (const launcher of ["node", "python"]) test(`Windows ${launcher} parent termination closes the lifetime pipe and stops Java`, { skip: !windows }, async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-parent-stop-"));
  const fake = path.join(root, "java.mjs");
  const pid = path.join(root, "pid");
  fs.writeFileSync(fake, `import fs from 'node:fs';fs.writeFileSync(${JSON.stringify(pid)},String(process.pid));setInterval(()=>{},1000);`);
  const out = path.join(root, "out");
  const child = spawn(launcher === "node" ? process.execPath : (process.env.PSTACK_PYTHON || "python"),
    [launcher === "node" ? entry : path.join(here, "../statechart.py"),
      path.join(corpus, "Login/Login.tla"), "--out", out], {
    stdio: "ignore", env: { ...process.env, JAVA: process.execPath, TLA2TOOLS: "fake.jar",
      STATECHART_JAVA_MODE: "direct", STATECHART_JAVA_ARGS: JSON.stringify([fake]) },
  });
  const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
  try {
    for (let i = 0; i < 200 && !fs.existsSync(pid); i++) await sleep(50);
    assert.ok(fs.existsSync(pid));
    const exited = new Promise((resolve) => child.once("exit", resolve));
    child.kill();
    await exited;
    const java = Number(read(pid));
    let alive = true;
    for (let i = 0; i < 100; i++) {
      try { process.kill(java, 0); } catch { alive = false; break; }
      await sleep(50);
    }
    assert.equal(alive, false);
    assert.equal(fs.existsSync(out), false);
  } finally {
    if (child.exitCode === null) child.kill();
    if (fs.existsSync(pid)) {
      try { process.kill(Number(read(pid))); } catch { /* Already stopped by its job. */ }
    }
  }
});

test("Windows cancellation handler stops Java without publishing", { skip: !windows }, () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-cancel-"));
  const pid = path.join(root, "pid");
  const fake = path.join(root, "java.mjs");
  const hook = path.join(root, "cancel.mjs");
  fs.writeFileSync(fake, `import fs from 'node:fs';fs.writeFileSync(${JSON.stringify(pid)},String(process.pid));setInterval(()=>{},1000);`);
  fs.writeFileSync(hook, `import fs from 'node:fs';
    if(process.argv[1]===${JSON.stringify(entry)}) {
      const poll=setInterval(()=>{if(fs.existsSync(${JSON.stringify(pid)})){clearInterval(poll);process.emit('SIGINT');}},20);
    }`);
  const out = path.join(root, "out");
  const r = spawnSync(process.execPath, ["--import", pathToFileURL(hook).href, entry,
    path.join(corpus, "Login/Login.tla"), "--out", out], { encoding: "utf8", timeout: 15000,
    env: { ...process.env, JAVA: process.execPath, TLA2TOOLS: "fake.jar",
      STATECHART_JAVA_MODE: "direct", STATECHART_JAVA_ARGS: JSON.stringify([fake]) } });
  assert.ifError(r.error);
  assert.equal(r.status, 130);
  assert.match(r.stderr, /SIGINT stopped/);
  assert.equal(fs.existsSync(out), false);
  assert.throws(() => process.kill(Number(read(pid)), 0), /ESRCH/);
});

for (const existing of [false, true]) {
  test(`Windows output directory ${existing ? "with content is preserved" : "empty is accepted"}`,
    { skip: !windows }, () => {
      const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-output-"));
      const out = path.join(root, "out");
      fs.mkdirSync(out);
      if (existing) fs.writeFileSync(path.join(out, "mine.txt"), "user content");
      const r = spawnSync(process.execPath, [entry, path.join(corpus, "Login/Login.tla"), "--out", out], {
        encoding: "utf8", timeout: 15000, env: { ...process.env,
          JAVA: process.execPath, TLA2TOOLS: "replay.jar", STATECHART_REPLAY: path.join(corpus, "Login"),
          STATECHART_JAVA_MODE: "direct", STATECHART_JAVA_ARGS: JSON.stringify([path.join(here, "java.ts")]) },
      });
      assert.ifError(r.error);
      assert.equal(r.status, existing ? 2 : 0, r.stderr);
      if (existing) assert.equal(read(path.join(out, "mine.txt")), "user content");
      else assert.ok(fs.existsSync(path.join(out, "report.md")));
    });
}

test("Windows missing Java/TLC and bad timeout fail with diagnostics", { skip: !windows }, () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-diagnostic-"));
  for (const args of [[], ["--timeout-ms", "0"]]) {
    const r = spawnSync(process.execPath, [entry, path.join(corpus, "Login/Login.tla"),
      "--out", path.join(root, "out"), ...args], { encoding: "utf8", timeout: 15000,
      env: { ...process.env, JAVA: "", TLA2TOOLS: "", STATECHART_JAVA_ARGS: "[]" } });
    assert.equal(r.status, 2);
    assert.match(r.stderr, args.length ? /--timeout-ms/ : /Set TLA2TOOLS/);
    assert.equal(fs.existsSync(path.join(root, "out")), false);
  }
});

test("Windows real Java keeps Unicode source/JAR paths with configured JVM flags",
  { skip: !windows || !process.env.TLA2TOOLS }, () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), "pstack-é 中文 🐮-"));
    const dir = path.join(root, "spec-é 中文 🐮");
    fs.cpSync(path.join(corpus, "Login"), dir, { recursive: true });
    const jar = path.join(root, "tools-é 中文 🐮.jar");
    fs.copyFileSync(process.env.TLA2TOOLS!, jar);
    const out = path.join(root, "out");
    const r = spawnSync(process.execPath, [entry, path.join(dir, "Login.tla"), "--view",
      path.join(dir, "view.mjs"), "--out", out, "--timeout-ms", "30000"], {
      encoding: "utf8", timeout: 40000, env: { ...process.env, TLA2TOOLS: jar,
        STATECHART_JAVA_ARGS: '["-Xmx256m"]' },
    });
    assert.ifError(r.error);
    assert.equal(r.status, 0, r.stderr);
    assert.equal(read(path.join(out, "chart.mmd")), read(path.join(corpus, "Login/chart.mmd")));
  });
