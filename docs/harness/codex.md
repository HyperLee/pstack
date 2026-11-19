# Codex 執行環境

本分支的 skills 已直接使用 Codex 語意，不需要 Cursor 指令轉接層。完整的代理規約位於 [codex-runtime.md](../../skills/poteto-mode/references/codex-runtime.md)，工具使用型 skills 會先讀取它。

| 項目 | 桌面 App | CLI |
| --- | --- | --- |
| Skill 呼叫 | 使用可用的選擇介面 | `/skills` 或 `$skill-name` |
| 多代理 | 依目前提供的 spawn／follow-up／wait 工具 | 依目前提供的同類工具 |
| 隔離 | 優先使用 App 管理的 worktree | 適合環境中的 worktree／獨立輸出 |
| 聊天歷史 | 可用且已限定專案的聊天工具 | 目前對話、指定匯出檔與 resume note |
| 缺少功能 | 回報缺口，不虛構工具 | 相同原則 |

原始 Cursor `Task` 的欄位、指定 cloud environment 與自訂 agent type 都不是可直接送給 Codex 的參數。以當前可呼叫 schema 為準；不把某一版工具名稱硬編碼成所有版本的保證。

Skill 的位置依 runtime 規約解析：Windows 實體副本使用旁邊的 `.pstack-suite.json` 相對定位完整套件；連結模式解析真實路徑。兩種模式都必須能定位 sibling skills、指南與角色參考。專案安裝的 `.codex/pstack/` 與 `.agents/skills/` 一起納入版本控制。

此分支以原生 Windows / PowerShell 為主要目標，保留 POSIX 入口；詳細需求與驗證狀態見 [Windows 指南](../windows.md)。不保證關機或休眠後持續執行。
