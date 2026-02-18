"""
拡散モデルによる画像生成 — 対話形式アニメーション
================================================

台本: scenes/diffusion_model_script.md

manim render -qm scenes/diffusion_model_animation.py -a
"""

from manim import *
import numpy as np

# ============================================================================
# カラー定数（ホワイトテーマ）
# ============================================================================
BG_COLOR = "#f5f5f5"
TEXT_MAIN = "#1a1a2e"        # メインテキスト（濃紺）
ACCENT_RED = "#d6336c"       # 深めローズ
ACCENT_YELLOW = "#e8590c"    # ディープオレンジ
ACCENT_BLUE = "#1971c2"      # ディープブルー
ACCENT_GREEN = "#099268"     # ディープグリーン
ACCENT_PURPLE = "#7048e8"    # ディープパープル
ACCENT_CYAN = "#0c8599"      # ディープシアン
TEXT_DIM = "#868e96"         # 薄めグレー
CHAR_METAN = "#d6336c"       # めたんの色（ローズピンク）
CHAR_ZUNDA = "#099268"       # ずんだもんの色（ディープグリーン）

# ============================================================================
# ヘルパー関数
# ============================================================================

def get_subtitle(speaker, text, speaker_color=TEXT_MAIN):
    """字幕を返す。話者名（上段）+ セリフ（下段）を中央揃えで配置"""
    name = Text(speaker, font="Noto Sans JP", font_size=20,
                color=speaker_color, weight=BOLD)
    line = Text(text, font="Noto Sans JP", font_size=22, color=TEXT_MAIN)
    content = VGroup(name, line).arrange(DOWN, buff=0.15, center=True)
    bg = RoundedRectangle(
        corner_radius=0.1,
        width=content.get_width() + 0.8, height=content.get_height() + 0.4,
        fill_color=WHITE, fill_opacity=0.85, stroke_color="#dee2e6", stroke_width=1
    )
    bg.move_to(content)
    result = VGroup(bg, content)
    result.to_edge(DOWN, buff=0.3)
    result.set_x(0)
    return result


def show_subtitle(scene, speaker, text, speaker_color=TEXT_MAIN, duration=3.0, prev_sub=None):
    """字幕を表示し、前の字幕があれば消す"""
    sub = get_subtitle(speaker, text, speaker_color)
    anims = [FadeIn(sub, shift=UP * 0.1)]
    if prev_sub is not None:
        anims.append(FadeOut(prev_sub))
    scene.play(*anims, run_time=0.4)
    scene.wait(duration)
    return sub


def get_noise_grid(rows, cols, cell_size=0.35, noise_level=1.0, seed=None):
    """ノイズレベルに応じたグリッドを返す（0=きれい, 1=完全ノイズ）"""
    if seed is not None:
        np.random.seed(seed)
    import colorsys
    grid = VGroup()
    for i in range(rows):
        for j in range(cols):
            base_hue = (i / rows * 0.3 + j / cols * 0.15) % 1.0
            base_sat = 0.6
            base_val = 0.5 + 0.3 * (1 - i / rows)
            noise_hue = np.random.random()
            noise_sat = np.random.random() * 0.3
            noise_val = np.random.random()
            final_hue = base_hue * (1 - noise_level) + noise_hue * noise_level
            final_sat = base_sat * (1 - noise_level) + noise_sat * noise_level
            final_val = base_val * (1 - noise_level) + noise_val * noise_level
            r, g, b = colorsys.hsv_to_rgb(final_hue, final_sat, final_val)
            color = rgb_to_color([r, g, b])
            cell = Square(side_length=cell_size)
            cell.set_fill(color, opacity=1)
            cell.set_stroke(width=0)
            cell.move_to(np.array([j * cell_size, -i * cell_size, 0]))
            grid.add(cell)
    grid.center()
    return grid


def get_box_with_label(text, color, width=2.5, height=0.7, font_size=20):
    """ラベル付きボックスを返す"""
    box = RoundedRectangle(
        corner_radius=0.12, width=width, height=height,
        fill_color=color, fill_opacity=0.2,
        stroke_color=color, stroke_width=2
    )
    label = Text(text, font="Noto Sans JP", font_size=font_size, color=color)
    label.move_to(box)
    return VGroup(box, label)


# ============================================================================
# Scene 01: タイトル (0:00-0:25) 目標 25s
# ============================================================================

class Scene01_Title(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        sub1 = show_subtitle(self, "ずんだもん",
            "最近AIで絵が描けるって聞いたけど、どういう仕組みなの？",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "今日は「拡散モデル」という画像生成AIの心臓部について話そう",
            CHAR_METAN, duration=4, prev_sub=sub1)

        title = Text("拡散モデルによる画像生成",
                     font="Noto Sans JP", font_size=48, color=TEXT_MAIN, weight=BOLD)
        title.shift(UP * 0.8)

        subtitle = Text("Diffusion Models for Image Generation",
                        font_size=24, color=ACCENT_CYAN)
        subtitle.next_to(title, DOWN, buff=0.4)

        line_l = Line(LEFT * 5, LEFT * 0.5, color=ACCENT_RED, stroke_width=2)
        line_r = Line(RIGHT * 0.5, RIGHT * 5, color=ACCENT_RED, stroke_width=2)
        lines = VGroup(line_l, line_r).next_to(subtitle, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.play(Create(line_l), Create(line_r), run_time=0.6)
        self.wait(3)

        self.play(FadeOut(sub2), run_time=0.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 02: 画像生成って何？ (0:25-1:15) 目標 50s
# ============================================================================

class Scene02_WhatIsGeneration(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        sub1 = show_subtitle(self, "ずんだもん",
            "拡散モデル？ 何かが広がっていくイメージ？",
            CHAR_ZUNDA, duration=4)

        sub2 = show_subtitle(self, "めたん",
            "インクを水に落とすと、どんどん広がって均一になるよね？",
            CHAR_METAN, duration=5, prev_sub=sub1)

        # インクの拡散を表現
        center_dot = Dot(ORIGIN + UP * 0.8, radius=0.3,
                        color=ACCENT_BLUE, fill_opacity=0.9)
        self.play(FadeIn(center_dot, scale=0.5), run_time=0.8)

        particles = VGroup()
        np.random.seed(7)
        for _ in range(60):
            angle = np.random.uniform(0, 2 * PI)
            dist = np.random.uniform(0.5, 2.5)
            p = Dot(
                ORIGIN + UP * 0.8 + np.array([np.cos(angle) * dist, np.sin(angle) * dist, 0]),
                radius=0.04, color=ACCENT_BLUE, fill_opacity=0.4
            )
            particles.add(p)

        self.play(
            center_dot.animate.set_opacity(0.1).scale(5),
            LaggedStart(*[FadeIn(p) for p in particles], lag_ratio=0.01),
            run_time=3
        )
        self.wait(1)

        sub3 = show_subtitle(self, "めたん",
            "拡散モデルはこの「広がる」プロセスの逆をやるんだ",
            CHAR_METAN, duration=5, prev_sub=sub2)

        reverse_arrow = Arrow(RIGHT * 2, LEFT * 2, color=ACCENT_YELLOW,
                             stroke_width=3).shift(UP * 0.8)
        reverse_label = Text("逆方向!", font="Noto Sans JP", font_size=22,
                           color=ACCENT_YELLOW, weight=BOLD)
        reverse_label.next_to(reverse_arrow, UP, buff=0.15)
        self.play(GrowArrow(reverse_arrow), FadeIn(reverse_label), run_time=1)
        self.wait(2)

        sub4 = show_subtitle(self, "ずんだもん",
            "え、逆？ バラバラのものを元に戻すってこと？",
            CHAR_ZUNDA, duration=4, prev_sub=sub3)

        sub5 = show_subtitle(self, "めたん",
            "少しずつ戻していく。ここが拡散モデルのミソなんだ",
            CHAR_METAN, duration=6, prev_sub=sub4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 03: 前方過程 (1:15-2:45) 目標 90s
# ============================================================================

class Scene03_ForwardProcess(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 1: 前方過程（Forward Process）",
                       font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "元の画像に少しずつノイズを加えていくプロセスだよ",
            CHAR_METAN, duration=6)

        # ノイズレベル段階の画像
        noise_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
        labels = ["t = 0", "t = 250", "t = 500", "t = 750", "t = 1000"]
        grids = VGroup()
        for nl, lbl in zip(noise_levels, labels):
            grid = get_noise_grid(6, 6, cell_size=0.22, noise_level=nl, seed=42)
            step_label = Text(lbl, font_size=16, color=TEXT_DIM)
            step_label.next_to(grid, DOWN, buff=0.15)
            grids.add(VGroup(grid, step_label))

        grids.arrange(RIGHT, buff=0.4)
        grids.next_to(section, DOWN, buff=0.6)

        self.play(FadeIn(grids[0]), run_time=0.8)
        for i in range(1, len(grids)):
            arrow = Arrow(
                grids[i-1].get_right(), grids[i].get_left(),
                buff=0.1, color=TEXT_DIM, stroke_width=2,
                max_tip_length_to_length_ratio=0.2
            )
            self.play(GrowArrow(arrow), FadeIn(grids[i]), run_time=0.8)
            self.wait(0.5)
        self.wait(1)

        sub2 = show_subtitle(self, "めたん",
            "各ステップで元画像をちょっと薄めて、その分ノイズを足す",
            CHAR_METAN, duration=6, prev_sub=sub1)

        formula = MathTex(
            r"q(x_t | x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1-\beta_t}\, x_{t-1},\, \beta_t \mathbf{I})",
            font_size=32, color=TEXT_MAIN
        )
        formula.to_edge(DOWN, buff=1.8)
        self.play(Write(formula), run_time=2.5)
        self.wait(2)

        sub3 = show_subtitle(self, "めたん",
            "1000回繰り返すと元画像の情報は消えて完全なノイズになる",
            CHAR_METAN, duration=7, prev_sub=sub2)

        overall_arrow = Arrow(grids[0].get_bottom() + DOWN * 0.3,
                             grids[-1].get_bottom() + DOWN * 0.3,
                             color=ACCENT_RED, stroke_width=2)
        arrow_label = Text("元画像 → 完全なノイズ", font="Noto Sans JP",
                          font_size=16, color=ACCENT_RED)
        arrow_label.next_to(overall_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(overall_arrow), FadeIn(arrow_label), run_time=1)
        self.wait(2)

        sub4 = show_subtitle(self, "ずんだもん",
            "わざわざ壊すの？ なんで？",
            CHAR_ZUNDA, duration=4, prev_sub=sub3)

        sub5 = show_subtitle(self, "めたん",
            "壊す過程を記録しておくと「戻す方法」を学べるんだ",
            CHAR_METAN, duration=6, prev_sub=sub4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 04: ニューラルネットワークの学習 (2:45-4:30) 目標 105s
# ============================================================================

class Scene04_Training(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 2: ニューラルネットワークの学習",
                       font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "ノイズだらけの画像から「何のノイズが加わったか」を当てるゲームだ",
            CHAR_METAN, duration=7)

        # 入力 → U-Net → 出力 の図
        noisy_img = get_noise_grid(5, 5, cell_size=0.2, noise_level=0.7, seed=10)
        noisy_img.shift(LEFT * 4 + UP * 0.5)
        noisy_label = Text("ノイズ画像 xt", font="Noto Sans JP", font_size=16, color=TEXT_DIM)
        noisy_label.next_to(noisy_img, DOWN, buff=0.2)
        noisy_group = VGroup(noisy_img, noisy_label)

        t_label = get_box_with_label("t = 500", ACCENT_YELLOW, width=1.5, height=0.5, font_size=16)
        t_label.next_to(noisy_group, DOWN, buff=0.3)

        unet = get_box_with_label("U-Net", ACCENT_PURPLE, width=2.5, height=1.2, font_size=26)
        unet.move_to(UP * 0.5)

        pred_noise = get_noise_grid(5, 5, cell_size=0.2, noise_level=1.0, seed=99)
        pred_noise.shift(RIGHT * 4 + UP * 0.5)
        pred_label = MathTex(r"\hat{\varepsilon}", font_size=32, color=ACCENT_YELLOW)
        pred_text = Text("予測ノイズ", font="Noto Sans JP", font_size=16, color=TEXT_DIM)
        pred_label.next_to(pred_noise, DOWN, buff=0.2)
        pred_text.next_to(pred_label, DOWN, buff=0.1)
        pred_group = VGroup(pred_noise, pred_label, pred_text)

        arr1 = Arrow(noisy_group.get_right(), unet.get_left(), buff=0.2,
                     color=TEXT_DIM, stroke_width=2)
        arr2 = Arrow(unet.get_right(), pred_group.get_left(), buff=0.2,
                     color=TEXT_DIM, stroke_width=2)

        self.play(FadeIn(noisy_group), FadeIn(t_label), run_time=1)
        self.wait(1)
        self.play(GrowArrow(arr1), FadeIn(unet), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arr2), FadeIn(pred_group), run_time=1)
        self.wait(1)

        sub2 = show_subtitle(self, "ずんだもん",
            "ノイズを当てる？",
            CHAR_ZUNDA, duration=3, prev_sub=sub1)

        sub3 = show_subtitle(self, "めたん",
            "ネットワークにノイズ画像とステップtを渡して、ノイズを予測させる",
            CHAR_METAN, duration=7, prev_sub=sub2)

        sub4 = show_subtitle(self, "めたん",
            "実際に加えたノイズと予測の差を最小にするよう学習する",
            CHAR_METAN, duration=6, prev_sub=sub3)

        loss = MathTex(
            r"\mathcal{L} = \| \varepsilon - \hat{\varepsilon} \|^2",
            font_size=36, color=ACCENT_YELLOW
        )
        loss.to_edge(DOWN, buff=1.8)
        loss_box = SurroundingRectangle(loss, buff=0.15, color=ACCENT_YELLOW, stroke_width=1.5)
        self.play(Write(loss), Create(loss_box), run_time=2)
        self.wait(2)

        sub5 = show_subtitle(self, "ずんだもん",
            "正解が分かってるから学習できるんだ！ 自分でノイズを加えたもんね",
            CHAR_ZUNDA, duration=6, prev_sub=sub4)

        sub6 = show_subtitle(self, "めたん",
            "そう！ 自分でノイズを加えたから正解を知っている。これが美しいところだ",
            CHAR_METAN, duration=7, prev_sub=sub5)

        insight = Text("自作自演で学習データを無限に作れる！",
                       font="Noto Sans JP", font_size=20, color=ACCENT_GREEN, weight=BOLD)
        insight.next_to(loss_box, DOWN, buff=0.4)
        self.play(FadeIn(insight), run_time=0.8)
        self.wait(3)

        sub7 = show_subtitle(self, "ずんだもん",
            "でも全部のステップで学習するの？ 大変じゃない？",
            CHAR_ZUNDA, duration=5, prev_sub=sub6)

        sub8 = show_subtitle(self, "めたん",
            "毎回ランダムにステップtを選んで学習する。どのtにも対応できるように",
            CHAR_METAN, duration=7, prev_sub=sub7)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 05: 逆過程 (4:30-6:15) 目標 105s
# ============================================================================

class Scene05_ReverseProcess(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 3: 逆過程 — 画像を生み出す",
                       font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "学習が終わったら画像生成だ。完全なランダムノイズから始める",
            CHAR_METAN, duration=6)

        # 段階的なデノイジング
        steps = [1.0, 0.75, 0.5, 0.25, 0.0]
        step_labels = ["xT", "x750", "x500", "x250", "x0"]

        grids = VGroup()
        for nl, sl in zip(steps, step_labels):
            g = get_noise_grid(6, 6, cell_size=0.22, noise_level=nl, seed=42)
            lbl = Text(sl, font_size=14, color=TEXT_DIM)
            lbl.next_to(g, DOWN, buff=0.1)
            grids.add(VGroup(g, lbl))

        grids.arrange(RIGHT, buff=0.5)
        grids.next_to(section, DOWN, buff=0.6)

        self.play(FadeIn(grids[0]), run_time=1)
        self.wait(1)

        sub2 = show_subtitle(self, "ずんだもん",
            "このグチャグチャから絵ができるの？",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        sub3 = show_subtitle(self, "めたん",
            "予測ノイズを引き算すると、少しだけきれいになる。これを繰り返す",
            CHAR_METAN, duration=5, prev_sub=sub2)

        for i in range(1, len(grids)):
            unet_mini = Text("U-Net", font_size=10, color=ACCENT_PURPLE)
            arrow = Arrow(
                grids[i-1].get_right(), grids[i].get_left(),
                buff=0.08, color=ACCENT_PURPLE, stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            unet_mini.next_to(arrow, UP, buff=0.05)
            self.play(
                GrowArrow(arrow), FadeIn(unet_mini), FadeIn(grids[i]),
                run_time=1.2
            )
            self.wait(1)

        final_rect = SurroundingRectangle(grids[-1], buff=0.08,
                                          color=ACCENT_GREEN, stroke_width=2.5)
        self.play(Create(final_rect), run_time=0.5)
        self.wait(1)

        sub4 = show_subtitle(self, "ずんだもん",
            "だんだん絵になってきた！ まるで霧が晴れていくみたい",
            CHAR_ZUNDA, duration=5, prev_sub=sub3)

        sub5 = show_subtitle(self, "めたん",
            "最初は構図や色が決まり、後半で細かいディテールが浮かび上がる",
            CHAR_METAN, duration=7, prev_sub=sub4)

        coarse_label = Text("粗い構図", font="Noto Sans JP", font_size=14, color=ACCENT_CYAN)
        fine_label = Text("精密なディテール", font="Noto Sans JP", font_size=14, color=ACCENT_GREEN)
        coarse_label.next_to(grids[1], DOWN, buff=0.5)
        fine_label.next_to(grids[-1], DOWN, buff=0.5)
        self.play(FadeIn(coarse_label), FadeIn(fine_label), run_time=0.8)
        self.wait(2)

        sub6 = show_subtitle(self, "ずんだもん",
            "でも同じノイズから始めたら毎回同じ絵にならない？",
            CHAR_ZUNDA, duration=5, prev_sub=sub5)

        sub7 = show_subtitle(self, "めたん",
            "スタートのノイズが毎回ランダムだから、無限のバリエーションが生まれる",
            CHAR_METAN, duration=7, prev_sub=sub6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 06: テキスト条件付け (6:15-7:45) 目標 90s
# ============================================================================

class Scene06_TextConditioning(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 4: テキストで画像を操る",
                       font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "ずんだもん",
            "「猫の絵を描いて」って指定できるよね？ どうやるの？",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "プロンプトをまず数値ベクトルに変換する。テキスト条件付けだ",
            CHAR_METAN, duration=6, prev_sub=sub1)

        # テキスト → エンコーダ → ベクトル
        prompt_text = Text("「夕焼けの中を歩く猫」", font="Noto Sans JP",
                          font_size=22, color=TEXT_MAIN)
        prompt_text.shift(LEFT * 3.5 + UP * 1.2)

        encoder_box = get_box_with_label("テキスト\nエンコーダ", ACCENT_CYAN,
                                         width=2.0, height=0.9, font_size=16)
        encoder_box.next_to(prompt_text, RIGHT, buff=0.8)

        vec_cells = VGroup()
        np.random.seed(77)
        for i in range(6):
            val = np.random.uniform(-1, 1)
            cell = Square(side_length=0.3)
            cell.set_fill(
                ManimColor(ACCENT_CYAN) if val >= 0 else ManimColor(ACCENT_RED),
                opacity=abs(val)
            )
            cell.set_stroke(GREY_B, 0.5)
            vec_cells.add(cell)
        vec_cells.arrange(DOWN, buff=0.02)
        vec_cells.next_to(encoder_box, RIGHT, buff=0.8)
        vec_label = Text("テキスト\nベクトル", font="Noto Sans JP",
                        font_size=14, color=TEXT_DIM)
        vec_label.next_to(vec_cells, DOWN, buff=0.15)

        arr1 = Arrow(prompt_text.get_right(), encoder_box.get_left(),
                     buff=0.15, color=TEXT_DIM, stroke_width=2)
        arr2 = Arrow(encoder_box.get_right(), vec_cells.get_left(),
                     buff=0.15, color=TEXT_DIM, stroke_width=2)

        self.play(FadeIn(prompt_text), run_time=0.8)
        self.play(GrowArrow(arr1), FadeIn(encoder_box), run_time=1)
        self.play(GrowArrow(arr2), FadeIn(vec_cells), FadeIn(vec_label), run_time=1)
        self.wait(1)

        sub3 = show_subtitle(self, "めたん",
            "この情報をノイズ除去のたびにネットワークに渡すんだ",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 下部にU-Netの図
        noisy_box = get_box_with_label("ノイズ画像", GREY_B, width=2, height=0.6, font_size=16)
        noisy_box.shift(LEFT * 3 + DOWN * 1.0)

        unet = get_box_with_label("U-Net", ACCENT_PURPLE, width=2.5, height=1.0, font_size=22)
        unet.shift(DOWN * 1.0)

        result_box = get_box_with_label("きれいな画像", ACCENT_GREEN, width=2, height=0.6, font_size=16)
        result_box.shift(RIGHT * 3 + DOWN * 1.0)

        arr3 = Arrow(noisy_box.get_right(), unet.get_left(), buff=0.15,
                     color=TEXT_DIM, stroke_width=2)
        arr4 = Arrow(vec_cells.get_bottom(), unet.get_top(), buff=0.15,
                     color=ACCENT_CYAN, stroke_width=2)
        arr5 = Arrow(unet.get_right(), result_box.get_left(), buff=0.15,
                     color=TEXT_DIM, stroke_width=2)

        text_arrow_label = Text("テキスト情報", font="Noto Sans JP",
                               font_size=14, color=ACCENT_CYAN)
        text_arrow_label.next_to(arr4, RIGHT, buff=0.1)

        self.play(
            FadeIn(noisy_box), GrowArrow(arr3),
            FadeIn(unet),
            GrowArrow(arr4), FadeIn(text_arrow_label),
            GrowArrow(arr5), FadeIn(result_box),
            run_time=2
        )
        self.wait(1)

        sub4 = show_subtitle(self, "ずんだもん",
            "カーナビみたいに「こっちに進め」って方向を教えてくれる感じ？",
            CHAR_ZUNDA, duration=5, prev_sub=sub3)

        sub5 = show_subtitle(self, "めたん",
            "テキストあり/なし両方で予測し、テキスト方向を強調するんだ",
            CHAR_METAN, duration=6, prev_sub=sub4)

        # ガイダンススケールの図
        self.play(*[FadeOut(m) for m in self.mobjects if m != sub5], run_time=0.5)

        scale_title = Text("ガイダンススケール", font="Noto Sans JP",
                          font_size=26, color=ACCENT_YELLOW, weight=BOLD)
        scale_title.to_edge(UP, buff=0.8)
        self.play(FadeIn(scale_title), run_time=0.5)

        low_label = Text("スケール: 低い", font="Noto Sans JP",
                        font_size=18, color=TEXT_DIM)
        high_label = Text("スケール: 高い", font="Noto Sans JP",
                         font_size=18, color=TEXT_DIM)
        low_desc = Text("自由度高い\n指示から外れることも", font="Noto Sans JP",
                       font_size=16, color=ACCENT_CYAN)
        high_desc = Text("テキストに忠実\n多様性は減る", font="Noto Sans JP",
                        font_size=16, color=ACCENT_YELLOW)

        low_group = VGroup(low_label, low_desc).arrange(DOWN, buff=0.3)
        high_group = VGroup(high_label, high_desc).arrange(DOWN, buff=0.3)
        comparison = VGroup(low_group, high_group).arrange(RIGHT, buff=3.0)
        comparison.next_to(scale_title, DOWN, buff=0.8)

        arrow_scale = Arrow(low_group.get_right(), high_group.get_left(),
                           buff=0.3, color=TEXT_DIM, stroke_width=2)

        self.play(FadeIn(low_group), FadeIn(high_group),
                 GrowArrow(arrow_scale), run_time=1.5)

        sub6 = show_subtitle(self, "めたん",
            "ガイダンススケールで影響度を調整できるよ",
            CHAR_METAN, duration=6, prev_sub=sub5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 07: 潜在拡散モデル (7:45-9:15) 目標 90s
# ============================================================================

class Scene07_LatentDiffusion(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 5: 潜在空間での高速化",
                       font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "ずんだもん",
            "512x512の画像を1000ステップ処理って、めちゃくちゃ遅そう",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "初期の拡散モデルは非常に遅かった。そこで登場したのが潜在拡散モデルだ",
            CHAR_METAN, duration=7, prev_sub=sub1)

        # パイプライン図
        img_input = get_noise_grid(6, 6, cell_size=0.2, noise_level=0.0, seed=42)
        img_input.shift(LEFT * 5.5 + UP * 0.5)
        img_label = Text("512 x 512", font_size=14, color=TEXT_DIM)
        img_label.next_to(img_input, DOWN, buff=0.15)

        encoder = get_box_with_label("エンコーダ", ACCENT_CYAN, width=1.8, height=0.7, font_size=14)
        encoder.shift(LEFT * 2.5 + UP * 0.5)

        latent = get_noise_grid(3, 3, cell_size=0.25, noise_level=0.5, seed=42)
        latent.shift(UP * 0.5)
        latent_label = Text("64 x 64", font_size=14, color=ACCENT_YELLOW)
        latent_label.next_to(latent, DOWN, buff=0.15)
        latent_box = SurroundingRectangle(VGroup(latent, latent_label), buff=0.15,
                                          color=ACCENT_YELLOW, stroke_width=1.5)
        latent_title = Text("潜在空間", font="Noto Sans JP", font_size=14,
                           color=ACCENT_YELLOW)
        latent_title.next_to(latent_box, UP, buff=0.1)

        decoder = get_box_with_label("デコーダ", ACCENT_GREEN, width=1.8, height=0.7, font_size=14)
        decoder.shift(RIGHT * 2.5 + UP * 0.5)

        img_output = get_noise_grid(6, 6, cell_size=0.2, noise_level=0.0, seed=42)
        img_output.shift(RIGHT * 5.5 + UP * 0.5)
        out_label = Text("512 x 512", font_size=14, color=TEXT_DIM)
        out_label.next_to(img_output, DOWN, buff=0.15)

        a1 = Arrow(img_input.get_right(), encoder.get_left(), buff=0.15,
                   color=TEXT_DIM, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(encoder.get_right(), latent.get_left(), buff=0.2,
                   color=TEXT_DIM, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        a3 = Arrow(latent.get_right(), decoder.get_left(), buff=0.2,
                   color=TEXT_DIM, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        a4 = Arrow(decoder.get_right(), img_output.get_left(), buff=0.15,
                   color=TEXT_DIM, stroke_width=2, max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(img_input), FadeIn(img_label), run_time=0.8)
        self.wait(0.5)

        sub3 = show_subtitle(self, "めたん",
            "画像をオートエンコーダで圧縮して、小さな潜在空間に変換する",
            CHAR_METAN, duration=6, prev_sub=sub2)

        self.play(GrowArrow(a1), FadeIn(encoder), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(latent), FadeIn(latent_label),
                 Create(latent_box), FadeIn(latent_title), run_time=1)
        self.wait(1)

        sub4 = show_subtitle(self, "ずんだもん",
            "8分の1！ それは速くなりそう",
            CHAR_ZUNDA, duration=4, prev_sub=sub3)

        diffusion_label = Text("ここで拡散過程", font="Noto Sans JP",
                              font_size=14, color=ACCENT_PURPLE)
        diffusion_label.next_to(latent_box, DOWN, buff=0.3)
        self.play(FadeIn(diffusion_label), run_time=0.5)

        sub5 = show_subtitle(self, "めたん",
            "この小さな空間で拡散するから計算量が劇的に減る",
            CHAR_METAN, duration=6, prev_sub=sub4)

        self.play(GrowArrow(a3), FadeIn(decoder), run_time=0.8)
        self.play(GrowArrow(a4), FadeIn(img_output), FadeIn(out_label), run_time=0.8)
        self.wait(1)

        sub6 = show_subtitle(self, "ずんだもん",
            "画質は落ちないの？",
            CHAR_ZUNDA, duration=4, prev_sub=sub5)

        sub7 = show_subtitle(self, "めたん",
            "オートエンコーダが良ければ劣化なし。これがStable Diffusionの由来だ",
            CHAR_METAN, duration=8, prev_sub=sub6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 08: まとめ (9:15-10:00) 目標 45s
# ============================================================================

class Scene08_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("まとめ", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "全体の流れをおさらいしよう",
            CHAR_METAN, duration=3)

        # 5つのステップ
        steps_data = [
            ("1. 前方過程", "画像にノイズを加えて壊す", ACCENT_BLUE),
            ("2. 学　　習", "ネットワークがノイズを予測する訓練", ACCENT_PURPLE),
            ("3. 逆 過 程", "ノイズから少しずつ画像を生成", ACCENT_GREEN),
            ("4. テキスト", "プロンプトで生成方向をガイド", ACCENT_CYAN),
            ("5. 潜在空間", "圧縮空間で高速化", ACCENT_YELLOW),
        ]

        step_groups = VGroup()
        for label, desc, color in steps_data:
            step_label = Text(label, font="Noto Sans JP", font_size=22,
                             color=color, weight=BOLD)
            step_desc = Text(desc, font="Noto Sans JP", font_size=18, color=TEXT_DIM)
            step_desc.next_to(step_label, RIGHT, buff=0.4)
            step_groups.add(VGroup(step_label, step_desc))

        step_groups.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        step_groups.next_to(section, DOWN, buff=0.6)

        for i, group in enumerate(step_groups):
            self.play(
                FadeIn(group, shift=LEFT * 0.2),
                *(step_groups[j].animate.set_opacity(0.4) for j in range(i)),
                run_time=0.8
            )
            self.wait(0.8)

        self.play(*[g.animate.set_opacity(1) for g in step_groups], run_time=0.5)
        self.wait(1)

        sub2 = show_subtitle(self, "ずんだもん",
            "壊すことで作り方を学ぶって、なんだか禅みたいだね",
            CHAR_ZUNDA, duration=5, prev_sub=sub1)

        sub3 = show_subtitle(self, "めたん",
            "壊す過程を知っているからこそ、戻す方法を学べる。これが本質だ",
            CHAR_METAN, duration=6, prev_sub=sub2)

        # 最後のノイズ→画像変換
        self.play(*[FadeOut(m) for m in self.mobjects if m != sub3], run_time=0.5)

        noise_final = get_noise_grid(8, 8, cell_size=0.22, noise_level=1.0, seed=42)
        noise_final.shift(LEFT * 2.5)
        clean_final = get_noise_grid(8, 8, cell_size=0.22, noise_level=0.0, seed=42)
        clean_final.shift(RIGHT * 2.5)
        final_arrow = Arrow(noise_final.get_right(), clean_final.get_left(),
                           buff=0.3, color=ACCENT_YELLOW, stroke_width=3)
        final_label = Text("拡散モデル", font="Noto Sans JP",
                          font_size=20, color=ACCENT_YELLOW)
        final_label.next_to(final_arrow, UP, buff=0.15)

        self.play(FadeIn(noise_final), run_time=0.8)
        self.play(GrowArrow(final_arrow), FadeIn(final_label), run_time=1)
        self.play(FadeIn(clean_final), run_time=0.8)

        sub4 = show_subtitle(self, "ずんだもん",
            "ありがとう！ イメージ掴めた気がする",
            CHAR_ZUNDA, duration=4, prev_sub=sub3)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
