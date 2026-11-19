# 驗證與交付

「編譯成功」只能證明編譯成功。使用者在乎的行為，需要在真正的應用程式、CLI 或 API 上驗證。

## 建立可重跑的驗證

[`create-verification-skill`](../../skills/create-verification-skill/SKILL.md) 會檢查專案的啟動方式、控制介面、證據來源與隔離方式，再建立專案 `.agents/skills/verify-<app>/`。

驗證需涵蓋啟動、健康檢查、實際操作、可見結果與副作用。feature map 是可維護的旅程索引，不是為了一次成功而簡化的假路徑。用 [`maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md) 持續對照程式與實際產品。

## 形式驗證與數字

對重試、併發、狀態轉移等問題，可用形式驗證檢查明確範圍內的性質。[statechart](../../skills/statechart/SKILL.md) 使用 TLC，產出報告與 Mermaid；仍需把反例對照真正程式，不能把模型正確視為產品已被證明。

效能數據先通過 [benchmark-checklist](../../skills/benchmark-checklist/SKILL.md)：同等條件、實際工作量、錯誤數、重複次數、變異與瓶頸解釋。數字不合理時，先檢查量測方法。

## PR 與合併

PR 是被要求時的交付方式。依實際授權建立、推送或合併；讀取 CI 不代表已取得 merge 授權。

Babysit 整理真正未完成的檢查；Shipping 要求獨立驗證覆蓋目前 patch，並確認真正合併完成。排入 merge queue 或設定 auto-merge，不等於已合併。

沒有必要的獨立 verifier、工具或權限時，留下明確缺口，不弱化完成條件。目錄與 evidence 的保留位置也應一併交付。

下一章：[長時間任務](07-overnight.md)。
