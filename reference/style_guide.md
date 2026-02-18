# 🎨 3Blue1Brown スタイルガイド for Manim

Manim で 3Blue1Brown スタイルの教育アニメーションを作成するためのスタイルガイド。

---

## カラーパレット

### ダーク系背景（推奨）

```python
# 背景色
DARK_BG = "#1a1a2e"       # 深いネイビー（メイン推奨）
DARK_BG_ALT = "#0f0f23"   # より暗い背景
DARK_BG_WARM = "#1e1e2e"  # 温かみのあるダーク

# アクセント・強調色
ACCENT_RED = "#e94560"     # 赤系アクセント（重要な要素）
ACCENT_BLUE = "#0f3460"    # 青系（補助的要素）
ACCENT_YELLOW = "#f5c518"  # 黄色（特に重要な強調）
ACCENT_GREEN = "#2ecc71"   # 緑（正解・成功の意味）
ACCENT_PURPLE = "#9b59b6"  # 紫（第3の要素）
ACCENT_CYAN = "#1abc9c"    # シアン（装飾的要素）

# テキスト色
TEXT_WHITE = "#ffffff"
TEXT_GREY = "#b0b0b0"
TEXT_DIM = "#666666"
```

### 3Blue1Brown 公式カラー

```python
# 3B1B で頻出する色
THREE_BLUE = "#3b82f6"     # メインの青
THREE_BROWN = "#975838"    # メインの茶
GRANT_YELLOW = "#ffff00"   # グラントが使うハイライト黄色
GRANT_GREEN = "#83c167"    # 正の値・成功
GRANT_RED = "#cf5044"      # 負の値・エラー
```

---

## タイポグラフィ

### 日本語テキスト

```python
# 通常テキスト
Text("テキスト", font="Noto Sans JP", font_size=36, color=WHITE)

# タイトル（大きめ）
Text("タイトル", font="Noto Sans JP", font_size=48, color=WHITE, weight=BOLD)

# サブタイトル
Text("補足", font="Noto Sans JP", font_size=24, color="#e94560")

# 説明文
Text("説明テキスト", font="Noto Sans JP", font_size=20, color="#b0b0b0")
```

### 数式（LaTeX）

```python
# 基本の数式
MathTex(r"E = mc^2", font_size=44, color=WHITE)

# 色付き数式
MathTex(r"f(x) = ", r"\sin(x)", font_size=40)
formula[1].set_color("#e94560")

# 行列
MathTex(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}")
```

**注意**: `MathTex` 内に日本語を入れてはいけない。日本語は必ず `Text` を使う。

---

## アニメーション原則

### 1. 出現のアニメーション

```python
# テキスト・数式 → Write がベスト
self.play(Write(formula), run_time=2)

# 図形 → Create
self.play(Create(circle), run_time=1)

# グラフ → Create
self.play(Create(graph), run_time=2)

# フェードイン（シンプルに出す）
self.play(FadeIn(obj), run_time=0.5)
self.play(FadeIn(obj, shift=UP * 0.3), run_time=0.8)  # 方向付き

# 矢印 → GrowArrow
self.play(GrowArrow(arrow), run_time=1)
```

### 2. 変化のアニメーション

```python
# 変形（同じ型のオブジェクト間）
self.play(Transform(old_obj, new_obj), run_time=2)

# 置き換え変形（old_obj を scene から消して new_obj を残す）
self.play(ReplacementTransform(old_obj, new_obj), run_time=2)

# 移動
self.play(obj.animate.shift(RIGHT * 2), run_time=1)
self.play(obj.animate.move_to(ORIGIN), run_time=1)

# スケール
self.play(obj.animate.scale(0.5), run_time=0.8)

# 色変更
self.play(obj.animate.set_color("#e94560"), run_time=0.5)
```

### 3. 強調のアニメーション

```python
# 囲み線で強調（最もよく使う）
self.play(Circumscribe(obj, color="#e94560", run_time=1.5))

# 点滅的な強調
self.play(Indicate(obj, color=YELLOW))

# 下線を引く
underline = Underline(obj, color="#e94560")
self.play(Create(underline))
```

### 4. 消去のアニメーション

```python
# フェードアウト
self.play(FadeOut(obj), run_time=0.5)
self.play(FadeOut(obj, shift=UP), run_time=0.8)

# 全オブジェクトを消去（シーン切り替え時）
self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

# Uncreate（Create の逆再生）
self.play(Uncreate(obj), run_time=1)
```

### 5. テンポ

```python
# 重要な説明の後 — 長めの待ち
self.wait(2)

# 軽い切り替え
self.wait(0.5)

# 数式を表示した後
self.wait(1.5)
```

---

## レイアウトのパターン

### タイトルシーン

```python
class TitleScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        title = Text("メインタイトル", font="Noto Sans JP", font_size=52, color=WHITE)
        subtitle = Text("サブタイトル", font="Noto Sans JP", font_size=28, color="#e94560")
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle), shift=UP), run_time=0.8)
```

### テキスト＋数式の説明シーン

```python
class ExplanationScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 上部に説明テキスト
        explanation = Text(
            "関数の微分は接線の傾きを表す",
            font="Noto Sans JP", font_size=28, color=WHITE
        ).to_edge(UP, buff=0.8)
        
        # 中央に数式
        formula = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            font_size=44, color=WHITE
        )
        
        self.play(Write(explanation), run_time=1.5)
        self.wait(0.5)
        self.play(Write(formula), run_time=2.5)
        self.wait(2)
```

### グラフ＋アニメーション

```python
class GraphScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=5,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        
        # 軸ラベル
        x_label = axes.get_x_axis_label("x", direction=DOWN)
        y_label = axes.get_y_axis_label("y", direction=LEFT)
        
        # グラフ
        graph = axes.plot(lambda x: np.sin(x), color="#e94560", stroke_width=3)
        graph_label = MathTex(r"y = \sin(x)", color="#e94560", font_size=28)
        graph_label.next_to(graph, UR, buff=0.2)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.play(Create(graph), run_time=2)
        self.play(Write(graph_label), run_time=1)
        self.wait(2)
```

### ステップバイステップの解説

```python
class StepByStepScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        steps = [
            "ステップ 1: 問題を定義する",
            "ステップ 2: 式を変形する",
            "ステップ 3: 結果を確認する",
        ]
        
        step_texts = VGroup(*[
            Text(step, font="Noto Sans JP", font_size=28, color=WHITE)
            for step in steps
        ]).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        step_texts.move_to(ORIGIN)
        
        for i, step_text in enumerate(step_texts):
            self.play(Write(step_text), run_time=1)
            self.wait(1)
            if i < len(step_texts) - 1:
                # 表示済みのステップを薄くする
                self.play(step_text.animate.set_opacity(0.4), run_time=0.3)
        
        # 最後に全部を元に戻す
        self.play(*[s.animate.set_opacity(1) for s in step_texts], run_time=0.5)
        self.wait(2)
```

### 比較（左右に並べる）

```python
class ComparisonScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        
        # 左側
        left_title = Text("変換前", font="Noto Sans JP", font_size=28, color="#e94560")
        left_content = MathTex(r"f(x) = x^2", font_size=36)
        left_group = VGroup(left_title, left_content).arrange(DOWN, buff=0.5)
        left_group.shift(LEFT * 3)
        
        # 右側
        right_title = Text("変換後", font="Noto Sans JP", font_size=28, color="#2ecc71")
        right_content = MathTex(r"f'(x) = 2x", font_size=36)
        right_group = VGroup(right_title, right_content).arrange(DOWN, buff=0.5)
        right_group.shift(RIGHT * 3)
        
        # 矢印
        arrow = Arrow(left_group.get_right(), right_group.get_left(), color=WHITE)
        
        self.play(FadeIn(left_group), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(FadeIn(right_group), run_time=1)
        self.wait(2)
```

---

## よくある落とし穴

| 問題 | 原因 | 解決策 |
|------|------|--------|
| 日本語が表示されない | フォント未指定 | `font="Noto Sans JP"` を指定 |
| LaTeX エラー | 日本語を MathTex に入れた | 日本語は Text で、数式は MathTex で |
| オブジェクトが画面外 | 座標超過 | x: -7〜7, y: -4〜4 の範囲内に |
| アニメーションが速すぎる | run_time 未指定 | `run_time=1.5` 等を明示指定 |
| Transform がおかしい | 同じ Mobject を再利用 | `.copy()` でコピーしてから使う |
| 色が見づらい | 明るい背景に薄い色 | ダーク背景 + コントラスト高い色 |

---

## Manim CLI リファレンス

```bash
# 低品質レンダリング（テスト用、高速）
manim render -ql scene_file.py SceneClassName

# 中品質（通常用途）
manim render -qm scene_file.py SceneClassName

# 高品質
manim render -qh scene_file.py SceneClassName

# 4K品質
manim render -qk scene_file.py SceneClassName

# 全シーンをレンダリング
manim render -qm scene_file.py -a

# 最終フレームのみ保存（レイアウト確認用）
manim render -ql -s scene_file.py SceneClassName
```
