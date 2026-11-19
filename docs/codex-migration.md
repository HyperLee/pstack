# Codex 移植架構與驗證

## 來源與盤點

移植基準為本 checkout 的初始提交 `333d3ab`，原套件 manifest 版本為 0.15.43。主要套件有 58 個 skills，其中包含 24 個原則；poteto-mode 有 22 個 playbooks。Benny 另有 3 份直接讀取的操作文件，不列入一般技能探索。

原版經 Codex skill-creator 的格式檢查時，有 57 個主要 skills 帶有不接受的 frontmatter 欄位。移植後保留 name／description 等標準欄位，將手動呼叫政策移入 agents/openai.yaml。

## 上游更新比對紀錄

### 2026-11-19：上游 0.15.44

以本機原始快照 `333d3ab`（0.15.43）比對上游固定提交 [`e58dd043600587dbaf58ba315e7f2b38373eeb43`](https://github.com/cursor/plugins/commit/e58dd043600587dbaf58ba315e7f2b38373eeb43)（0.15.44）的 `pstack/` 子目錄，共 551 個檔案，7 個變更，無新增或刪除。此紀錄表示已檢查該上游版本；原始移植基準仍為 0.15.43。

| 上游變更 | Codex 版處理 |
| --- | --- |
| arena、poteto-mode 的 Gemini 預設由 Carbon 改為 Neon，推理維持 high 上限 | 維持模型繼承或已確認支援的角色設定，依實際工具能力處理，不加入固定 Gemini 模型名稱或專屬上限 |
| setup-pstack 自動將 panel 中非 Neon 的舊 Gemini 4 設定替換為 Neon | 保留使用者設定，不自動遷移 Cursor 模型規則；模型覆寫仍須確認當前環境支援 |
| README、Claude Code harness 文件與兩份 plugin manifest 更新模型名稱或版本 | 保留 Codex 文件與安裝方式，僅補記上游比對結果，不恢復原平台入口 |

結論：此次無須同步 skills、執行工具或設定格式；58 個主要 skills、22 個 playbooks 與 24 個原則的數量不變。

## 調整對照

| 原始相依 | Codex 版本 |
| --- | --- |
| Cursor plugin manifests | 移除，改用本機／專案 skill 安裝程式 |
| Cursor Task、自訂 agent type | 真實可用的 Codex 工具與角色參考文件 |
| 固定 Claude／Gemini 代號 | 繼承目前模型，或使用已確認可用的設定 |
| always-applied model rule | pstack 自行讀取的專屬 JSON |
| 外部 deslop／control plugins | 專案既有檢查與當前可用控制工具 |
| 私人 transcript 路徑 | 範圍受限的聊天工具／指定匯出檔 |
| `/loop` 與 cloud persistence | 目前任務中的 watcher／事件等待 |
| 自動刪除 worktree／暫存目錄 | 唯讀盤點、保留證據、人工清理 |
| Slack 原生 trigger 假設 | 明確來源座標與額外輸入轉接需求 |

## 來源、安裝與修改

個人安裝用絕對連結指向來源；專案安裝用完整 vendor payload 加相對連結。payload 排除 Git metadata、node_modules、Python cache 與工作紀錄；包含安裝與驗證所需來源。

每次解析相依先取得 SKILL.md 的 canonical path，再定位 suite root。修改 interdependent skills 時保留完整套件來源；唯讀來源先交付 patch 與目的地需求，不建立失去相依的單一覆本。

模型 profile 有 schema_version、budget、max_workers、roles。專案檔整份優先於個人檔；格式錯誤須明確處理。模型權限仍由目前 runtime 決定，profile 驗證只證明資料形狀，不證明帳號可呼叫該模型。

## 執行工具

PR watcher 保留既有 CLI／輸出與決策核心，取消執行時自動安裝。statechart 保留 TLC pipeline、圖形與報告語意，取消程序群組的能力仍保留；目錄不再自動刪除。

暫存成果保留在每次執行的工作目錄。CLI 會顯示 statechart 的保留位置。測試可使用 [run-checks.sh](../scripts/run-checks.sh) 將輸出與暫存資料收在一個目錄；它不執行目錄清理。

## 驗證方式

- `python3 scripts/validate.py`：frontmatter、UI policy、相依檔與移植相依檢查。
- `python3 -B -m unittest discover -s tests -v`：安裝、profile、Benny 來源輸入與唯讀盤點。
- PR watcher：`bun test watch-pr`、`bun run typecheck`。
- statechart：`node --test test/*.test.ts`。TLC lane 需有效的 Java 與 TLA2TOOLS；renderer lane 需網路及套件。
- 行為檢查：在無外部寫入的獨立情境中檢查缺少工具、分工、授權與未連接範本。

執行結果另見 [驗證紀錄](verification.md)。缺少前置需求或未連接的服務不會被列為成功的實際整合。此次不發送真實 Slack 訊息、不建立排程，也不對真實 PR 進行合併。
