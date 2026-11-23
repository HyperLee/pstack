# 驗證紀錄

驗證日期：2026-11-19。變更位於 Codex 管理的隔離 worktree，基準為來源提交 `333d3ab`。

## 自動檢查

| 檢查 | 結果 |
| --- | --- |
| Codex skill-creator `quick_validate.py` | 61／61 通過：58 個主要 skills、3 個 Benny 操作文件 |
| 套件 validator | 58 個主要 skills、22 個 playbooks、24 個原則、UI metadata 與本機引用通過 |
| 原生 Codex `skills/list` | 58 個 skills、58 份介面資訊、0 個解析錯誤 |
| Python 行為測試 | 15／15 通過 |
| PR watcher Bun 測試 | 56／56 通過 |
| TypeScript strict／noEmit | 通過 |
| statechart Node／TLC／renderer 測試 | 373／373 通過，0 skipped |
| `git diff --check` | 通過 |

共 444 項自動測試通過，未把重跑次數或人工情境重複計入。

Python 測試涵蓋個人／專案安裝、dry-run 不寫入、衝突時不部分安裝、重跑不變、含空白路徑、專案搬移、profile 格式與優先順序、Benny 字串時間戳，以及不抓取遠端／不改 refs 的 worktree 盤點。另以真實 Git worktree 搬移情境確認失效註冊路徑會回報未知並繼續，不中斷整份盤點。

statechart 驗證包含 SIGINT、SIGTERM、SIGKILL、自有子程序停止、原子輸出、成功／失敗時保留工作目錄、語法與 TLC corpus、圖形與 renderer。寫入中止測試以可觀察的實際檔案寫入階段同步，避免「偵測到檔案時程序已經完成」的排程競態。

## 原生與獨立情境

使用 Codex CLI 0.170.0 的 app-server，在暫存 Git 專案中安裝完整套件，只呼叫 initialize 與 skills/list，未建立聊天或執行模型任務。可透過下列腳本重跑：

```bash
python3 -B scripts/check-discovery.py
```

另外透過實際原生 Codex subagents 執行 swarm：兩個獨立 workers 分別讀取 installer 與 profile 的目前未提交來源，執行 6 項與 4 項既有測試，主代理收集兩份終端證據。四份來源檔案的 SHA-256 前後一致，沒有共享寫入或使用固定模型代號。

Benny 的獨立唯讀情境提供離線報告、已配置的 operations channel、全部關閉的寫入旗標，以及缺少的 Slack 連接器／App adapter。結果正確停在未驗證／Blocked 狀態，保留字串座標與證據缺口，不建立 operations thread、不發訊息、不寫 tracker／PR，也不把離線 marker 當成已確認的 triage。

## 審查修正

獨立唯讀審查發現的兩項功能問題已處理：失效 worktree 路徑造成盤點中斷，以及 Benny operations-channel 授權與來源 thread 契約不一致。前者有失敗後通過的真實 Git 回歸測試；後者統一為獨立的旗標與明確授權，並經上述無寫入情境核對。另修正 setup 的 discovery description，改為描述實際 JSON 設定。

第一個指定模型的審查因額度限制未啟動，已改由可用的獨立 Codex 代理完成審查；未將失敗的代理列為已完成的評審。

## 環境與重跑

本次環境為 macOS arm64、Python 3.9.6、Node 26.13.0、Bun 1.4.4、TypeScript 7.0.2、Temurin Java 25.0.5 與 TLC 1.7.4。TLC jar 的 SHA-256 與原始程式釘選值相同。額外工具與相依套件置於暫存測試環境，未全域安裝。

完整重跑入口：

```bash
PSTACK_BUN=/path/to/bun \
TLA2TOOLS=/path/to/tla2tools.jar \
JAVA=/path/to/java \
bash scripts/run-checks.sh
```

程序中止與 native app-server 檢查需要允許存取自有子程序／本機 runtime 的環境；受限沙箱的拒絕不能算成產品通過。測試 runner 將 npm cache 與成果導向自己的暫存根目錄。

本次完整輸出保留於 `/tmp/pstack-all-checks-final.log`，測試暫存資料保留於 `/tmp/pstack-full-statechart-20261119`；其他檢查也會各自顯示保留路徑。目錄清理由使用者手動執行。

## 未驗證的外部範圍

未發送真實 Slack 訊息、修改真實 tracker、建立排程、觸發外部 webhook 或合併真實 PR。這些仍是需要工具、設定與授權的選配整合。原生 Windows、其他作業系統，以及桌面 skill 選擇介面的逐項操作尚未完整實測，不以此次 macOS／原生探索結果代替。

## 2026-11-24 statechart 相容性更新

- 在 macOS arm64 使用 Node 26.13.0、Temurin 25.0.5.1 與 TLC 1.7.4 執行完整 `statechart` 測試，412／412 通過，0 skipped。涵蓋 33 個 CRLF 重播案例、串流邊界、真實 TLC、renderer、程序中止及暫存保留。
- 另外用 Bun 1.4.4 與 Deno 2.9.6 驗證真實 TLC 可辨識 `NotOne`，並確認執行中的 CLI 收到 `SIGKILL` 後會停止測試子程序並保留暫存資料。
- 套件 validator 與 15 項 Python 測試全數通過。Codex app-server 探索到 58 個技能與 58 份介面資訊，0 個解析錯誤。
- Windows 的 `taskkill` 錯誤與既有輸出目錄檢查已用模擬環境驗證。原生 Windows 的 Java／TLC 啟動、輸出及中止仍待實機驗證。
