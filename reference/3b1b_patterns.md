# 🎬 3Blue1Brown 実践パターン集（Manim CE 向け）

> **出典**: `reference/3b1b_videos/` にある Grant Sanderson の実際のソースコード
>
> 3b1b は ManimGL（`manimlib`）を使用しているが、このドキュメントでは
> Manim Community Edition（`manim`）で使える形に翻訳している。

---

## 目次

1. [構造パターン](#構造パターン)
2. [アニメーション演出パターン](#アニメーション演出パターン)
3. [数学的可視化パターン](#数学的可視化パターン)
4. [テキスト・数式パターン](#テキスト数式パターン)
5. [カメラ・フレームパターン](#カメラフレームパターン)
6. [ManimGL → CE 翻訳チートシート](#manimgl--ce-翻訳チートシート)

---

## 構造パターン

### 1. ヘルパー関数を活用する

3b1b はシーンの外にヘルパー関数を定義し、再利用する。

```python
# ❌ 悪い例: シーン内に全部書く
class MyScene(Scene):
    def construct(self):
        # 100行のコード...

# ✅ 良い例: ヘルパーを分離（3b1b のパターン）
def get_labeled_arrow(start, end, label_text, color=YELLOW, font_size=24):
    """矢印 + ラベルを返すヘルパー"""
    arrow = Arrow(start, end, color=color, stroke_width=3)
    label = Text(label_text, font_size=font_size, color=color)
    label.next_to(arrow, UP, buff=0.1)
    return VGroup(arrow, label)

def get_titled_box(text, color, font_size=36, width=None, height=None, opacity=0.1):
    """タイトル付きボックスを返す（MLWithinDeepL パターン）"""
    title = Text(text, font_size=font_size)
    w = width or title.get_width() + 1.0
    h = height or title.get_height() + 1.0
    box = Rectangle(width=w, height=h)
    box.set_fill(interpolate_color(BLACK, color, opacity), 1)
    box.set_stroke(color, 2)
    title.next_to(box.get_top(), DOWN, buff=MED_SMALL_BUFF)
    result = VGroup(box, title)
    return result
```

### 2. 設計定数をクラス属性で定義

```python
class FourierScene(Scene):
    # 3b1b パターン: CONFIG の代わりにクラス属性
    n_samples = 1000
    frequency = 2.1
    wave_color = YELLOW
    sum_color = GREEN
    equilibrium_height = 1.5

    def construct(self):
        graph = self.get_wave_graph(self.frequency)
        # ...

    def get_wave_graph(self, frequency):
        """シーン固有のヘルパーメソッド"""
        # get_* パターン（3b1b で頻出）
        pass
```

### 3. シーンの構成メソッド分割

```python
class ExplanationScene(Scene):
    def construct(self):
        # 3b1b は construct 内を論理的なセクションに分割する
        # コメントで「# Show initial setup」のようにセクションを示す
        self.show_title()
        self.introduce_concept()
        self.show_formula()
        self.demonstrate_visually()

    def show_title(self):
        # ...
        pass

    def introduce_concept(self):
        # ...
        pass
```

---

## アニメーション演出パターン

### 1. LaggedStart / LaggedStartMap（最重要パターン）

3b1b のコードで最も多用されるパターン。複数要素を時間差で動かす。

```python
# パターン1: 複数要素を時間差でフェードイン
items = VGroup(*[Text(f"Item {i}") for i in range(5)])
items.arrange(DOWN)
self.play(LaggedStartMap(FadeIn, items, shift=0.2 * UP, lag_ratio=0.1, run_time=2))

# パターン2: 異なるアニメーションを時間差で
self.play(LaggedStart(
    FadeIn(title, lag_ratio=0.1),
    GrowArrow(arrow),
    Write(formula),
    lag_ratio=0.3,
    run_time=2
))

# パターン3: 変形を時間差で（DrawBorderThenFill は CE でも使える）
rects = VGroup(*[Rectangle() for _ in range(10)])
self.play(LaggedStart(*(
    DrawBorderThenFill(rect)
    for rect in rects
), lag_ratio=0.02), run_time=1.5)
```

### 2. 段階的な表示と強調（ShowIncreasingSubsets）

```python
# 3b1b パターン: テキストを段階的に表示
words = VGroup(*[Text(w) for w in "This is a sentence".split()])
words.arrange(RIGHT)
self.play(ShowIncreasingSubsets(words, run_time=1))

# 強調して一つずつ見せる
for i, word in enumerate(words):
    rect = SurroundingRectangle(word, buff=0.1, color=YELLOW, stroke_width=2)
    self.play(Create(rect), run_time=0.3)
    self.wait(0.3)
    self.play(FadeOut(rect), run_time=0.2)
```

### 3. TransformFromCopy パターン

元のオブジェクトを残したまま、コピーを変化させる。

```python
# 3b1b 頻出: 元を残してコピーを変形
source_formula = MathTex(r"e^{i\pi}")
target_formula = MathTex(r"-1")
target_formula.next_to(source_formula, DOWN, buff=1)

arrow = Arrow(source_formula, target_formula)
self.play(
    GrowArrow(arrow),
    TransformFromCopy(source_formula, target_formula),
    run_time=1.5
)
```

### 4. SurroundingRectangle で強調

```python
# 3b1b では数式の一部を強調するのに頻繁に使う
formula = MathTex(r"f(x) = ", r"\sin(x)", r" + ", r"\cos(x)")
rect = SurroundingRectangle(formula[1], buff=0.1, color=YELLOW, stroke_width=2)
self.play(Create(rect))
self.wait()
# 別の部分に移動
self.play(rect.animate.surround(formula[3]))
self.wait()
self.play(FadeOut(rect))
```

### 5. time_span による同時アニメーション制御

```python
# 3b1b パターン: 同じ play() 内で異なるタイミング
# CE では lag_ratio や Succession で代替
self.play(
    LaggedStart(
        FadeIn(box, scale=1.2),
        GrowFromCenter(brace),
        FadeIn(brace_text),
        lag_ratio=0.3,
    ),
    run_time=2
)
```

### 6. VShowPassingFlash（線が走るエフェクト）

```python
# 3b1b のアテンション可視化など
arc = Arc(start_angle=0, angle=PI, radius=2, color=YELLOW, stroke_width=3)
self.play(VShowPassingFlash(arc.copy(), time_width=1.5), run_time=2)
```

### 7. Animate で流れるように

```python
# 3b1b パターン: .animate チェーン
self.play(
    title.animate.scale(0.5).to_corner(UL),
    formula.animate.move_to(ORIGIN),
    run_time=1.5
)
```

---

## 数学的可視化パターン

### 1. 色で値を表現（value_to_color パターン）

```python
def value_to_color(value, min_val=-10, max_val=10):
    """値を色にマッピング（3b1b の行列可視化パターン）"""
    alpha = np.clip((value - min_val) / (max_val - min_val), 0, 1)
    if value >= 0:
        return interpolate_color(BLUE_E, BLUE_B, alpha)
    else:
        return interpolate_color(RED_E, RED_B, alpha)
```

### 2. ニューラルネットワーク可視化

```python
def create_neural_network(layer_sizes, neuron_radius=0.15, buff=2.0):
    """3b1b スタイルのニューラルネットワーク図"""
    layers = VGroup()
    for size in layer_sizes:
        layer = VGroup(*[
            Circle(radius=neuron_radius, stroke_color=WHITE, stroke_width=1,
                   fill_color=WHITE, fill_opacity=np.random.random() * 0.8)
            for _ in range(size)
        ]).arrange(DOWN, buff=0.3)
        layers.add(layer)
    layers.arrange(RIGHT, buff=buff)

    connections = VGroup()
    for l1, l2 in zip(layers, layers[1:]):
        for n1 in l1:
            for n2 in l2:
                line = Line(n1.get_center(), n2.get_center(),
                           buff=neuron_radius,
                           stroke_width=np.random.random() * 2,
                           stroke_opacity=np.random.random() * 0.6,
                           stroke_color=value_to_color(np.random.uniform(-10, 10)))
                connections.add(line)

    return VGroup(connections, layers)
```

### 3. グラフの段階的構築

```python
class GraphBuildUp(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=8, y_length=5, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2}
        )

        # 3b1b パターン: まず軸を表示
        self.play(Create(axes), run_time=1)

        # グラフを描画
        graph = axes.plot(lambda x: np.sin(x), color="#e94560", stroke_width=3)
        self.play(Create(graph), run_time=2)

        # 垂直線で値を追跡（3b1b のフーリエ動画パターン）
        x_tracker = ValueTracker(-3)
        v_line = always_redraw(lambda: axes.get_vertical_line(
            axes.c2p(x_tracker.get_value(),
                     np.sin(x_tracker.get_value())),
            color=YELLOW, stroke_width=2
        ))
        dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(),
                     np.sin(x_tracker.get_value())),
            color=YELLOW, radius=0.06
        ))

        self.add(v_line, dot)
        self.play(x_tracker.animate.set_value(3), run_time=4, rate_func=linear)
```

### 4. Brace + ラベルで注釈

```python
# 3b1b 頻出パターン
items = VGroup(*[Square(0.5) for _ in range(5)]).arrange(RIGHT)
brace = Brace(items, DOWN)
brace_text = brace.get_tex(r"\text{5 items}")
self.play(
    GrowFromCenter(brace),
    Write(brace_text),
    run_time=1
)
# Brace を別の要素に移動
new_brace = Brace(items[:3], DOWN)
self.play(brace.animate.become(new_brace))
```

---

## テキスト・数式パターン

### 1. t2c（text-to-color）で変数を色分け

```python
# 3b1b の最も特徴的なパターン
# ManimGL: Tex(formula, t2c={"x": BLUE, "y": RED})
# CE 翻訳:
formula = MathTex(r"f(", r"x", r") = ", r"x", r"^2 + ", r"y")
formula.set_color_by_tex("x", BLUE)
formula.set_color_by_tex("y", RED)

# または手動で
formula[1].set_color(BLUE)  # 1番目の "x"
formula[3].set_color(BLUE)  # 2番目の "x"
formula[5].set_color(RED)   # "y"
```

### 2. TransformMatchingTex（数式の変形）

```python
# 3b1b パターン: 数式の一部を保持しながら変形
eq1 = MathTex(r"f(x)", r"=", r"x^2", r"+", r"3x")
eq2 = MathTex(r"f'(x)", r"=", r"2x", r"+", r"3")

self.play(Write(eq1))
self.wait()
self.play(TransformMatchingTex(eq1, eq2), run_time=2)
```

### 3. テキストブロックの構築

```python
# 3b1b パターン: 段落テキスト
def get_paragraph(words, line_len=40, font_size=36, font="Noto Sans JP"):
    """3b1b の get_paragraph 関数の CE 翻訳"""
    text = ""
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > line_len:
            text += current_line.strip() + "\n"
            current_line = word + " "
        else:
            current_line += word + " "
    text += current_line.strip()
    return Text(text, font=font, font_size=font_size)
```

---

## カメラ・フレームパターン

### 1. カメラのズーム・パン

```python
class CameraMoveScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # 全体を表示してからズームイン
        all_objects = VGroup(...)
        self.play(self.camera.frame.animate.set(width=all_objects.width * 1.5))

        # 特定の部分にフォーカス
        self.play(
            self.camera.frame.animate.set(width=5).move_to(target_obj),
            run_time=2
        )

        # 引きに戻す
        self.play(
            self.camera.frame.animate.set(width=14).move_to(ORIGIN),
            run_time=1.5
        )
```

---

## ManimGL → CE 翻訳チートシート

| ManimGL (3b1b)               | Manim CE                                  |
|------------------------------|-------------------------------------------|
| `from manimlib import *`     | `from manim import *`                     |
| `InteractiveScene`           | `Scene`                                   |
| `Tex(R"...")`                | `MathTex(r"...")`                         |
| `TexText("...")`             | `Tex(r"\text{...}")`                      |
| `OldTexText("...")`          | `Tex(r"\text{...}")`                      |
| `ShowCreation()`             | `Create()`                                |
| `t2c={"x": BLUE}`           | `.set_color_by_tex("x", BLUE)`            |
| `self.frame`                 | `self.camera.frame` (MovingCameraScene)    |
| `frame.reorient(...)`        | `self.camera.frame.animate.move_to(...)`  |
| `frame.add_ambient_rotation` | カスタム updater が必要                     |
| `fix_in_frame()`             | CE では不要（2D のみ）                      |
| `FRAME_WIDTH / FRAME_HEIGHT` | `config.frame_width / config.frame_height`|
| `DecimalMatrix`              | `DecimalMatrix`（CE にもある）              |
| `MobjectMatrix`              | `MobjectMatrix`（CE にもある）              |
| `Broadcast()`                | CE にはない → `AnimationGroup` で代替       |
| `random_bright_color()`      | 自作ヘルパーが必要                          |
| `checkpoint_paste()`         | CE では使えない                             |
| `LabeledArrow`               | 自作クラスで実装                            |
| `set_backstroke()`           | `.set_stroke(BLACK, width, background=True)` |
| `NumberPlane` (3D)           | `NumberPlane()`                            |
| `ThreeDAxes`                 | `ThreeDAxes`（CE にもある）                 |
| `ComplexPlane`               | `ComplexPlane`（CE にもある）                |
| `path_arc=60*DEGREES`        | `path_arc=60*DEGREES`（同じ）               |
| `rate_func=there_and_back`   | `rate_func=there_and_back`（同じ）          |
| `time_span=(0, 2)`           | CE にはない → `LaggedStart` で代替           |

---

## 参考ファイル索引（`reference/3b1b_videos/`）

### 初学者向け（シンプルで読みやすい）
| ファイル | テーマ | 学べるパターン |
|---------|--------|---------------|
| `_2024/transformers/embedding.py` | Transformer埋め込み | テキスト分割、行列可視化、色分け |
| `_2024/transformers/ml_basics.py` | ML基礎 | ボックス図、ネスト構造、ダイヤル |
| `_2024/transformers/helpers.py` | ヘルパー集 | 再利用可能コンポーネント設計 |
| `_2017/nn/` | ニューラルネット | ネットワーク図、重み可視化 |

### 中級者向け（数学的可視化）
| ファイル | テーマ | 学べるパターン |
|---------|--------|---------------|
| `_2018/fourier.py` | フーリエ変換 | 波形、グラフ連動、段階的合成 |
| `_2025/laplace/derivatives.py` | ラプラス変換 | 可換図式、数式変形アニメーション |
| `_2019/diffyq/` | 微分方程式 | ベクトル場、フロー |
| `_2017/eoc/` | 微積分の本質 | 直感的な数学アニメーション |

### 上級者向け（複雑な演出）
| ファイル | テーマ | 学べるパターン |
|---------|--------|---------------|
| `_2024/transformers/attention.py` | アテンション | 大規模アニメーション、VShowPassingFlash |
| `_2018/uncertainty.py` | 不確定性原理 | 3D、波束、確率分布 |
| `_2025/laplace/main_equations.py` | ラプラス変換 | 複素平面、ポール可視化 |

---

## 重要な教訓

### 3b1b のコードから学ぶべきこと

1. **コメントでセクションを区切る**: `# Show initial setup`, `# Transition to next concept`
2. **ヘルパー関数を使い回す**: `get_*` パターンでオブジェクト生成を分離
3. **LaggedStart を多用する**: 同時に動くと「AI っぽい」。時間差が「手作り感」を作る
4. **SurroundingRectangle で注目を誘導**: 説明したい部分を囲んで目を向けさせる
5. **TransformFromCopy で因果関係を示す**: 「AからBが生まれる」を視覚的に
6. **色の一貫性**: 同じ概念には同じ色を使い続ける（`t2c` パターン）
7. **段階的に複雑さを増す**: 一度に全部見せず、少しずつ追加する
8. **wait() を恐れない**: 十分な「間」が理解を助ける
