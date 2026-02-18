"""
LLMが文章を生成する仕組み — 3Blue1Brown スタイルアニメーション
==============================================================

manim render -qm scenes/llm_generation_animation.py -a
"""

from manim import *
import numpy as np
import random

# ============================================================================
# カラー定数
# ============================================================================
BG_COLOR = "#1a1a2e"
ACCENT_RED = "#e94560"
ACCENT_YELLOW = "#f5c518"
ACCENT_BLUE = "#3b82f6"
ACCENT_GREEN = "#2ecc71"
ACCENT_PURPLE = "#9b59b6"
ACCENT_CYAN = "#1abc9c"
TEXT_DIM = "#888888"

# ============================================================================
# ヘルパー関数
# ============================================================================

def get_token_box(text, color=ACCENT_BLUE, font_size=28, width=None, height=0.55):
    """トークンを視覚化するボックスを返す"""
    label = Text(text, font="Noto Sans JP", font_size=font_size, color=WHITE)
    w = width or (label.get_width() + 0.4)
    box = RoundedRectangle(
        corner_radius=0.1, width=max(w, 0.6), height=height,
        fill_color=color, fill_opacity=0.25,
        stroke_color=color, stroke_width=2
    )
    label.move_to(box)
    return VGroup(box, label)


def value_to_color(value, low=-1, high=1):
    """値を色にマッピング"""
    alpha = np.clip((value - low) / (high - low + 1e-8), 0, 1)
    blue = ManimColor(ACCENT_BLUE)
    red = ManimColor(ACCENT_RED)
    black = ManimColor(BLACK)
    if value >= 0:
        return interpolate_color(black, blue, alpha)
    else:
        return interpolate_color(black, red, 1 - alpha)


# ============================================================================
# Scene 1: タイトル
# ============================================================================

class Scene01_Title(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # メインタイトル
        title = Text(
            "LLMが文章を生成する仕組み",
            font="Noto Sans JP", font_size=46, color=WHITE, weight=BOLD
        )
        title.shift(UP * 0.5)

        subtitle = Text(
            "Large Language Model の内側を覗いてみよう",
            font="Noto Sans JP", font_size=24, color=ACCENT_RED
        )
        subtitle.next_to(title, DOWN, buff=0.6)

        # 装飾線
        line_left = Line(LEFT * 5, LEFT * 0.5, color=ACCENT_RED, stroke_width=2)
        line_right = Line(RIGHT * 0.5, RIGHT * 5, color=ACCENT_RED, stroke_width=2)
        lines = VGroup(line_left, line_right)
        lines.next_to(subtitle, DOWN, buff=0.5)

        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.5)
        self.wait(0.3)
        self.play(FadeIn(subtitle), run_time=1)
        self.play(Create(line_left), Create(line_right), run_time=0.8)
        self.wait(1)

        # プレビュー：ステップ概要
        steps = VGroup(*[
            Text(s, font="Noto Sans JP", font_size=20, color=TEXT_DIM)
            for s in [
                "1. テキストをトークンに分解",
                "2. トークンを数値ベクトルに変換",
                "3. Transformer で文脈を理解",
                "4. 次の単語の確率を予測",
                "5. 繰り返して文章を生成",
            ]
        ]).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.next_to(lines, DOWN, buff=0.6)

        self.play(LaggedStart(*[
            FadeIn(step) for step in steps
        ], lag_ratio=0.15), run_time=2)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 2: トークン化
# ============================================================================

class Scene02_Tokenization(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # セクションタイトル
        section = Text("Step 1: トークン化", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section), run_time=0.8)

        # 元の文章
        sentence_text = "今日はとても良い天気です"
        sentence = Text(sentence_text, font="Noto Sans JP", font_size=36, color=WHITE)
        sentence.next_to(section, DOWN, buff=0.8)
        self.play(FadeIn(sentence), run_time=1)
        self.wait(0.5)

        # 説明テキスト
        desc = Text(
            "LLM はまず文章を「トークン」と呼ばれる\n小さな単位に分解します",
            font="Noto Sans JP", font_size=20, color=TEXT_DIM
        )
        desc.next_to(sentence, DOWN, buff=0.6)
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(0.5)

        # トークンへの分割を視覚化
        tokens = ["今日", "は", "とても", "良い", "天気", "です"]
        colors = [ACCENT_BLUE, ACCENT_PURPLE, ACCENT_GREEN, ACCENT_YELLOW, ACCENT_CYAN, ACCENT_RED]

        token_boxes = VGroup(*[
            get_token_box(t, color=c)
            for t, c in zip(tokens, colors)
        ]).arrange(RIGHT, buff=0.15)
        token_boxes.move_to(sentence.get_center())

        # 文章 → トークンに変形
        self.play(FadeOut(desc), run_time=0.3)
        self.play(
            FadeOut(sentence),
            LaggedStart(*[FadeIn(tb, shift=UP * 0.2) for tb in token_boxes],
                        lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(0.5)

        # 各トークンを一つずつ強調
        highlight_rect = SurroundingRectangle(
            token_boxes[0], buff=0.08, color=ACCENT_YELLOW, stroke_width=2.5
        )
        self.play(Create(highlight_rect), run_time=0.4)
        for i in range(1, len(token_boxes)):
            self.play(
                highlight_rect.animate.move_to(token_boxes[i]),
                run_time=0.3
            )
            self.wait(0.15)
        self.play(FadeOut(highlight_rect), run_time=0.3)

        # トークンIDの表示
        self.play(token_boxes.animate.shift(UP * 0.5), run_time=0.5)

        arrow_down = Arrow(ORIGIN, DOWN * 0.6, color=WHITE, stroke_width=2,
                           max_tip_length_to_length_ratio=0.2)
        arrow_down.next_to(token_boxes, DOWN, buff=0.3)
        self.play(GrowArrow(arrow_down), run_time=0.5)

        ids = [1024, 42, 8803, 512, 2048, 99]
        id_boxes = VGroup(*[
            get_token_box(str(tid), color=c, font_size=22)
            for tid, c in zip(ids, colors)
        ]).arrange(RIGHT, buff=0.15)
        id_boxes.next_to(arrow_down, DOWN, buff=0.3)

        id_label = Text("トークン ID", font="Noto Sans JP", font_size=18, color=TEXT_DIM)
        id_label.next_to(id_boxes, DOWN, buff=0.3)

        self.play(
            LaggedStart(*[FadeIn(ib, shift=UP * 0.15) for ib in id_boxes],
                        lag_ratio=0.08),
            run_time=1.2
        )
        self.play(FadeIn(id_label), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 3: 埋め込み（Embedding）
# ============================================================================

class Scene03_Embedding(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 2: 埋め込み（Embedding）", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section), run_time=0.8)

        # トークンIDを表示
        tokens = ["今日", "は", "とても"]
        ids = ["1024", "42", "8803"]
        token_id_group = VGroup()
        for tok, tid in zip(tokens, ids):
            tok_text = Text(tok, font="Noto Sans JP", font_size=22, color=WHITE)
            id_text = Text(tid, font_size=18, color=TEXT_DIM)
            id_text.next_to(tok_text, DOWN, buff=0.1)
            token_id_group.add(VGroup(tok_text, id_text))
        token_id_group.arrange(RIGHT, buff=1.2)
        token_id_group.next_to(section, DOWN, buff=0.7).shift(LEFT * 2.5)

        self.play(LaggedStart(*[FadeIn(g) for g in token_id_group],
                              lag_ratio=0.2), run_time=1)

        # 説明テキスト
        desc = Text(
            "各トークンは高次元の数値ベクトルに\n変換されます（例: 768次元）",
            font="Noto Sans JP", font_size=20, color=TEXT_DIM
        )
        desc.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(desc), run_time=0.8)

        # ベクトル（行列セル）の可視化
        np.random.seed(42)
        vectors_group = VGroup()
        for i, tok_group in enumerate(token_id_group):
            cells = VGroup()
            n_cells = 8
            for j in range(n_cells):
                val = np.random.uniform(-1, 1)
                cell = Square(side_length=0.35)
                cell.set_fill(value_to_color(val), opacity=0.8)
                cell.set_stroke(GREY_B, 0.5)
                num = DecimalNumber(val, num_decimal_places=1, font_size=12, color=WHITE)
                num.move_to(cell)
                cells.add(VGroup(cell, num))
            cells.arrange(DOWN, buff=0.02)
            cells.next_to(tok_group, DOWN, buff=0.8)
            vectors_group.add(cells)

        # 矢印（トークン → ベクトル）
        arrows = VGroup()
        for tok_group, vec in zip(token_id_group, vectors_group):
            a = Arrow(
                tok_group.get_bottom(), vec.get_top(),
                buff=0.15, color=GREY_B, stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(a)

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.2), run_time=1)
        self.play(LaggedStart(*[
            FadeIn(vec, shift=UP * 0.15) for vec in vectors_group
        ], lag_ratio=0.15), run_time=1.5)
        self.wait(0.5)

        # 「...」を追加（768次元のうちの一部だけ）
        dots_labels = VGroup()
        for vec in vectors_group:
            dots = Text("...", font_size=20, color=TEXT_DIM)
            dots.next_to(vec, DOWN, buff=0.1)
            dim_label = Text("768次元", font="Noto Sans JP", font_size=14, color=TEXT_DIM)
            dim_label.next_to(dots, DOWN, buff=0.1)
            dots_labels.add(VGroup(dots, dim_label))

        self.play(LaggedStart(*[FadeIn(d) for d in dots_labels],
                              lag_ratio=0.1), run_time=0.8)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 4: Transformer（セルフアテンション）
# ============================================================================

class Scene04_Transformer(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 3: Transformer", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section), run_time=0.8)

        # トークンを横に並べる
        tokens = ["今日", "は", "とても", "良い", "天気"]
        token_boxes = VGroup(*[
            get_token_box(t, color=ACCENT_BLUE, font_size=22, height=0.5)
            for t in tokens
        ]).arrange(RIGHT, buff=0.3)
        token_boxes.shift(UP * 1.8)

        self.play(LaggedStart(*[FadeIn(tb) for tb in token_boxes],
                              lag_ratio=0.1), run_time=1)

        # Self-Attention の説明
        attn_title = Text("セルフアテンション", font="Noto Sans JP",
                          font_size=26, color=ACCENT_YELLOW, weight=BOLD)
        attn_title.next_to(token_boxes, DOWN, buff=0.5)
        self.play(FadeIn(attn_title), run_time=0.5)

        attn_desc = Text(
            "各トークンが他の全トークンとの\n「関連度」を計算します",
            font="Noto Sans JP", font_size=18, color=TEXT_DIM
        )
        attn_desc.next_to(attn_title, DOWN, buff=0.3)
        self.play(FadeIn(attn_desc), run_time=0.8)
        self.wait(0.5)

        # 「天気」に注目 → 他のトークンとの関連度を弧で表示
        target_idx = 4  # 「天気」
        self.play(FadeOut(attn_desc), run_time=0.3)

        # ターゲット強調
        target_rect = SurroundingRectangle(
            token_boxes[target_idx], buff=0.08,
            color=ACCENT_YELLOW, stroke_width=2.5
        )
        focus_label = Text("「天気」に注目", font="Noto Sans JP",
                           font_size=18, color=ACCENT_YELLOW)
        focus_label.next_to(target_rect, UP, buff=0.2)
        self.play(Create(target_rect), FadeIn(focus_label), run_time=0.6)

        # アテンションの弧とスコア
        attn_weights = [0.15, 0.05, 0.10, 0.30, 0.40]
        arcs = VGroup()
        weight_labels = VGroup()

        for i, (w, tb) in enumerate(zip(attn_weights, token_boxes)):
            if i == target_idx:
                continue
            arc_color_alpha = w / 0.4
            arc_color = interpolate_color(
                ManimColor(GREY_B), ManimColor(ACCENT_YELLOW), arc_color_alpha
            )
            arc = CurvedArrow(
                token_boxes[target_idx].get_bottom() + DOWN * 0.05,
                tb.get_bottom() + DOWN * 0.05,
                angle=-PI * 0.4 if i < target_idx else PI * 0.4,
                color=arc_color,
                stroke_width=1.5 + w * 6,
                tip_length=0.15
            )
            wl_color = interpolate_color(
                ManimColor(TEXT_DIM), ManimColor(ACCENT_YELLOW), arc_color_alpha
            )
            wl = Text(f"{w:.0%}", font_size=14, color=wl_color)
            wl.next_to(arc, DOWN, buff=0.05)
            arcs.add(arc)
            weight_labels.add(wl)

        self.play(LaggedStart(*[
            Create(arc) for arc in arcs
        ], lag_ratio=0.15), run_time=2)
        self.play(LaggedStart(*[
            FadeIn(wl) for wl in weight_labels
        ], lag_ratio=0.1), run_time=0.8)
        self.wait(1)

        # 解釈テキスト
        interpret = Text(
            "「良い」と「天気」の関連度が高い → 文脈を理解している",
            font="Noto Sans JP", font_size=18, color=ACCENT_GREEN
        )
        interpret.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(interpret), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 5: 次トークン予測
# ============================================================================

class Scene05_NextTokenPrediction(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 4: 次のトークンを予測", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section), run_time=0.8)

        # 入力トークン列
        input_tokens = ["今日", "は", "とても", "良い", "天気"]
        input_boxes = VGroup(*[
            get_token_box(t, color=ACCENT_BLUE, font_size=22, height=0.48)
            for t in input_tokens
        ]).arrange(RIGHT, buff=0.12)
        input_boxes.next_to(section, DOWN, buff=0.7)

        self.play(LaggedStart(*[FadeIn(tb) for tb in input_boxes],
                              lag_ratio=0.08), run_time=1)

        # 「?」ボックス
        q_box = get_token_box("?", color=ACCENT_YELLOW, font_size=28, height=0.48)
        q_box.next_to(input_boxes, RIGHT, buff=0.12)
        self.play(FadeIn(q_box, shift=LEFT * 0.3), run_time=0.8)
        self.wait(0.3)

        # Transformer ブロックの矢印
        arrow_down = Arrow(
            VGroup(input_boxes, q_box).get_bottom() + DOWN * 0.1,
            VGroup(input_boxes, q_box).get_bottom() + DOWN * 0.9,
            color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15
        )
        transformer_box = RoundedRectangle(
            corner_radius=0.15, width=3.5, height=0.6,
            fill_color=ACCENT_PURPLE, fill_opacity=0.2,
            stroke_color=ACCENT_PURPLE, stroke_width=2
        )
        transformer_label = Text("Transformer", font_size=22, color=ACCENT_PURPLE)
        transformer_label.move_to(transformer_box)
        transformer_group = VGroup(transformer_box, transformer_label)
        transformer_group.next_to(arrow_down, DOWN, buff=0.15)

        self.play(GrowArrow(arrow_down), FadeIn(transformer_group), run_time=1)

        # 確率分布
        arrow_down2 = Arrow(
            transformer_group.get_bottom() + DOWN * 0.1,
            transformer_group.get_bottom() + DOWN * 0.7,
            color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15
        )
        self.play(GrowArrow(arrow_down2), run_time=0.5)

        prob_title = Text("次のトークンの確率分布", font="Noto Sans JP",
                          font_size=20, color=WHITE)
        prob_title.next_to(arrow_down2, DOWN, buff=0.2)
        self.play(FadeIn(prob_title), run_time=0.5)

        # 確率バー
        probs_data = [
            ("です", 0.42, ACCENT_GREEN),
            ("だ", 0.18, ACCENT_BLUE),
            ("で", 0.15, ACCENT_CYAN),
            ("に", 0.08, ACCENT_PURPLE),
            ("が", 0.05, GREY_B),
            ("...", 0.12, GREY),
        ]
        bars = VGroup()
        for text, prob, color in probs_data:
            label = Text(text, font="Noto Sans JP", font_size=18, color=WHITE)
            bar = Rectangle(
                width=3.5 * prob, height=0.28,
                fill_color=color, fill_opacity=0.7, stroke_width=0
            )
            pct = Text(f"{prob*100:.0f}%", font_size=14, color=WHITE)
            row = VGroup(label, bar, pct).arrange(RIGHT, buff=0.15)
            bars.add(row)

        bars.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        bars.next_to(prob_title, DOWN, buff=0.3)
        # 画面内に収まるように調整
        if bars.get_bottom()[1] < -3.8:
            bars.shift(UP * (bars.get_bottom()[1] + 3.8) * -1)

        self.play(LaggedStart(*[FadeIn(b) for b in bars],
                              lag_ratio=0.1), run_time=1.5)
        self.wait(0.5)

        # 最も確率が高い「です」を強調
        top_rect = SurroundingRectangle(bars[0], buff=0.06,
                                        color=ACCENT_YELLOW, stroke_width=2)
        self.play(Create(top_rect), run_time=0.5)

        # 「です」を選択 → ? を置換
        new_box = get_token_box("です", color=ACCENT_GREEN, font_size=22, height=0.48)
        new_box.move_to(q_box)

        self.play(
            FadeOut(q_box),
            FadeIn(new_box, shift=UP * 0.2),
            run_time=1
        )
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


# ============================================================================
# Scene 6: 自己回帰的生成ループ
# ============================================================================

class Scene06_AutoregressiveGeneration(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("Step 5: 文章の生成", font="Noto Sans JP",
                       font_size=36, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section), run_time=0.8)

        desc = Text(
            "LLM は予測したトークンを入力に追加し、\nこのプロセスを繰り返して文章を生成します",
            font="Noto Sans JP", font_size=20, color=TEXT_DIM
        )
        desc.next_to(section, DOWN, buff=0.5)
        self.play(FadeIn(desc), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(desc), run_time=0.3)

        # 自己回帰的に文章を生成する様子をアニメーション
        generation_steps = [
            "は",
            "とても",
            "良い",
            "天気",
            "です",
        ]

        current_boxes = VGroup()

        # 初期トークン「今日」
        first_box = get_token_box("今日", color=ACCENT_BLUE, font_size=24, height=0.5)
        first_box.move_to(LEFT * 4.5 + UP * 1.0)
        current_boxes.add(first_box)
        self.play(FadeIn(first_box), run_time=0.5)

        for step_idx, new_token in enumerate(generation_steps):
            # 「→ ?」を表示
            q_box = get_token_box("?", color=ACCENT_YELLOW, font_size=24, height=0.5)
            q_box.next_to(current_boxes, RIGHT, buff=0.15)

            # 処理中のインジケータ
            dots = Text("...", font_size=20, color=ACCENT_YELLOW)
            dots.next_to(q_box, DOWN, buff=0.2)

            self.play(FadeIn(q_box, shift=LEFT * 0.2), run_time=0.3)
            self.play(FadeIn(dots), run_time=0.2)
            self.wait(0.3)

            # 新トークンに置換
            new_box = get_token_box(new_token, color=ACCENT_GREEN, font_size=24, height=0.5)
            new_box.move_to(q_box)

            self.play(
                FadeOut(q_box), FadeOut(dots),
                FadeIn(new_box, shift=UP * 0.15),
                run_time=0.5
            )

            # 色をブルーに戻す（確定）
            settled_box = get_token_box(new_token, color=ACCENT_BLUE, font_size=24, height=0.5)
            settled_box.move_to(new_box)
            self.play(FadeOut(new_box), FadeIn(settled_box), run_time=0.3)
            current_boxes.add(settled_box)

        self.wait(0.5)

        # 完成した文章を強調
        final_rect = SurroundingRectangle(
            current_boxes, buff=0.15, color=ACCENT_GREEN, stroke_width=2.5,
            corner_radius=0.1
        )
        complete_label = Text("完成!", font="Noto Sans JP", font_size=28,
                              color=ACCENT_GREEN, weight=BOLD)
        complete_label.next_to(final_rect, DOWN, buff=0.4)

        self.play(Create(final_rect), FadeIn(complete_label), run_time=1)
        self.wait(0.8)

        # 全体をまとめる → 中央に移動
        all_gen = VGroup(current_boxes, final_rect, complete_label)
        self.play(all_gen.animate.scale(0.8).move_to(UP * 1.5), run_time=1)

        # まとめテキスト
        summary_lines = VGroup(*[
            Text(line, font="Noto Sans JP", font_size=20, color=c)
            for line, c in [
                ("LLM の文章生成 = 次のトークンを予測し続けること", WHITE),
                ("1.トークン化 → 2.埋め込み → 3.Transformer → 4.確率予測", ACCENT_CYAN),
                ("この繰り返しで、一見「知性」があるような文章が生まれます", TEXT_DIM),
            ]
        ]).arrange(DOWN, buff=0.3)
        summary_lines.next_to(all_gen, DOWN, buff=0.6)

        self.play(LaggedStart(*[FadeIn(l) for l in summary_lines],
                              lag_ratio=0.3), run_time=2)
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
