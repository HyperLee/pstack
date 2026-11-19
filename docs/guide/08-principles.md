# 24 個工程原則

原則是具體決策的提示，不是需要背誦的口號。主代理只在讀過該 leaf skill，且它確實改變決策時引用。

## 思考與範圍

1. Laziness Protocol：用最小足夠的改動解決問題。
2. Foundational Thinking：先選對資料形狀與共享邊界。
3. Redesign from First Principles：把新需求視為一開始就存在的條件。
4. Attack the Premise：相同前提連續失敗時，先測試前提。
5. Subtract Before You Add：移除不必要的複雜度再新增。
6. Minimize Reader Load：減少理解程式所需追蹤的層次與隱含狀態。
7. Outcome-Oriented Execution：朝已確認的目標結構收斂。
8. Experience First：以使用者與維護者的體驗判斷取捨。
9. Exhaust the Design Space：真正開放的設計問題值得比較替代方案。
10. Build the Lever：建立能重跑工作或證明結果的工具。

## 結構

11. Model the Domain：讓資料結構表達規則。
12. Boundary Discipline：在系統邊界處驗證。
13. Type System Discipline：盡可能讓非法狀態無法表示。
14. Make Operations Idempotent：讓重試收斂到同一結果。
15. Migrate Callers Then Delete Legacy APIs：在可協調範圍內完成呼叫端遷移。
16. Separate Before Serializing Shared State：先消除不必要的共享寫入。

## 驗證

17. Prove It Works：核對真正的成果。
18. Fix Root Causes：修正第一個錯誤決策，而非遮住症狀。
19. Sequence Work into Verifiable Units：每一個小單位都能驗收。
20. Test Behavior, Not Implementation：測試可觀察行為。
21. Explain the Number：先解釋數字的限制與可信度。

## 協作與改善

22. Guard the Context Window：大批資料留在適當的分析位置，主聊天保留結論與證據。
23. Never Block on the Human：已授權的可逆工作繼續做；這不是擴權條款。
24. Encode Lessons in Structure：重複出錯的事優先用結構、型別或檢查防止。

完整條件與細節見 [poteto-mode 的原則索引](../../skills/poteto-mode/SKILL.md#principles) 與各個 `principle-*` skill。

下一章：[建立自己的工作方式](09-make-it-yours.md)。
