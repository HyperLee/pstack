# Windows 專用版本實作紀錄

依本次對話核定計畫實作：完整原生 Windows 工具支援；僅使用 `codex/windows-support` 分支，不合併、不推送、不建立 PR。

## 設計決策

- 使用目前 checkout 的獨立分支，依核定計畫不另建 worktree。
- Windows 預設實體複製，POSIX 保留連結。複製模式保存完整套件、註冊副本、相對定位檔及換行規範，避免權限與跨機器連結問題。
- 兩份技能內容是明確取捨：保留原有完整套件配置；不做隱藏同步或自動覆寫。安裝器檢查兩份內容，差異即停止。
- Windows statechart 使用 Python 標準庫 ctypes 的 Win32 Job Object；在 worker 開始執行前加入 job，避免程序建立競態。不新增 native 編譯套件。
- 保留所有測試證據及暫存資料，不執行目錄批次刪除。
- Windows CLI 測試取代 POSIX 專用 Shell/FIFO/signal 測試，其餘共用測試保留。POSIX 不在本機宣稱重新驗證。

## 執行紀錄

- 安裝新增測試先因缺少 copy 介面失敗，實作後 4 個案例通過。
- Pipe reader、UTF-8 BOM 設定及 TSV 新增測試先失敗，實作後通過。
- Job Object 新增測試先因缺少 supervisor 失敗，實作後驗證參數及兩種終止路徑通過。
- Windows 回放發現 CRLF 標記解析問題；新增字串／串流測試重現後修正共用換行解析。
- PR watcher 先有 1 個 POSIX fixture 失敗；以參數陣列和可注入 command runner 替換後，56 個測試通過。
- 實際 Codex app-server 已探索到 58 個 skills、58 個介面、0 錯誤；完整驗證結果見 [驗證紀錄](windows-verification.md)。

## 審查與修正

- 獨立唯讀審查指出 Python 3.9–3.11 沒有 `os.path.isjunction` 時會漏掉 Junction；已用 reparse-point 屬性補上偵測，回歸測試先重現再通過。
- 追加審查指出 JVM 前置參數不應繞過 Unicode bridge；已改為只有明確 `STATECHART_JAVA_MODE=direct` 的測試／wrapper 才繞過，真實 Unicode JAR 與 JVM flags 案例已驗證。
- Windows 原生 Java launcher 在 MS950 系統會改變字碼頁外的字元；新增 Python/JNI adapter，以 UTF-16 設定路徑及 URLClassLoader 載入 JAR。保留 Java/JRE 執行能力，完整 oracle 開發測試則要求 JDK。
- Windows 不允許直接 rename 覆蓋空目錄；發佈前將原空目錄保留於 staging，失敗時嘗試還原，不刪除目錄。

## 完成驗證

- Python 最終 27 個測試通過，包含 Git clone / checkout 後再次安裝。
- PR watcher 56 個測試及型別檢查通過。
- Statechart 最終整套 289 個測試通過，0 失敗、0 跳過；包含真實 TLC、4,000 組設定 oracle、渲染與 Windows 程序生命週期。
- Python 啟動入口也由外層 Job Object 保護；強制結束它後，Node / worker / Java 不殘留。
- JNI 未捕捉 Java 例外保留 Java launcher 的退出碼 1，adapter 自身錯誤為 2；SANY 診斷案例重新通過。
- Metadata / 文件連結靜態驗證及實際 Codex 58 skills / 58 interfaces 探索通過。
- 獨立唯讀審查追加檢查無重要未解決問題。保留原始測試證據，不清理目錄。
- 依使用者要求僅保留 Windows 分支，不採用合併、推送或 PR 整合方式。
