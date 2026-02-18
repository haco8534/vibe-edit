# 🎬 ManimAI — 3Blue1Brown スタイル自動アニメーション生成

Antigravity のチャットで **「〇〇について説明する動画を作って」** と言うだけで、
3Blue1Brown スタイルの Manim アニメーションを自動生成するプロジェクトです。

## ✨ 使い方

### 1. Antigravity のチャットでテーマを伝える

```
「フーリエ変換について説明する動画を作って」
「ニューラルネットワークの仕組みをアニメーションで見せて」
「固有値の直感的な説明動画を作成して」
```

### 2. エージェントが自動で動画を作成

エージェント（AI）が以下を自動で行います：

1. **構成設計** — テーマに合ったシーン構成を考える
2. **コード作成** — `scenes/` に Manim コードを書く
3. **レンダリング** — `manim render` で動画を生成
4. **エラー修正** — もしエラーが出たら自動で修正

### 3. 動画が完成

レンダリングされた動画は `media/videos/` に出力されます。

## 📁 プロジェクト構成

```
manim/
├── .agent/
│   └── workflows/
│       └── create-animation.md   # エージェントのワークフロー定義
├── reference/
│   ├── style_guide.md            # 3Blue1Brownスタイルガイド
│   ├── 3b1b_patterns.md          # 3b1bの実際のコードから抽出したパターン集（CE翻訳版）
│   └── 3b1b_videos/              # 3b1bの実際のソースコード（ManimGL版, gitignored）
│       ├── _2024/transformers/   #   Transformer解説動画のコード
│       ├── _2025/laplace/        #   ラプラス変換動画のコード
│       ├── _2018/fourier.py      #   フーリエ変換動画のコード
│       └── ...                   #   2015〜2026年の全動画コード
├── examples/                     # 参考用サンプルコード
│   ├── fourier.py
│   ├── linear_algebra.py
│   └── 3b1b_patterns.py          # 3b1bパターンのCE実装サンプル（実行可能）
├── scenes/                       # 生成されたアニメーションコード
├── media/                        # レンダリング出力（自動生成）
├── requirements.txt
└── README.md
```

## 📋 前提条件

- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html) がインストール済み
- Manim の依存関係（LaTeX, FFmpeg 等）が揃っている
- Antigravity（AI エージェント搭載 IDE）を使用

```bash
pip install manim
```

## 🎨 カスタマイズ

### 3b1b リファレンスコード
`reference/3b1b_videos/` に 3Blue1Brown の Grant Sanderson が実際に使っている
ソースコード（ManimGL 版）が含まれています。`reference/3b1b_patterns.md` には
これらのパターンを Manim CE で使える形に翻訳した解説があります。

### サンプルコードの追加
`examples/` に高品質な Manim コードを追加すると、
エージェントがそのスタイルを参考にして生成品質が向上します。
特に `3b1b_patterns.py` は 3b1b の実際のパターンを CE で再現したサンプルです。

### スタイルの調整
`reference/style_guide.md` を編集することで、
色やアニメーションスタイルをカスタマイズできます。

### ワークフローの調整
`.agent/workflows/create-animation.md` を編集することで、
エージェントの動作を変更できます。
