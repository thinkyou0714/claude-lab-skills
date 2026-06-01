---
description: "論点整理・前提検証・意思決定支援を行う。問いや状況を渡すと、issue-framing から decision-materials まで必要な Skill を順に適用する。"
argument-hint: "<問い・状況・検討したいこと>"
allowed-tools: Read,Grep
---

この command が使う skills:

- issue-framing: ../../skills/issue-framing/SKILL.md
- assumption-audit: ../../skills/assumption-audit/SKILL.md
- boundary-check: ../../skills/boundary-check/SKILL.md
- risk-scan: ../../skills/risk-scan/SKILL.md
- tradeoff-analysis: ../../skills/tradeoff-analysis/SKILL.md
- critique-panel: ../../skills/critique-panel/SKILL.md
- success-failure-criteria: ../../skills/success-failure-criteria/SKILL.md
- decision-materials: ../../skills/decision-materials/SKILL.md

## 手順

1. `issue-framing` を読み込み、渡された問い・状況を「論点 / 根拠 / 問いの構造」に分解する
2. `assumption-audit` を読み込み、分解した論点の前提を列挙・検証する
3. `boundary-check` を読み込み、検討範囲の境界を確認する（何を含めるか / 含めないか）
4. `risk-scan` を読み込み、この問いに関連するリスクを洗い出す
5. 複数の選択肢が存在する場合は `tradeoff-analysis` を読み込み、比較軸を整理する
6. `critique-panel` を読み込み、出力した論点・結論に対して反証・批判的視点を加える
7. `success-failure-criteria` を読み込み、判断の成功・失敗条件を定義する
8. `decision-materials` を読み込み、最終的な判断材料を整理して出力する
9. 最終判断は人間に委ねる

## 出力の優先度

- 全 Skill を適用する必要はない。問いの性質に応じて必要な Skill のみ適用する
- 「どの Skill を適用したか / しなかったか」を冒頭に明示する
- 適用しなかった Skill の理由を1行で記載する

## Guardrails

- 答えを出さない。判断材料を揃えることに徹する
- 前提が不足している場合は推測せず、不足を明示して止まる
- 全 Skill を機械的に適用しない（問いに不要な Skill は省く）
