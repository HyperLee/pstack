# Benny：選配的問題分類與重現流程

Benny 將一則 Slack 問題報告分成兩階段：先分類與查重，再重現已確認的問題、驗證既有修復，必要時準備有限範圍的 draft PR。

這個目錄不會隨主要 skills 註冊；請讓 Codex 直接讀取 [操作契約](FOR_AGENTS.md)。Codex 版本以手動執行為基礎，排程範本目前尚未連接事件來源。

1. 在目標專案安裝完整 pstack 套件。
2. 指定目標專案，請 Codex 讀取操作契約並執行 setup。
3. 將設定、feature map 與 routing map 放在 `.codex/benny/`，與工作流來源分開。
4. 提供原始報告的 channel、thread 與 message 座標，並明確說明允許哪些外部寫入。
5. 具備 Slack、tracker 與實際應用程式控制工具後，才執行相應階段。

沒有 Slack 連接器、來源座標或操作授權時，流程會回報缺口，不發送訊息。新增 Slack 事件觸發或定期處理，需要額外的輸入轉接與持久化去重機制；本套件不包含這個服務。

範本可從 [設定檔](templates/configuration.example.yaml) 開始。秘密值使用環境變數或秘密管理服務，勿寫入設定、聊天或版本控制。
