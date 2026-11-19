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

Skill 的真實位置必須先解析連結，才能定位完整套件中的 sibling skills、指南與角色參考。個人安裝依賴來源 clone，專案安裝將來源放在專案內，使用相對連結保持可攜性。

目前支援範圍以 POSIX 工具環境為基礎；尚未宣稱原生 Windows 或關機後執行能力。
