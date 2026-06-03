---
name: agmsg
description: "Claude Code と Codex (や他の CLI エージェント) を共有 SQLite メールボックスで直接メッセージ連携させ、人間がAI間でコピペを往復する作業を消す。2台のエージェントで実装役・レビュー役を分担する時、片方の出力をもう片方へ手作業で運んでいる時、エージェント間ハンドオフを自動化したい時に使う。upstream は fujibee/agmsg (MIT)。"
---

## Purpose

Claude Code ↔ Codex のような 2 つの CLI エージェント間で、人間が「片方の出力をコピーして
もう片方の入力欄に貼る」往復作業を消す。両エージェントが同じ team に属し、共有 SQLite
メールボックス (`messages` テーブル) でメッセージを送受信する。実装は
[fujibee/agmsg](https://github.com/fujibee/agmsg) (MIT) を利用する — この skill はその
**導入・運用・落とし穴の判断**を担う orchestration skill であり、upstream スクリプトの複製ではない。

## Use When

- Claude Code が実装、Codex がレビュー (または難所担当) のような **2 台分担**をしていて、
  指摘・依頼を手作業で往復させている
- エージェント間の依頼/結果ハンドオフを **session をまたいで確実に**届けたい
- 「賢い AI を 2 台並べて、その間を一番アホな作業 (コピペ) を人間がやっている」状態を解消したい
- Windows + Git Bash + Codex CLI 環境で agmsg を入れようとして、sqlite3 不在や表示文字化けで詰まった

**使わない**: 単一エージェントで完結するタスク / リアルタイム双方向音声・ファイル転送
(agmsg はテキストメッセージのみ) / ネットワーク越しの別マシン間連携 (ローカル共有 DB 前提)。

## Inputs

- **エージェント構成**: どの 2 (以上) のエージェントを連携させるか (例: Claude Code=`cc` / Codex=`codex`)
- **team 名**: メッセージを共有するグループ (例: `lab`)
- **連携プロジェクト**: 両エージェントが共同作業する作業ディレクトリ (配信 hook はここに紐づく)
- **配信モード**: `monitor` (Claude Code 専用 real-time) / `turn` (Stop hook、Codex 既定) / `off`
- **OS / shell**: Windows(Git Bash) か macOS/Linux か (落とし穴が変わる)

## Output Contract

1. **論点**: この環境で agmsg を確実に動かすための最大の障害は何か
2. **根拠**: そう判断した理由 (sqlite3 不在 / HOME split / hook 互換性 / 表示エスケープ 等)
3. **セットアップ手順**: 依存導入 → install → identity 登録 → 配信モード設定 の順序
4. **検証結果**: 双方向 round-trip と既読管理が動くことの確認方法
5. **含意**: 配信モード選択が latency / 二重配信に与える影響
6. **改善案 / 代替**: hook が効かない環境での fallback (手動 check) と将来の自動化余地
7. **判断材料**: team 名・identity 名・対象プロジェクトなど人間が決めるべき事項

## Review Lens

- **目的妥当性**: 本当にコピペ往復が起きているか (単発タスクに過剰投入していないか)
- **範囲の過不足**: 連携させるエージェント・プロジェクトの範囲が適切か
- **中長期リスク**: グローバル hook 設定を壊していないか / DB の肥大・既読漏れ
- **LAB 全体との整合性**: 既存の Codex 連携 (codex-hub 等) と衝突していないか
- **非エンジニア理解可能性**: 「2台のAIが直接話す」を説明できるか
- **他LLM移植耐性**: 設定が特定エージェントに過度依存していないか (gemini 等も join 可能か)

## Instructions

1. **依存確認**: `sqlite3` が PATH 上にあるか。無ければ導入 (Windows: `scoop install sqlite`、
   macOS: 標準同梱、Linux: `apt install sqlite3`)。
2. **install**: `bash <(curl -fsSL https://raw.githubusercontent.com/fujibee/agmsg/main/setup.sh)`
   → `~/.agents/skills/agmsg/` + `/agmsg` command + Codex `writable_roots` 追記。
3. **identity 登録**: 各エージェントを team に join。
   `~/.agents/skills/agmsg/scripts/join.sh <team> <name> <type> "<project>"`
   (type = `claude-code` / `codex` / `gemini` / `antigravity`)。
4. **配信モード**: `delivery.sh set monitor claude-code "<project>"` (Claude=real-time) と
   `delivery.sh set turn codex "<project>"` (Codex=ターン境界)。**これはプロジェクト単位の
   hook ファイルに書かれ、グローバル設定は触らない**。
5. **送受信**: `send.sh <team> <from> <to> "<msg>"` / `inbox.sh <team> <agent>` (既読化)。
   エージェント内では Claude `/agmsg`、Codex `$agmsg`。
6. **検証**: cc→codex と codex→cc の round-trip + `inbox` の既読化 + (Codex) Stop hook の
   JSON 注入を確認する。

## Guardrails

- **グローバル hook を壊さない**: Codex の `~/.codex/hooks.json`、Claude の `~/.claude/settings.json`
  hook chain は触らない。agmsg はプロジェクト単位の `.codex/hooks.json` /
  `.claude/settings.local.json` を使う。これらを誤って repo に commit しない (machine-local)。
- **HOME 一貫性**: Windows では全エージェントを Git Bash 側 (`HOME=/c/Users/...`) に統一。WSL 経由が
  混ざると `~`=`/home/...` で **別 DB** になりメッセージが共有されない。
- **Windows sqlite 表示文字化け**: scoop 等の sqlite3 (≥3.49) は出力中の制御文字をエスケープ表示し
  (`char(31)`→可視 `^_`) CRLF を出すため、agmsg の `$'\x1f'` 区切りが壊れ表示が文字化けする
  (配信自体は正常)。tab は raw で通るので表示系 script の区切りを `char(9)` + `IFS=$'\t\r'` に
  置換して解決する。upstream `--update` で剥がれるので再適用すること。
- **Codex 0.130 の turn hook**: 環境により Stop hook が発火しないことがある。その場合は手動
  `$agmsg` を使う (Claude 側 monitor は無関係に動く)。
- 無限リトライ・無制限の DB 成長を放置しない。古いメッセージは定期的に整理する。

## LAB Cross-Check

| 観点 | 状態 | 備考 |
|---|---|---|
| 自動化フロー | — | 既存の Codex 連携 (codex-hub / auto-delegate) と役割が衝突しないか |
| データ / 認証 / ログ | — | DB はローカルのみ・秘匿情報をメッセージに載せないか |
| 実装 / 運用フロー | — | install / delivery 設定が冪等に再現できるか |
| 非エンジニア理解可能性 | — | 「2台のAIが直接メッセージを送り合う」を説明できるか |
| 会員共有 / 再利用耐性 | — | セットアップ手順が他プロジェクト・他マシンに転用できるか |
| 他LLM移植耐性 | — | gemini / antigravity 等も同じ枠組みで join できるか |

状態は OK / 注意 / NG / 対象外 で記入すること。

## Handoff Notes

- **要件**: 2 エージェントが共有メールボックスで送受信でき、人間のコピペ往復が消えた状態
- **成功条件**: 双方向 round-trip + 既読管理が動作 / 対象プロジェクトで配信 hook が有効
- **失敗条件**: メッセージが届かない / 別 DB に書かれて共有されない / 表示が文字化けして読めない
- **実行範囲**: `~/.agents/skills/agmsg/` と **プロジェクト単位**の配信 hook ファイルのみ
- **影響範囲**: グローバル hook には影響させない (させたら設計ミス)
- **ロールバック方針**: `delivery.sh set off` で配信停止、upstream `uninstall.sh` で撤去、
  `config.toml` は `.bak` から復元
- **コスト比較**: セットアップ工数 vs 1 日何十回のコピペ往復・集中力分断のコスト

## Further Reading

- upstream: <https://github.com/fujibee/agmsg> (MIT) / docs <https://agmsg.cc/>
- `trigger-action-map` skill — エージェント間ハンドオフのトリガー・アクション整理
- `failure-point-review` skill — メッセージ未達・hook 不発火の障害設計
- `monitoring-alert-design` skill — 配信失敗・未読滞留の監視設計
