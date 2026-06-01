# 使用例 — search.py でのキーワード検索

_`src/lab-core/scripts/search.py` の使い方を示す例です。_

---

## 基本的な使い方

```powershell
# lab-skills/ ディレクトリで実行する

# 全 src/ からキーワード検索
python src/lab-core/scripts/search.py "判断ゲート"

# 特定ディレクトリに絞る
python src/lab-core/scripts/search.py "ROI" --path src/lab-core

# rules ディレクトリだけ検索
python src/lab-core/scripts/search.py "アンチパターン" --tag rules

# JSON/CSV も含めて検索
python src/lab-core/scripts/search.py "価格" --ext .md .json .csv
```

---

## 出力例

```
[検索結果] キーワード: '判断ゲート' — 4 ファイルにマッチ

  src/lab-core/data/glossary.md
    L25: | 判断ゲート | 次フェーズへ進む前に答えるべき Yes/No の問いの集合。... |

  src/lab-core/rules/cost-comparison.md
    L57: - 判断ゲート GATE-4（費用対効果ゲート）: `judgment-gates.md`

  src/lab-core/rules/judgment-gates.md
    L1: # 判断ゲート — lab-core 共通基盤
    L20: ## GATE-2: 自動化判断ゲート

  src/lab-core/templates/skill-template.md
    L71: - `src/lab-core/rules/judgment-gates.md` — 判断ゲートとの整合性
```

---

## 活用シーン

| シーン | コマンド例 |
|--------|-----------|
| 戦略レビュー前の関連情報収集 | `python src/lab-core/scripts/search.py "競争回避"` |
| アンチパターンの確認 | `python src/lab-core/scripts/search.py "AP-" --tag antipatterns` |
| コスト判断基準の参照 | `python src/lab-core/scripts/search.py "ROI" --path src/lab-core` |
