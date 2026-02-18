# 🎬 Manim Animation Projects

Antigravity と Manim (Community Edition) を使用して、高品質な解説アニメーションを作成するためのプロジェクトリポジトリです。
3Blue1Brown スタイルの美しい数学・科学・経済解説動画を効率的に制作するワークフローを提供します。

## ✨ 特徴

- **プロジェクトベース管理**: アニメーションごとに専用ディレクトリ (`projects/`) でコードと台本を管理。
- **並列レンダリング**: `tools/render_parallel.py` を使用して、複数シーンを同時に高速レンダリング。
- **自動結合**: レンダリング完了後、FFmpeg を使って全シーンを一本の動画 (`outputs/`) に自動結合。
- **AIエージェント対応**: Antigravity エージェントが構成案、台本、コード作成をサポート。

## 📁 ディレクトリ構造

```
manim/
├── projects/                 # アニメーションプロジェクト
│   ├── tokyo_analysis/       # 例: 東京一極集中解説
│   │   ├── animation.py      # Manim コード
│   │   ├── script.md         # 台本・構成案
│   │   └── media/            # 中間生成ファイル (gitignored)
│   └── ...
├── outputs/                  # 完成した動画ファイル (.mp4)
├── tools/                    # ユーティリティスクリプト
│   └── render_parallel.py    # 並列レンダリング & 結合ツール
├── reference/                # 参考資料
│   ├── style_guide.md        # デザイン・配色ガイド
│   └── 3b1b_patterns.md      # 3b1bスタイル実装パターン
├── .agent/                   # エージェント設定
│   └── skills/               # エージェント用スキル (Layout Guideなど)
└── README.md
```

## 🚀 使い方

### 1. 新しいプロジェクトの作成
`projects/` ディレクトリ配下に新しいフォルダを作成し、`animation.py` と `script.md` を用意します。

```bash
mkdir projects/my_new_topic
# animation.py と script.md を作成
```

### 2. アニメーションコードの作成
`animation.py` に Manim コードを記述します。
各シーンは `Scene` クラスとして実装します。

**注意点**:
- 日本語フォントは `font="Noto Sans JP"` などを指定。
- レイアウトは `.agent/skills/manim_presentation_layout/SKILL.md` のガイドラインに従ってください（上部・下部のセーフエリアを確保）。

### 3. レンダリングと結合
`render_parallel.py` スクリプトを使用して、プロジェクト内の全シーンをレンダリングし、結合します。

```bash
# プロジェクト全体をレンダリング (デフォルト品質: -qm / 720p30)
python tools/render_parallel.py my_new_topic

# 高画質でレンダリング (-qh / 1080p60)
python tools/render_parallel.py my_new_topic -q -qh

# 特定のシーンのみレンダリング
python tools/render_parallel.py my_new_topic -s Scene01_Intro Scene02_Body
```

レンダリングが完了すると、自動的に結合コマンドが表示されます（または実行されます）。
完成した動画は `outputs/my_new_topic.mp4` に保存されます。

## 🛠️ 環境構築

1. **前提条件**:
   - Python 3.10+
   - FFmpeg (パスが通っていること)
   - LaTeX (オプション: 数式表示用)

2. **インストール**:
   ```bash
   pip install manim
   # その他必要なライブラリがあれば projects/*/requirements.txt 等を参照
   ```

## 📚 ガイドライン

### デザイン
- **カラーパレット**: `reference/style_guide.md` を参照。
- **レイアウト**: 上部タイトル、下部字幕と被らないように、メインコンテンツは画面中央 (`UP*1.0` 〜 `DOWN*1.0`) に配置することを推奨。

### エージェントスキル
`.agent/skills/manim_presentation_layout/SKILL.md` には、レイアウト崩れを防ぐためのアンチパターン集がまとまっています。

## 📝 ライセンス
このリポジトリのコードは、特に指定がない限り MIT ライセンスの下で公開されています。
生成された動画コンテンツの権利は制作者に帰属します。
