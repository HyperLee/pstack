# 實作、測試與整理差異

不同任務需要不同證據。

- 修復先保留可重現的失敗，再確認根因。
- 新功能先定義使用者可見行為與資料形狀。
- 重構先固定目前契約，再證明行為相同。
- 效能工作先建立可信基準，再用 profile 解釋改善。

```text
$poteto-mode 將解析集中到一個模組，行為完全不變。先記錄目前輸出，再證明修改後相同。
```

[`tdd`](../../skills/tdd/SKILL.md) 優先使用便宜、聚焦的失敗測試；若測試需要大量脆弱 mock，選擇更直接的可執行檢查並說明限制。

## 整理程式與文字

使用專案既有 lint、build 與測試，不依賴外部 Cursor plugin。清除沒有用途的防衛邏輯、遺留路徑與不相關變更，但不要把順手重構擴大成另一個專案。

[`no-comments`](../../skills/no-comments/SKILL.md) 的獨立 reviewer 只讀取與報告，由主代理判斷接受哪些變更。授權、license、必要註解與可證明的外部限制仍需保留。唯讀審查不會因為 skill 名稱而自動修改程式。

[`unslop`](../../skills/unslop/SKILL.md) 整理文字；[`technical-writing`](../../skills/technical-writing/SKILL.md) 協助寫清楚文件與 PR 描述。TypeScript 規則可用 `$typescript-best-practices` 明確載入。

每個小單位完成就檢查；先確認這一步有效，再開始下一步。刪除目錄或批次清理暫存檔仍交由使用者手動處理。

下一章：[驗證與交付](06-verify-and-ship.md)。
