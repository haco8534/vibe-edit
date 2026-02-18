"""
フーリエ変換 — 3Blue1Brown スタイル教育アニメーション

複雑な波がシンプルな正弦波の重ね合わせであることを
直感的に理解させるアニメーション。
"""
from manim import *
import numpy as np


# ── カラーパレット ──────────────────────────────────
BG_COLOR = "#1a1a2e"
ACCENT_RED = "#e94560"
ACCENT_BLUE = "#3b82f6"
ACCENT_YELLOW = "#f5c518"
ACCENT_GREEN = "#2ecc71"
TEXT_GREY = "#b0b0b0"
FONT = "Noto Sans JP"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 1: タイトル
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TitleScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "フーリエ変換", font=FONT, font_size=60, color=WHITE, weight=BOLD,
        )
        subtitle = Text(
            "複雑な波を解きほぐす",
            font=FONT, font_size=28, color=ACCENT_RED,
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1)
        self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle), shift=UP * 0.5), run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 2: 正弦波の紹介
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WaveIntroScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        intro = Text(
            "すべての信号は「波」でできている",
            font=FONT, font_size=28, color=WHITE,
        ).to_edge(UP, buff=0.6)
        self.play(FadeIn(intro), run_time=0.8)

        # 座標軸
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.8, 1.8, 0.5],
            x_length=10, y_length=3.5,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * 0.3)
        t_label = MathTex("t", font_size=28, color=GREY_A).next_to(axes.x_axis, RIGHT, buff=0.15)
        self.play(Create(axes), FadeIn(t_label), run_time=1)

        # 正弦波
        wave = axes.plot(lambda x: np.sin(x), color=ACCENT_RED, stroke_width=3)
        wave_label = MathTex(r"y = \sin(t)", color=ACCENT_RED, font_size=32)
        wave_label.next_to(axes, UP, buff=0.3).shift(RIGHT * 3)

        self.play(Create(wave), run_time=2)
        self.play(FadeIn(wave_label), run_time=0.5)
        self.wait(1)

        # 周波数を変える
        freq_text = Text(
            "周波数を上げると…", font=FONT, font_size=20, color=TEXT_GREY,
        ).next_to(axes, DOWN, buff=0.5)
        self.play(FadeIn(freq_text), run_time=0.5)

        wave_fast = axes.plot(lambda x: np.sin(3 * x), color=ACCENT_BLUE, stroke_width=3)
        wave_fast_label = MathTex(r"y = \sin(3t)", color=ACCENT_BLUE, font_size=32)
        wave_fast_label.next_to(axes, UP, buff=0.3).shift(RIGHT * 3)

        self.play(
            ReplacementTransform(wave, wave_fast),
            ReplacementTransform(wave_label, wave_fast_label),
            run_time=1.5, rate_func=smooth,
        )
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 3: 波の重ね合わせ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WaveSuperpositionScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        header = Text("波の重ね合わせ", font=FONT, font_size=34, color=WHITE)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.6)

        freqs = [1, 3, 5]
        amps = [1.0, 0.5, 0.3]
        colors = [ACCENT_RED, ACCENT_BLUE, ACCENT_YELLOW]

        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2.2, 2.2, 0.5],
            x_length=10, y_length=4, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * 0.4)
        self.play(Create(axes), run_time=0.8)

        # 波を1つずつ追加
        current_sum = lambda x: 0  # noqa: E731
        sum_wave = None
        labels = VGroup()

        for i, (f, a, c) in enumerate(zip(freqs, amps, colors)):
            individual = axes.plot(
                lambda x, freq=f, amp=a: amp * np.sin(freq * x),
                color=c, stroke_width=2, stroke_opacity=0.4,
            )
            label = MathTex(
                f"{a}" + r"\sin(" + f"{f}" + r"t)",
                color=c, font_size=24,
            )
            labels.add(label)

            prev_sum = current_sum
            current_sum = lambda x, ps=prev_sum, freq=f, amp=a: ps(x) + amp * np.sin(freq * x)
            new_sum_wave = axes.plot(current_sum, color=WHITE, stroke_width=3)

            if sum_wave is None:
                self.play(Create(individual), FadeIn(label), run_time=1)
                sum_wave = new_sum_wave
                self.play(Create(sum_wave), run_time=0.8)
            else:
                self.play(Create(individual), FadeIn(label), run_time=0.8)
                self.play(
                    ReplacementTransform(sum_wave, new_sum_wave),
                    run_time=1, rate_func=smooth,
                )
                sum_wave = new_sum_wave
            self.wait(0.5)

        # 凡例
        plus1 = MathTex("+", font_size=24, color=WHITE)
        plus2 = MathTex("+", font_size=24, color=WHITE)
        eq = MathTex(r"=", font_size=24, color=WHITE)
        result = Text("合成波", font=FONT, font_size=20, color=WHITE)

        legend = VGroup(labels[0], plus1, labels[1], plus2, labels[2], eq, result)
        legend.arrange(RIGHT, buff=0.25)
        legend.next_to(axes, DOWN, buff=0.5)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 4: 分解 = フーリエ変換の直感
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class DecompositionScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        header = Text(
            "逆に、複雑な波を分解できる？",
            font=FONT, font_size=30, color=WHITE,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(header), run_time=0.6)

        freqs = [1, 3, 5]
        amps = [1.0, 0.5, 0.3]
        colors = [ACCENT_RED, ACCENT_BLUE, ACCENT_YELLOW]

        # 上段: 合成波
        axes_top = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2, 0.5],
            x_length=10, y_length=2.5, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 1},
        ).shift(UP * 0.8)

        combined = axes_top.plot(
            lambda x: sum(a * np.sin(f * x) for f, a in zip(freqs, amps)),
            color=WHITE, stroke_width=3,
        )
        combined_label = Text(
            "合成波", font=FONT, font_size=18, color=TEXT_GREY
        ).next_to(axes_top, LEFT, buff=0.3)

        self.play(Create(axes_top), Create(combined), FadeIn(combined_label), run_time=1.5)
        self.wait(0.8)

        # 矢印
        arrow = Arrow(
            axes_top.get_bottom() + DOWN * 0.15,
            axes_top.get_bottom() + DOWN * 0.75,
            color=ACCENT_RED, stroke_width=3,
        )
        arrow_text = Text(
            "フーリエ変換", font=FONT, font_size=18, color=ACCENT_RED
        ).next_to(arrow, RIGHT, buff=0.2)
        self.play(GrowArrow(arrow), FadeIn(arrow_text), run_time=0.8)

        # 下段: 分解された波
        decomposed = VGroup()
        for f, a, c in zip(freqs, amps, colors):
            mini = Axes(
                x_range=[0, 2 * PI, PI],
                y_range=[-1.2, 1.2, 0.5],
                x_length=3, y_length=1.2, tips=False,
                axis_config={"color": GREY_B, "stroke_width": 1},
            )
            w = mini.plot(
                lambda x, freq=f, amp=a: amp * np.sin(freq * x),
                color=c, stroke_width=2.5,
            )
            lbl = MathTex(
                f"{a}" + r"\sin(" + f"{f}" + r"t)",
                color=c, font_size=20,
            ).next_to(mini, DOWN, buff=0.1)
            decomposed.add(VGroup(mini, w, lbl))

        decomposed.arrange(RIGHT, buff=0.5)
        decomposed.next_to(arrow, DOWN, buff=0.4)

        self.play(
            *[FadeIn(g, shift=UP * 0.2) for g in decomposed],
            run_time=1.2,
        )
        self.wait(1)

        conclusion = Text(
            "これがフーリエ変換の本質",
            font=FONT, font_size=26, color=ACCENT_YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(conclusion), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 5: 数式の解説
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class FormulaScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        header = Text(
            "数式で表すと", font=FONT, font_size=28, color=WHITE,
        ).to_edge(UP, buff=0.6)
        self.play(FadeIn(header), run_time=0.5)

        # フーリエ変換の公式
        formula = MathTex(
            r"\hat{f}(\xi)",          # 0
            r"=",                      # 1
            r"\int_{-\infty}^{\infty}",# 2
            r"f(x)",                   # 3
            r"\,",                     # 4
            r"e^{-2\pi i \xi x}",     # 5
            r"\, dx",                  # 6
            font_size=48, color=WHITE,
        )
        self.play(Write(formula), run_time=2.5)
        self.wait(1)

        # 各部分を色付け＋解説
        annotations = [
            (0, ACCENT_RED,    "周波数 ξ の成分"),
            (3, ACCENT_BLUE,   "元の信号"),
            (5, ACCENT_YELLOW, "周波数 ξ で回転する波"),
        ]

        braces_and_labels = VGroup()
        for idx, color, text in annotations:
            formula[idx].set_color(color)
            br = Brace(formula[idx], DOWN, color=color)
            lbl = Text(text, font=FONT, font_size=16, color=color)
            lbl.next_to(br, DOWN, buff=0.1)
            braces_and_labels.add(VGroup(br, lbl))
            self.play(
                formula[idx].animate.set_color(color),
                FadeIn(br), FadeIn(lbl),
                run_time=0.8,
            )
            self.wait(1)

        self.wait(0.5)
        self.play(FadeOut(braces_and_labels), run_time=0.4)

        summary = Text(
            "信号と各周波数の波との「相関」を計算する",
            font=FONT, font_size=22, color=ACCENT_GREEN,
        ).next_to(formula, DOWN, buff=1.0)
        self.play(FadeIn(summary), run_time=0.6)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# シーン 6: 時間領域 → 周波数領域
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class FrequencyDomainScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        header = Text(
            "時間領域 → 周波数領域", font=FONT, font_size=30, color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.6)

        freqs = [1, 3, 5]
        amps = [1.0, 0.5, 0.3]
        bar_colors = [ACCENT_RED, ACCENT_BLUE, ACCENT_YELLOW]

        # 左: 時間領域
        time_title = Text("時間領域", font=FONT, font_size=20, color=TEXT_GREY)
        axes_time = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2, 0.5],
            x_length=5, y_length=3, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 1.5},
        )
        time_wave = axes_time.plot(
            lambda x: sum(a * np.sin(f * x) for f, a in zip(freqs, amps)),
            color=WHITE, stroke_width=2.5,
        )
        time_title.next_to(axes_time, UP, buff=0.2)
        time_group = VGroup(time_title, axes_time, time_wave)
        time_group.shift(LEFT * 3.5 + DOWN * 0.3)

        # 中央: 矢印
        arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=ACCENT_RED, stroke_width=3)
        arrow.shift(DOWN * 0.3)
        ft_label = MathTex(r"\mathcal{F}", color=ACCENT_RED, font_size=30)
        ft_label.next_to(arrow, UP, buff=0.1)

        # 右: 周波数領域
        freq_title = Text("周波数領域", font=FONT, font_size=20, color=TEXT_GREY)
        axes_freq = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.2, 0.5],
            x_length=5, y_length=3, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 1.5},
        )
        freq_x = MathTex(r"\xi", font_size=22, color=GREY_A)
        freq_x.next_to(axes_freq.x_axis, RIGHT, buff=0.15)

        bars = VGroup()
        for f, a, c in zip(freqs, amps, bar_colors):
            bar = Rectangle(
                width=0.5, height=a * 2.5,
                fill_color=c, fill_opacity=0.8,
                stroke_color=c, stroke_width=1,
            )
            bar.move_to(axes_freq.c2p(f, 0), aligned_edge=DOWN)
            num = MathTex(str(f), font_size=18, color=c).next_to(bar, DOWN, buff=0.08)
            bars.add(VGroup(bar, num))

        freq_title.next_to(axes_freq, UP, buff=0.2)
        freq_group = VGroup(freq_title, axes_freq, freq_x, bars)
        freq_group.shift(RIGHT * 3.5 + DOWN * 0.3)

        # アニメーション
        self.play(Create(axes_time), FadeIn(time_title), run_time=0.8)
        self.play(Create(time_wave), run_time=1.5)
        self.wait(0.8)

        self.play(GrowArrow(arrow), FadeIn(ft_label), run_time=0.6)

        self.play(Create(axes_freq), FadeIn(freq_title), FadeIn(freq_x), run_time=0.8)
        for bg in bars:
            self.play(GrowFromEdge(bg[0], DOWN), FadeIn(bg[1]), run_time=0.6)

        self.wait(1)

        conclusion = Text(
            "フーリエ変換 = 波を周波数ごとに整理する",
            font=FONT, font_size=24, color=ACCENT_GREEN,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(conclusion), run_time=0.6)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
