"""
トヨタのビジネスモデル解剖 〜なぜ世界一なのか〜

企業解説アニメーション — プロ品質モーショングラフィックス風
"""
from manim import *
import numpy as np

# ── カラーパレット（トヨタブランド軸） ─────────────
BG = "#0d1117"
TOYOTA_RED = "#eb0a1e"
GOLD = "#d4a03c"
SILVER = "#c0c0c0"
SOFT_WHITE = "#e8e8e8"
LIGHT_GREY = "#8b949e"
DIM = "#30363d"
PANEL = "#161b22"
CHART_BLUE = "#58a6ff"
CHART_GREEN = "#3fb950"
CHART_ORANGE = "#d29922"
CHART_PURPLE = "#bc8cff"
CHART_CYAN = "#39d2c0"
FN = "Noto Sans JP"

def txt(text, size=24, color=SOFT_WHITE, **kw):
    return Text(text, font=FN, font_size=size, color=color, **kw)

def mono(text, size=24, color=SOFT_WHITE):
    return Text(text, font_size=size, color=color)

def panel_rect(w=4, h=3, color=DIM):
    return RoundedRectangle(
        corner_radius=0.12, width=w, height=h,
        fill_color=color, fill_opacity=0.4,
        stroke_color=color, stroke_width=0.5,
    )

def accent_line(start, end, color=TOYOTA_RED):
    return Line(start, end, color=color, stroke_width=2.5)

def wipe(self):
    self.play(*[FadeOut(m, shift=LEFT * 0.3) for m in self.mobjects], run_time=0.6)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. タイトル
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TitleScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 赤い横線が走ってからタイトル登場
        red_line = Line(LEFT * 8, RIGHT * 8, color=TOYOTA_RED, stroke_width=3)
        red_line.shift(UP * 0.5)
        self.play(Create(red_line), run_time=0.8, rate_func=rush_into)
        self.wait(0.3)

        title = txt("トヨタのビジネスモデル解剖", size=44, color=WHITE, weight=BOLD)
        title.next_to(red_line, UP, buff=0.4)

        sub = txt("なぜ世界一なのか", size=28, color=TOYOTA_RED)
        sub.next_to(red_line, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.6)
        self.wait(0.5)

        # 小さな補足
        note = txt("Toyota Motor Corporation", size=16, color=LIGHT_GREY)
        note.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(3)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 企業概要
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CompanyOverviewScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 左側にラベル
        header = txt("COMPANY OVERVIEW", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.6)

        # 4つのキーメトリクス
        metrics = [
            ("売上高", "45.1 兆円", "FY2024", TOYOTA_RED),
            ("営業利益", "5.35 兆円", "営業利益率 11.9%", GOLD),
            ("世界販売台数", "1,123 万台", "グループ合計", CHART_BLUE),
            ("従業員数", "37.5 万人", "連結", CHART_GREEN),
        ]

        cards = VGroup()
        for title_t, value, note_t, col in metrics:
            bg = panel_rect(w=2.8, h=2.2, color=PANEL)
            t = txt(title_t, size=14, color=LIGHT_GREY)
            v = txt(value, size=26, color=col, weight=BOLD)
            n = txt(note_t, size=11, color=DIM)
            content = VGroup(t, v, n).arrange(DOWN, buff=0.25)
            card = VGroup(bg, content)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.35)
        cards.shift(DOWN * 0.2)

        for i, card in enumerate(cards):
            self.play(
                FadeIn(card, shift=UP * 0.2),
                run_time=0.5,
                rate_func=smooth,
            )
            self.wait(0.4)

        # 底部ライン
        bottom_note = txt("自動車メーカー世界 売上高ランキング 第1位", size=16, color=LIGHT_GREY)
        bottom_note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(bottom_note), run_time=0.4)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 売上規模の比較
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class RevenueScaleScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("売上高の規模感", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        question = txt("45兆円はどれくらいの規模か？", size=24, color=WHITE)
        question.next_to(header, DOWN, buff=0.6).align_to(header, LEFT)
        self.play(FadeIn(question), run_time=0.5)
        self.wait(1)

        # 比較データ
        comparisons = [
            ("トヨタ", 45.1, TOYOTA_RED),
            ("日本の国家予算（一般会計）", 114.0, LIGHT_GREY),
            ("NTT", 13.4, CHART_BLUE),
            ("ソニー", 13.0, CHART_PURPLE),
            ("任天堂", 1.7, CHART_GREEN),
        ]

        bars = VGroup()
        max_val = 114.0
        bar_max_width = 9

        for name, val, col in comparisons:
            bar_w = (val / max_val) * bar_max_width
            bar = Rectangle(
                width=bar_w, height=0.45,
                fill_color=col, fill_opacity=0.7,
                stroke_width=0,
            )
            bar.align_to(LEFT * 5, LEFT)

            name_t = txt(name, size=14, color=SOFT_WHITE)
            name_t.next_to(bar, LEFT, buff=0.2)

            val_t = txt(f"{val}兆円", size=13, color=col, weight=BOLD)
            val_t.next_to(bar, RIGHT, buff=0.15)

            bars.add(VGroup(name_t, bar, val_t))

        bars.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        bars.shift(DOWN * 0.6)

        # バーの左端を揃え直す
        for bg in bars:
            bg[1].align_to(LEFT * 1.5, LEFT)
            bg[0].next_to(bg[1], LEFT, buff=0.2)
            bg[2].next_to(bg[1], RIGHT, buff=0.15)

        for i, bg in enumerate(bars):
            self.play(
                FadeIn(bg[0]),
                GrowFromEdge(bg[1], LEFT),
                FadeIn(bg[2]),
                run_time=0.7 if i == 0 else 0.4,
            )
            self.wait(0.3 if i == 0 else 0.15)

        self.wait(3)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 売上構成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class RevenueBreakdownScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("REVENUE BREAKDOWN", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("事業セグメント別 売上構成", size=22, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # 左：ドーナツチャート風
        segments = [
            ("自動車", 89, TOYOTA_RED),
            ("金融", 6, CHART_BLUE),
            ("その他", 5, LIGHT_GREY),
        ]

        # 円弧で擬似ドーナツ
        donut_center = LEFT * 3 + DOWN * 0.5
        radius = 1.8
        inner_radius = 1.1
        start_angle = PI / 2
        arcs = VGroup()

        for name, pct, col in segments:
            angle = pct / 100 * TAU
            arc = AnnularSector(
                inner_radius=inner_radius, outer_radius=radius,
                angle=angle, start_angle=start_angle,
                fill_color=col, fill_opacity=0.8,
                stroke_color=BG, stroke_width=2,
            ).move_arc_center_to(donut_center)
            arcs.add(arc)
            start_angle += angle

        # 中央テキスト
        center_val = txt("45.1", size=28, color=WHITE, weight=BOLD)
        center_unit = txt("兆円", size=14, color=LIGHT_GREY)
        center_g = VGroup(center_val, center_unit).arrange(DOWN, buff=0.1)
        center_g.move_to(donut_center)

        self.play(*[FadeIn(a) for a in arcs], run_time=1.2)
        self.play(FadeIn(center_g), run_time=0.4)

        # 右：凡例
        legend = VGroup()
        for name, pct, col in segments:
            dot = Square(side_length=0.2, fill_color=col, fill_opacity=0.8, stroke_width=0)
            n = txt(name, size=16, color=SOFT_WHITE)
            p = txt(f"{pct}%", size=16, color=col, weight=BOLD)
            row = VGroup(dot, n, p).arrange(RIGHT, buff=0.3)
            legend.add(row)
        legend.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        legend.shift(RIGHT * 2.5 + DOWN * 0.3)

        self.play(FadeIn(legend), run_time=0.6)
        self.wait(1)

        # コメント
        note = txt("売上の約9割が自動車事業。圧倒的な本業集中型", size=16, color=LIGHT_GREY)
        note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. グローバル販売
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class GlobalSalesScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("GLOBAL SALES", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("地域別 販売構成比", size=22, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # 地域データ
        regions = [
            ("日本", 187, "17%", TOYOTA_RED),
            ("北米", 282, "25%", CHART_BLUE),
            ("欧州", 115, "10%", CHART_GREEN),
            ("アジア", 347, "31%", CHART_ORANGE),
            ("その他", 192, "17%", LIGHT_GREY),
        ]

        # 横棒グラフ
        chart = VGroup()
        max_val = 347
        bar_max = 7

        for name, val, pct, col in regions:
            name_t = txt(name, size=16, color=SOFT_WHITE)
            bar = Rectangle(
                width=(val / max_val) * bar_max, height=0.5,
                fill_color=col, fill_opacity=0.65,
                stroke_width=0,
            )
            val_t = txt(f"{val}万台", size=13, color=col, weight=BOLD)
            pct_t = txt(pct, size=12, color=LIGHT_GREY)

            name_t.move_to(LEFT * 5.5)
            bar.align_to(LEFT * 3.5, LEFT)
            val_t.next_to(bar, RIGHT, buff=0.15)
            pct_t.next_to(val_t, RIGHT, buff=0.15)

            chart.add(VGroup(name_t, bar, val_t, pct_t))

        chart.arrange(DOWN, buff=0.35)
        chart.shift(DOWN * 0.3)

        # 名前とバーの位置を揃え直す
        for row in chart:
            row[0].align_to(LEFT * 5.5, LEFT)
            row[1].align_to(LEFT * 3.5, LEFT)
            row[2].next_to(row[1], RIGHT, buff=0.15)
            row[3].next_to(row[2], RIGHT, buff=0.15)

        for row in chart:
            self.play(
                FadeIn(row[0]),
                GrowFromEdge(row[1], LEFT),
                FadeIn(row[2]), FadeIn(row[3]),
                run_time=0.5,
            )
            self.wait(0.2)

        self.wait(1)

        # 見出しコメント
        note = txt("アジアが最大市場。地域偏重のない分散ポートフォリオ", size=16, color=LIGHT_GREY)
        note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(3)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 利益構造
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ProfitStructureScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("PROFIT STRUCTURE", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("なぜ利益率が高いのか", size=24, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # ウォーターフォールチャート風
        items = [
            ("売上高", 45.1, 0, LIGHT_GREY, True),
            ("原価", -33.8, 45.1, CHART_ORANGE, False),
            ("販管費", -5.0, 11.3, CHART_PURPLE, False),
            ("研究開発費", -1.3, 6.3, CHART_BLUE, False),
            ("営業利益", 5.0, 0, GOLD, True),
        ]

        chart = VGroup()
        scale = 0.065
        base_y = DOWN * 2

        for i, (name, val, offset, col, is_total) in enumerate(items):
            x = LEFT * 4.5 + RIGHT * i * 2.5
            h = abs(val) * scale
            bar = Rectangle(
                width=1.5, height=h,
                fill_color=col, fill_opacity=0.7,
                stroke_color=col, stroke_width=1,
            )
            if is_total:
                bar.move_to(x + base_y + UP * h / 2)
            else:
                bar.move_to(x + base_y + UP * (offset * scale - h / 2))

            n = txt(name, size=12, color=SOFT_WHITE)
            n.next_to(bar, DOWN, buff=0.15)

            v = txt(f"{val:+.1f}" if not is_total else f"{val:.1f}", size=13, color=col, weight=BOLD)
            v.next_to(bar, UP, buff=0.1)

            chart.add(VGroup(bar, n, v))

        chart.move_to(DOWN * 0.3)

        for cg in chart:
            self.play(
                GrowFromEdge(cg[0], DOWN),
                FadeIn(cg[1]), FadeIn(cg[2]),
                run_time=0.6,
            )
            self.wait(0.3)

        self.wait(1)

        # 営業利益率の強調
        margin_panel = panel_rect(w=4, h=1, color=PANEL)
        margin_t = txt("営業利益率", size=14, color=LIGHT_GREY)
        margin_v = txt("11.9%", size=30, color=GOLD, weight=BOLD)
        margin_n = txt("自動車業界トップクラス", size=12, color=LIGHT_GREY)
        mg = VGroup(margin_t, margin_v, margin_n).arrange(DOWN, buff=0.1)
        margin_card = VGroup(margin_panel, mg)
        margin_card.to_edge(RIGHT, buff=0.5).shift(UP * 1)

        self.play(FadeIn(margin_card, shift=LEFT * 0.2), run_time=0.6)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. 競合比較
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CompetitorScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("COMPETITOR ANALYSIS", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("主要自動車メーカーとの比較", size=22, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # データ（売上高 兆円換算、営業利益率 %）
        companies = [
            ("トヨタ", 45.1, 11.9, TOYOTA_RED),
            ("VW", 43.0, 7.0, CHART_BLUE),
            ("GM", 24.0, 6.5, LIGHT_GREY),
            ("ステランティス", 22.0, 10.0, CHART_GREEN),
            ("BYD", 9.0, 5.5, CHART_ORANGE),
        ]

        # テーブル風レイアウト
        col_x = [-3.5, -0.5, 2.5]  # 企業名, 売上高, 利益率

        # ヘッダー行
        h_name = txt("企業", size=13, color=LIGHT_GREY)
        h_rev = txt("売上高", size=13, color=LIGHT_GREY)
        h_margin = txt("営業利益率", size=13, color=LIGHT_GREY)
        for h, x in zip([h_name, h_rev, h_margin], col_x):
            h.move_to(RIGHT * x + UP * 1.2)

        header_line = Line(LEFT * 5.5 + UP * 0.95, RIGHT * 5 + UP * 0.95,
                           color=DIM, stroke_width=1)
        self.play(
            FadeIn(h_name), FadeIn(h_rev), FadeIn(h_margin),
            Create(header_line),
            run_time=0.5,
        )

        # データ行
        rows = VGroup()
        for i, (name, rev, margin, col) in enumerate(companies):
            y = 0.5 - i * 0.7
            n = txt(name, size=16, color=col, weight=BOLD)
            n.move_to(RIGHT * col_x[0] + UP * y)

            # 売上棒
            bar_w = rev / 45.1 * 4
            bar = Rectangle(width=bar_w, height=0.35,
                            fill_color=col, fill_opacity=0.5,
                            stroke_width=0)
            bar.align_to(RIGHT * (col_x[1] - 1.8), LEFT)
            bar.shift(UP * y)
            rv = txt(f"{rev:.1f}兆円", size=12, color=col)
            rv.next_to(bar, RIGHT, buff=0.1)

            # 利益率
            mg = txt(f"{margin}%", size=16, color=col, weight=BOLD)
            mg.move_to(RIGHT * col_x[2] + UP * y)

            row = VGroup(n, bar, rv, mg)
            rows.add(row)

        for row in rows:
            self.play(
                FadeIn(row[0]),
                GrowFromEdge(row[1], LEFT),
                FadeIn(row[2]),
                FadeIn(row[3]),
                run_time=0.5,
            )
            self.wait(0.15)

        self.wait(1.5)

        # ポイント
        point = txt("売上高トップかつ利益率もトップクラス → 量と質の両立", size=16, color=GOLD)
        point.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(point), run_time=0.5)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. トヨタ生産方式
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TPSScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("TOYOTA PRODUCTION SYSTEM", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("利益率の秘密 ── トヨタ生産方式", size=24, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.5)

        # 2本柱
        pillar_l = panel_rect(w=4.5, h=3.8, color=PANEL)
        pillar_r = panel_rect(w=4.5, h=3.8, color=PANEL)
        pillars = VGroup(pillar_l, pillar_r).arrange(RIGHT, buff=0.5)
        pillars.shift(DOWN * 0.4)

        # 左柱：ジャスト・イン・タイム
        jit_title = txt("ジャスト・イン・タイム", size=18, color=CHART_BLUE, weight=BOLD)
        jit_items = VGroup(
            txt("必要なモノを", size=14, color=SOFT_WHITE),
            txt("必要な時に", size=14, color=SOFT_WHITE),
            txt("必要な量だけ作る", size=14, color=SOFT_WHITE),
        ).arrange(DOWN, buff=0.2)
        jit_effect = txt("→ 在庫を最小化しコスト削減", size=13, color=CHART_BLUE)
        jit_g = VGroup(jit_title, jit_items, jit_effect).arrange(DOWN, buff=0.4)
        jit_g.move_to(pillar_l)

        # 右柱：自働化
        jidoka_title = txt("自働化（にんべんの自動化）", size=18, color=CHART_GREEN, weight=BOLD)
        jidoka_items = VGroup(
            txt("異常を即座に検知", size=14, color=SOFT_WHITE),
            txt("ラインを自動停止", size=14, color=SOFT_WHITE),
            txt("不良品を流さない", size=14, color=SOFT_WHITE),
        ).arrange(DOWN, buff=0.2)
        jidoka_effect = txt("→ 品質を工程で作り込む", size=13, color=CHART_GREEN)
        jidoka_g = VGroup(jidoka_title, jidoka_items, jidoka_effect).arrange(DOWN, buff=0.4)
        jidoka_g.move_to(pillar_r)

        self.play(FadeIn(pillar_l), FadeIn(pillar_r), run_time=0.5)
        self.play(FadeIn(jit_g, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(jidoka_g, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)

        # 基盤：カイゼン
        base = panel_rect(w=9.5, h=0.7, color=TOYOTA_RED)
        base_t = txt("基盤 : カイゼン（継続的改善）", size=16, color=WHITE, weight=BOLD)
        base_g = VGroup(base, base_t)
        base_g.next_to(pillars, DOWN, buff=0.3)
        self.play(FadeIn(base_g, shift=UP * 0.1), run_time=0.6)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. ブランドポートフォリオ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class BrandPortfolioScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("BRAND PORTFOLIO", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("マルチブランド戦略", size=22, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # ブランドカード
        brands = [
            ("Toyota", "量販・主力ブランド", "世界販売の大半を占める", TOYOTA_RED),
            ("Lexus", "高級車ブランド", "高マージン・ブランド価値", GOLD),
            ("ダイハツ", "軽自動車・小型車", "国内軽自動車シェア上位", CHART_BLUE),
            ("日野", "商用車（トラック・バス）", "物流・インフラ領域", CHART_GREEN),
        ]

        cards = VGroup()
        for name, desc, detail, col in brands:
            bg = panel_rect(w=5, h=1.2, color=PANEL)
            accent = Line(bg.get_left() + RIGHT * 0.1 + UP * 0.4,
                          bg.get_left() + RIGHT * 0.1 + DOWN * 0.4,
                          color=col, stroke_width=4)
            n = txt(name, size=20, color=col, weight=BOLD)
            d = txt(desc, size=13, color=SOFT_WHITE)
            dt = txt(detail, size=11, color=LIGHT_GREY)
            content = VGroup(n, d, dt).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            content.next_to(accent, RIGHT, buff=0.3)
            card = VGroup(bg, accent, content)
            cards.add(card)

        cards.arrange(DOWN, buff=0.25)
        cards.shift(DOWN * 0.2)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.5)

        note = txt("価格帯・車種・地域を幅広くカバーするポートフォリオ", size=16, color=LIGHT_GREY)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(3)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. パワートレイン戦略
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class PowertrainStrategyScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("MULTI-PATHWAY STRATEGY", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("全方位戦略 ── 一つに賭けない", size=24, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # 中央にトヨタ
        center_circle = Circle(radius=0.6, fill_color=TOYOTA_RED, fill_opacity=0.3,
                               stroke_color=TOYOTA_RED, stroke_width=2)
        center_label = txt("トヨタ", size=18, color=TOYOTA_RED, weight=BOLD)
        center = VGroup(center_circle, center_label)
        center.shift(DOWN * 0.3)
        self.play(FadeIn(center), run_time=0.5)

        # 4方向にパワートレイン
        paths = [
            ("HV/PHEV", "ハイブリッド", "現在の主力・最大の強み", CHART_GREEN, UP * 2 + LEFT * 0.5),
            ("BEV", "バッテリーEV", "次世代プラットフォーム開発中", CHART_BLUE, RIGHT * 3.5 + UP * 0.5),
            ("FCEV", "燃料電池（水素）", "MIRAI・商用車展開", CHART_CYAN, DOWN * 2.5 + RIGHT * 0.5),
            ("ICE", "内燃機関", "新興国向け・水素エンジン", CHART_ORANGE, LEFT * 4 + DOWN * 1),
        ]

        for name, desc, detail, col, pos in paths:
            node = panel_rect(w=3.2, h=1.3, color=PANEL)
            n = txt(name, size=18, color=col, weight=BOLD)
            d = txt(desc, size=12, color=SOFT_WHITE)
            dt = txt(detail, size=10, color=LIGHT_GREY)
            content = VGroup(n, d, dt).arrange(DOWN, buff=0.08)
            card = VGroup(node, content)
            card.move_to(pos + DOWN * 0.3)

            conn = Line(
                center.get_center(),
                card.get_center(),
                color=col, stroke_width=1.5, stroke_opacity=0.5,
            )
            self.play(Create(conn), run_time=0.3)
            direction = (pos) / np.linalg.norm(pos) if np.linalg.norm(pos) > 0 else UP
            self.play(FadeIn(card, shift=direction * 0.2), run_time=0.6)
            self.wait(0.5)

        note = txt("市場環境に応じて最適解を提供 → リスク分散", size=16, color=GOLD)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. 財務推移
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class FinancialGrowthScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("FINANCIAL GROWTH", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("売上高と営業利益の推移", size=22, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.4)

        # 年度データ
        years = ["FY20", "FY21", "FY22", "FY23", "FY24"]
        revenues = [29.9, 27.2, 31.4, 37.2, 45.1]
        profits = [2.4, 2.2, 3.0, 2.7, 5.35]

        # 軸
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 50, 10],
            x_length=10, y_length=4.5,
            tips=False,
            axis_config={"color": DIM, "stroke_width": 1},
            y_axis_config={"include_numbers": False},
        ).shift(DOWN * 0.3)

        # Y軸ラベル
        for val in [10, 20, 30, 40, 50]:
            lbl = txt(f"{val}", size=10, color=LIGHT_GREY)
            lbl.next_to(axes.c2p(0, val), LEFT, buff=0.15)
            axes.add(lbl)

        y_unit = txt("兆円", size=10, color=LIGHT_GREY)
        y_unit.next_to(axes.c2p(0, 50), UP, buff=0.1)
        axes.add(y_unit)

        # X軸ラベル
        for i, yr in enumerate(years):
            lbl = txt(yr, size=11, color=LIGHT_GREY)
            lbl.next_to(axes.c2p(i + 0.5, 0), DOWN, buff=0.15)
            axes.add(lbl)

        self.play(FadeIn(axes), run_time=0.6)

        # 売上棒グラフ
        rev_bars = VGroup()
        for i, val in enumerate(revenues):
            bar = Rectangle(
                width=0.7, height=val * (4.5 / 50),
                fill_color=TOYOTA_RED, fill_opacity=0.5,
                stroke_color=TOYOTA_RED, stroke_width=1,
            )
            bar.move_to(axes.c2p(i + 0.35, 0), aligned_edge=DOWN)
            v = txt(f"{val}", size=10, color=TOYOTA_RED)
            v.next_to(bar, UP, buff=0.05)
            rev_bars.add(VGroup(bar, v))

        # 利益棒グラフ
        profit_bars = VGroup()
        for i, val in enumerate(profits):
            bar = Rectangle(
                width=0.7, height=val * (4.5 / 50),
                fill_color=GOLD, fill_opacity=0.6,
                stroke_color=GOLD, stroke_width=1,
            )
            bar.move_to(axes.c2p(i + 0.75, 0), aligned_edge=DOWN)
            v = txt(f"{val}", size=10, color=GOLD)
            v.next_to(bar, UP, buff=0.05)
            profit_bars.add(VGroup(bar, v))

        # 凡例
        leg_rev_dot = Square(side_length=0.15, fill_color=TOYOTA_RED, fill_opacity=0.5, stroke_width=0)
        leg_rev_t = txt("売上高", size=11, color=TOYOTA_RED)
        leg_pro_dot = Square(side_length=0.15, fill_color=GOLD, fill_opacity=0.6, stroke_width=0)
        leg_pro_t = txt("営業利益", size=11, color=GOLD)
        legend = VGroup(
            VGroup(leg_rev_dot, leg_rev_t).arrange(RIGHT, buff=0.1),
            VGroup(leg_pro_dot, leg_pro_t).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.5)
        legend.to_edge(UR, buff=0.6)
        self.play(FadeIn(legend), run_time=0.3)

        # アニメーション
        for rb, pb in zip(rev_bars, profit_bars):
            self.play(
                GrowFromEdge(rb[0], DOWN), FadeIn(rb[1]),
                GrowFromEdge(pb[0], DOWN), FadeIn(pb[1]),
                run_time=0.5,
            )

        self.wait(1.5)

        note = txt("FY24 は売上・利益ともに過去最高を記録", size=16, color=GOLD)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(3.5)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12. 競争優位のまとめ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CompetitiveEdgeScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        header = txt("WHY #1?", size=14, color=TOYOTA_RED, weight=BOLD)
        header.to_edge(UL, buff=0.6)
        line = accent_line(header.get_left() + DOWN * 0.25,
                           header.get_right() + DOWN * 0.25 + RIGHT * 1)
        self.play(FadeIn(header), Create(line), run_time=0.5)

        sub = txt("トヨタが世界一であり続ける理由", size=26, color=WHITE)
        sub.next_to(header, DOWN, buff=0.5).align_to(header, LEFT)
        self.play(FadeIn(sub), run_time=0.5)

        # 5つの強み
        strengths = [
            ("01", "生産効率", "TPS による圧倒的なコスト競争力", TOYOTA_RED),
            ("02", "品質と信頼性", "世界的な品質評価・リセールバリュー", GOLD),
            ("03", "グローバル分散", "地域偏重のない販売・生産ネットワーク", CHART_BLUE),
            ("04", "技術の全方位", "HV で培った電動化技術の蓄積", CHART_GREEN),
            ("05", "サプライヤー連携", "系列企業との強固な協力体制", CHART_PURPLE),
        ]

        items = VGroup()
        for num, title_t, desc, col in strengths:
            num_t = txt(num, size=28, color=col, weight=BOLD)
            t = txt(title_t, size=18, color=SOFT_WHITE, weight=BOLD)
            d = txt(desc, size=13, color=LIGHT_GREY)
            td = VGroup(t, d).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
            row = VGroup(num_t, td).arrange(RIGHT, buff=0.4)
            accent = Line(row.get_left() + LEFT * 0.1, row.get_left() + LEFT * 0.1,
                          color=col, stroke_width=3)
            items.add(VGroup(accent, row))

        items.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        items.shift(DOWN * 0.4 + LEFT * 1)

        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.7)

        self.wait(3)
        wipe(self)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 13. クロージング
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ClosingScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        red_line = Line(LEFT * 8, RIGHT * 8, color=TOYOTA_RED, stroke_width=3)
        self.play(Create(red_line), run_time=0.8, rate_func=rush_into)
        self.wait(0.3)

        msg1 = txt("トヨタの強さは", size=30, color=WHITE)
        msg2 = txt("「当たり前を極める」ことにある", size=34, color=GOLD, weight=BOLD)
        msg1.next_to(red_line, UP, buff=0.5)
        msg2.next_to(red_line, DOWN, buff=0.5)

        self.play(FadeIn(msg1, shift=DOWN * 0.1), run_time=0.8)
        self.play(FadeIn(msg2, shift=UP * 0.1), run_time=0.8)
        self.wait(1.5)

        note = txt("※ 本動画のデータは FY2024 の公開情報に基づく概算値です", size=12, color=DIM)
        note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(4)
        wipe(self)
