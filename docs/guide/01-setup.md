# 安裝與設定

先從 [README 的安裝步驟](../../README.md#安裝) 選擇安裝層級。基本需求為 Python 3.9+、Git 與 Codex；進階工具才需要 Bun 或 Java／TLC。

## 選擇安裝層級

個人安裝在 `~/.agents/skills/` 連結目前 checkout，適合跨專案使用。請保留來源目錄。

專案安裝將完整套件複製到 `.codex/pstack/`，並建立 `.agents/skills/` 的相對連結；兩者一起分享，才能讓其他 checkout 讀到相同內容。遇到衝突時，安裝程式先停止，不覆蓋本地修改。

同名技能可能同時出現在多個安裝層級。選擇明確的來源，不假定 Codex 會合併它們。找不到新技能時，先確認連結，再開啟新聊天。

## 保留繼承設定，或調整預算

不執行 setup 也能使用。預設繼承聊天模型與推理設定，最多 3 個 workers。

```text
$setup-pstack 使用專案設定，繼承模型，最多兩個 workers。
```

設定由 pstack 讀取，不修改全域 `config.toml` 或 `AGENTS.md`。專案設定整份優先於個人設定；格式與角色見 [執行規約](../../skills/poteto-mode/references/codex-runtime.md)。

模型不可用時不猜測替代代號。實際工具不支援模型／推理覆寫時，回報限制並繼承。降低 workers、候選方案數與任務範圍，可以減少成本。

接著試一個能明確驗收的小任務，再逐漸擴大分工。

下一章：[使用主要入口](02-poteto-mode.md)。
