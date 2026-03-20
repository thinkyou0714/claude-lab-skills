# 使用例 — search.py でのキーワード検索

_`src/lab-core/scripts/search.py` の使い方を示す例です。_

---

## 基本的な使い方

```powershell
# lab-skills/ ディレクトリで実行する

# 全 src/ からキーワード検索
python src/lab-core/scripts/search.py "判断ゲート"

# 特定ディレクトリに絞る
python src/lab-core/scripts/search.py "BtoB" --path src/lab-strategy

# rules ディレクトリだけ検索
python src/lab-core/scripts/search.py "アンチパターン" --tag rules

# JSON/CSV も含めて検索
python src/lab-core/scripts/search.py "価格" --ext .md .json .csv
```

---

## 出力例

```
[検索結果] キーワード: '判断ゲート' — 2 ファイルにマッチ

  src/lab-core/rules/judgment-gates.md
    L1: # 判断ゲート — lab-core 共通基盤
    L15: ## GATE-1: 実装着手ゲート

  src/lab-core/data/glossary.md
    L12: | 判断ゲート | 次フェーズへ進む前に答えるべき Yes/No の問い |
```

---

## 活用シーン

| シーン | コマンド例 |
|--------|-----------|
| 戦略レビュー前の関連情報収集 | `python src/lab-core/scripts/search.py "競争回避"` |
| アンチパターンの確認 | `python src/lab-core/scripts/search.py "AP-" --tag antipatterns` |
| コスト判断基準の参照 | `python src/lab-core/scripts/search.py "ROI" --path src/lab-core` |
