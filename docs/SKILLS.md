# Skill カタログ — 全スキル索引

_このファイルは自動生成です。直接編集しないでください。_
_更新: `python src/lab-core/scripts/gen_catalog.py` / 検査: `--check`（CI）。_

収録: **6 プラグイン / 41 スキル**

## lab-automation-architecture（7）

| Skill | 説明 |
|---|---|
| [`agmsg`](../lab-automation-architecture/skills/agmsg/SKILL.md) | Claude Code と Codex (や他の CLI エージェント) を共有 SQLite メールボックスで直接メッセージ連携させ、人間がAI間でコピペを往復する作業を消す。2台のエージェントで実装役・レビュー役を分担する時、片方の出力をもう片方へ手作業で運んでいる時、エージェント間ハンドオフを自動化したい時に使う。upstream は fujibee/agmsg (MIT)。 |
| [`automation-feasibility`](../lab-automation-architecture/skills/automation-feasibility/SKILL.md) | 手動で行っている作業・プロセスを自動化できるか、すべきかを判断する。自動化コストと人的コストを比較し、ROI・リスク・依存性を整理する。自動化を検討し始めた段階で使う。 |
| [`failure-point-review`](../lab-automation-architecture/skills/failure-point-review/SKILL.md) | 自動化フロー・システム統合の障害点を体系的に列挙し、影響度・検知可能性・対応方針を整理する。実装前・リリース前の最終チェックで使う。 |
| [`manual-vs-automation-cost`](../lab-automation-architecture/skills/manual-vs-automation-cost/SKILL.md) | 手動運用と自動化の総コストを比較し、ROI・回収期間・損益分岐点を算出する。自動化の優先度と規模を決める判断材料を提供する。自動化の優先度・規模を決める前に使う。 |
| [`monitoring-alert-design`](../lab-automation-architecture/skills/monitoring-alert-design/SKILL.md) | 自動化フロー・システムの監視項目とアラート条件を設計する。障害を早期に検知し、適切な人間へ通知が届く仕組みを確定する。自動化フローのリリース前に使う。 |
| [`retry-idempotency-check`](../lab-automation-architecture/skills/retry-idempotency-check/SKILL.md) | 自動化フロー・API 呼び出しのリトライ設計とべき等性を確認する。同じ処理が複数回実行された場合に、データ破損・二重決済・重複挿入が起きないかを検証する。リトライ・再実行を伴う処理の設計時に使う。 |
| [`trigger-action-map`](../lab-automation-architecture/skills/trigger-action-map/SKILL.md) | 自動化フローのトリガー・アクション・条件分岐・エラー処理を可視化する。n8n / Webhook / cron 等の実装前に、フロー全体の抜け漏れを確認する。 |

## lab-communication-translation（6）

| Skill | 説明 |
|---|---|
| [`knowledge-capture`](../lab-communication-translation/skills/knowledge-capture/SKILL.md) | セッション内の判断・却下理由・前提変化・学びを、DECISIONS.md / ADR / CONTEXT.md に書き込める構造化草稿に変換する。Obsidian への直接書き込みや情報の正誤判断はスコープ外。セッションの判断・学びを記録に残すときに使う。 |
| [`llm-portability-review`](../lab-communication-translation/skills/llm-portability-review/SKILL.md) | ドキュメント・プロンプト・スキル定義が、Claude 以外のLLM（GPT-4o / Gemini / Codex 等）でも意図通りに動作するかを評価する。Claude 固有の解釈・暗黙前提・スタイル依存を検出し、移植耐性を高める改善案を提示する。他LLMへ移植する前に使う。 |
| [`onboarding-readability`](../lab-communication-translation/skills/onboarding-readability/SKILL.md) | ドキュメント・README・設計記録が、初めて読む人（人間またはAI）にとって理解可能かを評価する。前提知識・用語定義・構造・導線の欠落を検出し、改善点を提示する。ドキュメントを公開・共有する前に使う。 |
| [`reusable-doc-structure`](../lab-communication-translation/skills/reusable-doc-structure/SKILL.md) | ドキュメントの構造が、目的・読み手・更新頻度の変化に対して再利用・転用できる設計になっているかを評価・設計する。一度書いて終わりではなく、継続して使えるドキュメント設計を目指す。繰り返し使うドキュメントを設計するときに使う。 |
| [`stakeholder-translation`](../lab-communication-translation/skills/stakeholder-translation/SKILL.md) | 技術的な実装内容・判断・リスクを、非エンジニアのステークホルダーが理解できる言葉に変換する。「何が起きているか」「何が必要か」「何を決めてほしいか」を明確に伝える。非エンジニアへ報告・説明するときに使う。 |
| [`summary-structuring`](../lab-communication-translation/skills/summary-structuring/SKILL.md) | 長文の技術ドキュメント・会話ログ・実装結果を、目的に応じた構造で要約する。情報の抜け漏れを防ぎつつ、読み手が必要な情報に即座にアクセスできる形式にする。長文を要約・構造化するときに使う。 |

## lab-data-auth-ops（6）

| Skill | 説明 |
|---|---|
| [`access-control-matrix`](../lab-data-auth-ops/skills/access-control-matrix/SKILL.md) | ロール × リソース × 操作のアクセス制御マトリクスを体系的に設計し、権限の抜け漏れ・過剰付与を一覧で点検する。ロール設計やRBAC/行レベル権限を整理するときに使う。 |
| [`audit-log-design`](../lab-data-auth-ops/skills/audit-log-design/SKILL.md) | 「誰が・いつ・何をしたか」を後から追跡できる監査ログを設計する。重要操作・権限変更・データアクセスを記録する仕組みを決める前に使う。 |
| [`auth-boundary-check`](../lab-data-auth-ops/skills/auth-boundary-check/SKILL.md) | 認証・認可の境界（誰が・何に・どの条件でアクセスできるか）が、想定通りで漏れがないかを確認する。認証/権限の設計・変更の前に使う。 |
| [`data-model-review`](../lab-data-auth-ops/skills/data-model-review/SKILL.md) | データモデル・スキーマ設計が、要件・整合性・拡張性・権限境界に対して妥当かをレビューする。テーブル設計やスキーマ変更の前に使う。 |
| [`pii-handling-review`](../lab-data-auth-ops/skills/pii-handling-review/SKILL.md) | 個人情報（PII）の収集・保存・利用・開示・削除が、最小化と保護の原則に沿っているかをレビューする。PII を扱う機能の設計・公開の前に使う。 |
| [`rollback-readiness`](../lab-data-auth-ops/skills/rollback-readiness/SKILL.md) | データ層の変更（マイグレーション・一括更新・削除）を、失敗時に安全に戻せる状態かを確認する。スキーマ変更やデータ移行を実行する前に使う。 |

## lab-implementation-flow（7）

| Skill | 説明 |
|---|---|
| [`change-impact-scan`](../lab-implementation-flow/skills/change-impact-scan/SKILL.md) | コード・DB・設定の変更が波及する範囲を洗い出す。意図しない副作用・破壊的変更・依存箇所を実装前に特定する。 |
| [`cursor-handoff`](../lab-implementation-flow/skills/cursor-handoff/SKILL.md) | implementation-gate 通過後の情報を、施工AI（Cursor 等）が実行可能な指示書形式に変換する。ゲート通過前には使わない。 |
| [`implementation-gate`](../lab-implementation-flow/skills/implementation-gate/SKILL.md) | 実装に入ってよい状態かを確認する。要件・設計・影響範囲・ロールバック方針が揃っているかを一括チェックし、不足があれば実装ブロックを宣言する。実装着手の直前に使う。 |
| [`patch-readiness`](../lab-implementation-flow/skills/patch-readiness/SKILL.md) | 既存システムへのパッチ・ホットフィックス・緊急修正を安全に適用できる状態かを確認する。テスト・バックアップ・ロールバック手段が揃っているかをチェックする。パッチ・ホットフィックスを適用する前に使う。 |
| [`repo-structure-review`](../lab-implementation-flow/skills/repo-structure-review/SKILL.md) | リポジトリのディレクトリ構造・命名規則・ファイル配置が設計原則と整合しているかをレビューする。構造の崩れを早期に検出し、保守コストの増加を防ぐ。リポジトリ構造をレビューするときに使う。 |
| [`rollback-plan`](../lab-implementation-flow/skills/rollback-plan/SKILL.md) | 実装・デプロイ・マイグレーションが失敗した場合に元の状態に戻すための手順を設計する。何を・どの順序で・誰が・どこまで戻すかを事前に定義する。 |
| [`test-scope-definition`](../lab-implementation-flow/skills/test-scope-definition/SKILL.md) | 実装・変更に対して何をどこまでテストすべきかを定義する。テスト種別・対象・優先度・合否基準を整理し、テスト不足による手戻りを防ぐ。テスト計画を立てるときに使う。 |

## lab-strategy-design（7）

| Skill | 説明 |
|---|---|
| [`alternative-comparison`](../lab-strategy-design/skills/alternative-comparison/SKILL.md) | 複数の戦略・施策の選択肢を多軸で比較し、各案の前提・コスト・リスク・撤退容易性を可視化する。方向性を1案に絞る前に使う。 |
| [`competitive-avoidance`](../lab-strategy-design/skills/competitive-avoidance/SKILL.md) | 正面競争を避け、模倣されにくい差別化・独自ポジションを設計する。レッドオーシャンでの消耗を避けたいときに使う。 |
| [`goal-validation`](../lab-strategy-design/skills/goal-validation/SKILL.md) | 施策・事業の目標（KGI/KPI）が、本来の目的・上位戦略と整合し、測定可能かを検証する。目標を設定・見直す前に使う。 |
| [`pricing-rationale`](../lab-strategy-design/skills/pricing-rationale/SKILL.md) | 価格設定の根拠（価値基準・コスト基準・競合基準）を整理し、値付けの前提とリスクを可視化する。価格を決める・改定する前に使う。 |
| [`scope-design`](../lab-strategy-design/skills/scope-design/SKILL.md) | 事業・施策の戦略的スコープ（どの市場・顧客・課題に集中し、何を捨てるか）を設計する。戦略の的を絞る前に使う。 |
| [`strategy-assessment`](../lab-strategy-design/skills/strategy-assessment/SKILL.md) | 実行中の戦略・施策を、当初前提と実績の差分から査定し、継続・転換・撤退を判断する材料を整える。定期レビューや想定外の結果が出たときに使う。 |
| [`value-proposition-check`](../lab-strategy-design/skills/value-proposition-check/SKILL.md) | 提供価値が、顧客の実在する課題・代替手段に対して本当に刺さるかを検証する。プロダクト・施策の価値仮説を固める前に使う。 |

## lab-thinking-core（8）

| Skill | 説明 |
|---|---|
| [`assumption-audit`](../lab-thinking-core/skills/assumption-audit/SKILL.md) | 設計・仕様・計画に埋め込まれた前提を洗い出し、未検証の前提が判断を歪めていないかを確認する。設計レビュー前、ADR作成前、重要な技術選定前に使う。 |
| [`boundary-check`](../lab-thinking-core/skills/boundary-check/SKILL.md) | 設計・実装・施策のスコープの境界を確認し、やること・やらないこと・後回しにすることを明確にする。スコープクリープを防ぎ、責任境界を明確にする場面で使う。 |
| [`critique-panel`](../lab-thinking-core/skills/critique-panel/SKILL.md) | 提案・設計・計画に対して、複数の異なる視点からの批判的検討を行い、死角と改善余地を可視化する。1人の視点で固まりすぎた判断を揺さぶる場面で使う。 |
| [`decision-materials`](../lab-thinking-core/skills/decision-materials/SKILL.md) | 重要な判断を前に、論点・選択肢・コスト比較・リスク・推奨観点を一枚の判断シートとして整理する。最終判断を人間が下せる状態にする skill。 |
| [`issue-framing`](../lab-thinking-core/skills/issue-framing/SKILL.md) | 曖昧な相談を、論点・目的・成功条件・失敗条件・制約に分解して判断材料を揃える。要件定義前、設計前、壁打ち初動で使う。 |
| [`risk-scan`](../lab-thinking-core/skills/risk-scan/SKILL.md) | 設計・実装・運用の判断に対して、見落としがちなリスクを体系的にスキャンする。実装前・リリース前・大きな方針変更前に使う。 |
| [`success-failure-criteria`](../lab-thinking-core/skills/success-failure-criteria/SKILL.md) | 施策・実装・設計の成功条件と失敗条件を測定可能な形で定義する。「なんとなくうまくいった」を排除し、判断基準を事前に確定する場面で使う。 |
| [`tradeoff-analysis`](../lab-thinking-core/skills/tradeoff-analysis/SKILL.md) | 2つ以上の選択肢が持つトレードオフを多軸で比較し、何を得て何を失うかを明示する。選択肢が出揃った後、決断前に使う。 |
