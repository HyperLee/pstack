# pstack 使用指南

這份指南以 Codex 桌面 App 與 CLI 為對象。先理解工作流，再用一個小而真實的任務建立可驗證的信任。

1. [安裝與設定](01-setup.md)：選擇個人或專案安裝、模型與 worker 數。
2. [使用主要入口](02-poteto-mode.md)：用目標與完成條件選擇 playbook。
3. [理解現有程式](03-understand.md)：行為、歷史、教學與工作接續。
4. [設計與分工](04-design.md)：比較方案、平行覆蓋與反例審查。
5. [實作與整理](05-build-and-clean.md)：修復、重構、測試與差異檢查。
6. [驗證與交付](06-verify-and-ship.md)：實際產品、形式驗證、數據與 PR。
7. [長時間任務](07-overnight.md)：完成條件、紀錄、暫停與恢復。
8. [工程原則](08-principles.md)：24 個可具體運用的原則。
9. [建立自己的工作方式](09-make-it-yours.md)：偏好、反思與結構性改善。
10. [範例與常見問題](10-recipes-and-pitfalls.md)：可直接改寫的任務範例。

CLI 範例使用 `$skill-name`；桌面 App 可透過其 skill 選擇介面加入相同 skill。檔案中的英文指示不限定回覆語言。

不知道如何開始時：

```text
$poteto-help 我想審查目前分支，應該使用哪一個 skill？
```

Help 會說明與提供範例，不會僅因你問了使用方式就開始昂貴的多代理工作。
