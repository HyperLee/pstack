# Windows 版本驗證紀錄

日期：2026-11-19。分支：`codex/windows-support`；不合併回 `main`。

## 實測環境

| 項目 | 版本 |
| --- | --- |
| 作業系統 | Windows 11 專業版 x64，10.0.26300 |
| Python | 3.14.4 |
| Node | 25.9.0 |
| Bun | 1.3.13 |
| Java | Eclipse Temurin 21.0.8+9；JDK 完整測試，JRE 基本執行也驗證 |
| TLC | 1.7.4 |

TLC JAR SHA-256：`936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`。
測試用 Bun / Java / TLC 採工作目錄內的可攜工具，不修改全域安裝或 Codex 設定。

## 最終檢查

| 檢查 | 結果 |
| --- | --- |
| Python 安裝、設定、安全、工具及 Job Object 測試 | 27 個通過 |
| PR watcher Bun 測試 | 56 個通過 |
| PR watcher TypeScript 型別檢查 | 通過 |
| 技能、UI metadata、文件連結靜態驗證 | 58 skills、3 Benny 檔案、22 playbooks 通過 |
| Codex app-server 實際技能探索 | 58 skills、58 interfaces、0 errors |
| Statechart 全套 Windows / 共用測試 | 289 個通過，0 失敗、0 跳過 |
| Mermaid / Pele 渲染測試單獨重跑 | 75 個通過 |
| Bun runtime + 真實 Java/TLC Login 案例 | 通過，產生 chart 與 report |
| 獨立唯讀程式碼審查 | 發現的兩項問題已修正；追加審查無重要未解決問題 |

Windows 測試入口以對應的 CLI / 程序案例取代 POSIX 專用 Shell、FIFO 與 signal 測試，沒有把未執行的 POSIX 案例列為通過。

## 已覆蓋的行為

- 安裝預覽不寫入；重跑不重寫；同名路徑、修改後套件或技能副本不覆寫。
- 中文／空白專案路徑；整個專案搬移；Git commit、clone / checkout 後再次安裝。
- 舊版 Python 缺少 `isjunction` 時仍拒絕 Junction；不向其外部目標寫入。
- 安裝中斷時回報並保留產物，不批次刪除。
- UTF-8 BOM JSON；UTF-8 TSV 附加、欄位清理及試算表公式防護。
- 真實 Win32 Job Object：正常退出碼、Unicode / 引號參數、關閉控制 pipe、強制結束 supervisor。
- Node 與 Python 啟動入口被強制結束後，worker / Java 停止且不發佈未完成輸出。
- 取消處理與逾時；既有非空輸出保留；空輸出目錄可正常發佈。
- 真實來源與 JAR 路徑含 `é 中文 🐮`，搭配 JVM 參數仍可執行。
- CRLF TLC 訊息的字串與串流輸入，及 Java/SANY 錯誤診斷退出碼。
- 4,000 組設定與真實 TLC 的比對測試。

## 證據與限制

最終結果取自本機各項檢查重跑；開發中發現的失敗經修正後重新驗證，不以先前失敗當成通過。渲染測試曾遇到 npm `ECONNRESET`，重跑後通過。

本機證據保留在 `.superpowers/windows-support/`：`python-final.log`、`statechart-final.log`、`render-final.log`，以及 `final-checks/` 的 watcher / 型別 / discovery 紀錄。暫存目錄由各測試列出，均保留供人工清理，不納入版本控制。

本次沒有實測其他 Windows / Python / Node 版本、POSIX 回歸、桌面 App 技能選單點選，或需要登入的真實 GitHub PR 監看。實際技能探索透過 Codex app-server 驗證。已新增 Windows GitHub Actions 工作流，但本次未推送，因此未執行遠端 CI。未合併、未建立 PR。
