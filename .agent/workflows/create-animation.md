---
description: Manimを使って高品質な教育アニメーション動画を作成するワークフロー
---

Manimを使って、ずんだもんやめたんなどのキャラクターが登場する解説動画を作成する手順です。
プロジェクト指向のディレクトリ構造を採用し、台本作成から並列レンダリングまでを効率的に行います。

# 1. プロジェクトのセットアップ

まず、新しいプロジェクト用のフォルダを作成します。
`project_name` は英数字とアンダースコア（例: `api_explanation`, `quantum_mechanics`）を使用してください。

1. `projects/<project_name>` ディレクトリを作成します。
2. プロジェクトのテーマと目的を明確にします。

# 2. 台本の作成

動画の構成案と台本を作成します。
`projects/<project_name>/script.md` というファイルを作成し、以下の構成で記述します。

- **キャラクター設定**: 登場人物と役割（解説役：めたん、聞き手：ずんだもん 等）。
- **シーン構成**: 動画全体の流れをシーンごとに分割（例: Scene01_Intro, Scene02_Concept...）。
- **セリフとアクション**: 対話形式で記述し、画面上の動き（アニメーション）も具体的にメモします。

**Tips:**
- 1本の動画は10分程度を目安にし、シーンを細かく分ける（1シーン1〜2分）と管理しやすいです。
- 専門用語が出るときは、比喩や図解を入れることをルールにします。

# 3. アニメーションコードの実装

`projects/<project_name>/animation.py` を作成し、Manimのコードを実装します。

## 実装のポイント
- **ホワイトテーマ**: 背景 `#f5f5f5`、メインテキスト `#1a1a2e` を基本とします。
- **シーンクラス**: 台本に基づき、`Scene01_Intro` のようにシーンごとにクラスを定義します。
- **字幕システム**: `show_subtitle` などのヘルパー関数を使用して、キャラクターのセリフを表示します。
- **テンプレート**: 既存の `projects/api_explanation/animation.py` などを参考に、ボイラープレートを活用してください。

```python
from manim import *
# ... (カラー定義やヘルパー関数) ...

class Scene01_Intro(Scene):
    def construct(self):
        # ...
```

# 4. 並列レンダリングの実行

汎用レンダリングスクリプトを使用して、全シーンを高速にレンダリングします。

```bash
# プロジェクト名を指定して実行
python tools/render_parallel.py <project_name>

# 特定のシーンだけテストする場合
python tools/render_parallel.py <project_name> -s Scene01_Intro
```

このスクリプトは以下の処理を行います：
1. `animation.py` からシーンを自動検出。
2. 複数のCPUコアを使って並列レンダリング。
3. `outputs/<project_name>/` に動画を出力。
4. 最後に結合用の `ffmpeg` コマンドを表示。

# 5. 動画の結合と確認

スクリプトの最後に表示された `ffmpeg` コマンドを実行して、シーンを1つの動画ファイルに結合します。

例:
```bash
cd "outputs/<project_name>/720p30"
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy "../../../<project_name>.mp4"
```

完成した動画は `outputs/<project_name>.mp4` に保存されます。
内容を確認し、修正が必要な場合は「2. 台本の作成」または「3. アニメーションコードの実装」に戻ります。
