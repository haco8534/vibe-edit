"""
東京は本当に稼げる街なのか？ — ずんだもんとめたんの経済解説
======================================================

台本: projects/tokyo_analysis/script.md

Usage:
  python tools/render_parallel.py tokyo_analysis
"""

from manim import *
import numpy as np

# ============================================================================
# カラー定数（ホワイトテーマ）
# ============================================================================
BG_COLOR = "#f5f5f5"
TEXT_MAIN = "#1a1a2e"        # メインテキスト（濃紺）
ACCENT_RED = "#d6336c"       # 深めローズ（警告・注目）
ACCENT_YELLOW = "#e8590c"    # ディープオレンジ（注意）
ACCENT_BLUE = "#1971c2"      # ディープブルー（データ・冷徹）
ACCENT_GREEN = "#099268"     # ディープグリーン（ポジティブ・地方・ずんだ）
ACCENT_PURPLE = "#7048e8"    # ディープパープル（集積・権力）
TEXT_DIM = "#868e96"         # 薄めグレー
CHAR_METAN = "#d6336c"       # めたんの色
CHAR_ZUNDA = "#099268"       # ずんだもんの色

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

def create_bar_chart(data_dict, title, max_val=None, color=ACCENT_BLUE):
    """シンプルな棒グラフを作成するヘルパー"""
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    if max_val is None:
        max_val = max(values) * 1.1

    bars = VGroup()
    texts = VGroup()
    
    chart_width = 8
    chart_height = 4
    bar_width = (chart_width / len(labels)) * 0.6
    
    axes = Axes(
        x_range=[0, len(labels), 1],
        y_range=[0, max_val, max_val/5],
        x_length=chart_width,
        y_length=chart_height,
        axis_config={"color": TEXT_DIM, "include_tip": False},
        y_axis_config={"include_numbers": True, "font_size": 16, "color": TEXT_DIM}
    ).center()

    title_text = Text(title, font="Noto Sans JP", font_size=32, color=TEXT_MAIN, weight=BOLD)
    title_text.next_to(axes, UP, buff=0.5)

    for i, (label, val) in enumerate(zip(labels, values)):
        bar = Rectangle(
            width=bar_width,
            height=(val / max_val) * chart_height,
            fill_color=color,
            fill_opacity=0.8,
            stroke_width=0
        )
        bar.move_to(axes.c2p(i + 0.5, val / 2))
        bars.add(bar)

        label_text = Text(label, font="Noto Sans JP", font_size=20, color=TEXT_MAIN)
        label_text.next_to(axes.coords_to_point(i + 0.5, 0), DOWN, buff=0.2)
        texts.add(label_text)
        
        val_text = Text(str(val), font_size=18, color=color)
        val_text.next_to(bar, UP, buff=0.1)
        texts.add(val_text)

    return VGroup(title_text, axes, bars, texts)


# ============================================================================
# Scene 01: 導入とパラドックス (0:00〜1:30)
# ============================================================================

class Scene01_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # タイトル
        title = Text("検証：東京は稼げる街なのか？", font="Noto Sans JP", font_size=40, color=TEXT_MAIN, weight=BOLD)
        subtitle = Text("〜 一極集中の光と影 〜", font="Noto Sans JP", font_size=24, color=TEXT_DIM)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        self.play(title.animate.to_edge(UP, buff=0.5), FadeOut(subtitle))

        sub1 = show_subtitle(self, "ずんだもん",
            "「東京ドリーム」って言葉があるのだ！ やっぱり稼ぐなら東京一択なのだ！",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "その幻想、データで打ち砕いて差し上げましょうか？",
            CHAR_METAN, duration=4, prev_sub=sub1)

        # グラフ: 可処分所得
        income_data = {"東京都": 550, "神奈川": 500, "大阪": 450, "全国平均": 420, "沖縄": 350} # 仮の数値イメージ
        chart = create_bar_chart(income_data, "可処分所得ランキング (万円)", max_val=600, color=ACCENT_BLUE)
        chart.scale(0.8).move_to(UP * 0.5)

        self.play(Create(chart[1]), FadeIn(chart[0])) # Axes and Title
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in chart[2]], lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(chart[3])) # Texts

        sub3 = show_subtitle(self, "めたん",
            "確かに、額面の可処分所得は全国1位です",
            CHAR_METAN, duration=4, prev_sub=sub2)

        # 衝撃の事実
        ranking_text = Text("全国1位", font_size=48, color=ACCENT_BLUE, weight=BOLD).move_to(chart[2][0]).shift(UP*0.5+RIGHT*0.5)
        self.play(FadeIn(ranking_text, scale=1.2)) # Transformをやめて確実に管理
        self.wait(1)

        sub4 = show_subtitle(self, "めたん",
            "しかし、ある「コスト」を引くと、東京はなんと…",
            CHAR_METAN, duration=4, prev_sub=sub3)

        worst_text = Text("44位 (ワースト4位)", font_size=64, color=ACCENT_RED, weight=BOLD)
        worst_text.move_to(chart)
        
        # グラフが崩れ落ちるようなアニメーション
        self.play(
            FadeOut(chart), FadeOut(ranking_text),
            FadeIn(worst_text, scale=0.5),
            run_time=1.5
        )

        sub5 = show_subtitle(self, "ずんだもん",
            "えええ！？ ワースト4位？ 一体何が起きてるのだ？",
            CHAR_ZUNDA, duration=4, prev_sub=sub4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 02: 東京の「見えないコスト」 (1:30〜3:30)
# ============================================================================

class Scene02_Cost(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("東京の「見えないコスト」", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.2) # 少し上へ
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "めたん",
            "キーワードは2つ。「異常な家賃」と「通勤時間の損失」です",
            CHAR_METAN, duration=5)

        # 天秤のような比較アニメーション: 家賃
        left_plate = VGroup(Text("全国平均", font_size=20, color=TEXT_DIM), Square(color=TEXT_DIM, fill_opacity=0.5))
        right_plate = VGroup(Text("東京都", font_size=20, color=ACCENT_RED), Rectangle(height=2, width=1, color=ACCENT_RED, fill_opacity=0.8))
        
        balance_group = VGroup(left_plate, right_plate).arrange(RIGHT, buff=2)
        balance_group.move_to(UP * 1.0) # UP 1.5 -> 1.0 に戻して見出しとの干渉回避
        
        rent_label = Text("家賃相場", font="Noto Sans JP", font_size=24, color=TEXT_MAIN).next_to(balance_group, UP)

        self.play(FadeIn(rent_label), FadeIn(balance_group))

        sub2 = show_subtitle(self, "ずんだもん",
            "うぐぐ…確かに東京の部屋は狭くて高いのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        # 通勤時間のアニメーション
        # 時計
        clock = Circle(color=TEXT_MAIN)
        hand = Line(ORIGIN, UP * 0.8, color=ACCENT_RED)
        clock_group = VGroup(clock, hand).next_to(balance_group, DOWN, buff=0.5)
        
        time_text = Text("通勤時間: 往復90分", font="Noto Sans JP", font_size=24, color=ACCENT_RED).next_to(clock_group, RIGHT)

        self.play(FadeIn(clock_group), FadeIn(time_text))
        self.play(Rotate(hand, angle=-2*PI * 2, about_point=clock.get_center()), run_time=2) # 2回転

        loss_text = Text("月5.8万円の損失", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        loss_text.next_to(time_text, DOWN)
        
        self.play(Write(loss_text))

        sub3 = show_subtitle(self, "めたん",
            "通勤時間を時給換算すると、月5.8万円も捨てていることになります",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 結論の不等式 (MathTexは避けてTextで作成)
        formula = Text("所得 - (生活費 + 通勤損失) =", font="Noto Sans JP", font_size=36, color=TEXT_MAIN)
        rank_down = Text("44位", font_size=48, color=ACCENT_RED, weight=BOLD)
        equation = VGroup(formula, rank_down).arrange(RIGHT).move_to(DOWN * 1.5) # DOWN 0.5 -> 1.5 (字幕の上、かつ時計の下)

        self.play(FadeIn(equation[0]))
        self.play(Write(equation[1]), run_time=1)

        sub4 = show_subtitle(self, "ずんだもん",
            "働いても働いても、時間と家賃に消えていく…「ラットレース」なのだ…",
            CHAR_ZUNDA, duration=6, prev_sub=sub3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 03: なぜ人は集まるのか？（集積の経済） (3:30〜5:30)
# ============================================================================

class Scene03_Aggregation(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("なぜ人は集まるのか？（集積の経済）", font="Noto Sans JP", font_size=32, color=ACCENT_PURPLE, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "ずんだもん",
            "だったらみんな地方に行けばいいのだ。なんで東京に人が集まり続けるのだ？",
            CHAR_ZUNDA, duration=5)

        # 磁石のアニメーション (位置調整)
        # 円を小さくし、位置を下げることでセクションタイトルとの重なりを防ぐ
        magnet_pos = UP * 0.5
        magnet = Text("集積メリット", font_size=24, color=ACCENT_RED, weight=BOLD).move_to(magnet_pos)
        magnet_circle = Circle(radius=1.5, color=ACCENT_RED, fill_opacity=0.1).move_to(magnet_pos) # 半径 2 -> 1.5
        
        # 散らばる企業たち
        companies = VGroup(*[Square(side_length=0.3, color=ACCENT_BLUE, fill_opacity=0.8) for _ in range(10)])
        # ランダム配置（ただし円の外）
        for comp in companies:
            angle = np.random.uniform(0, 2*PI)
            dist = np.random.uniform(2.5, 4) # 距離も調整
            # 中心をmagnetの位置に合わせる
            comp.move_to(magnet.get_center() + np.array([dist * np.cos(angle), dist * np.sin(angle), 0]))

        sub2 = show_subtitle(self, "めたん",
            "会社が一箇所に集まると、取引コストが減るからです",
            CHAR_METAN, duration=4, prev_sub=sub1)

        self.play(FadeIn(magnet), FadeIn(magnet_circle), FadeIn(companies))
        
        # 吸い寄せられるアニメーション (中心はmagnet.get_center())
        self.play(
            *[comp.animate.move_to(magnet.get_center() + (comp.get_center() - magnet.get_center()) * 0.1) for comp in companies], # 中心へ近づく
            run_time=2, rate_func=rush_into
        )

        # ネットワーク線の生成
        lines = VGroup()
        for i in range(len(companies)):
            for j in range(i+1, len(companies)):
                if np.random.random() < 0.3: # 30%の確率で繋がる
                    l = Line(companies[i].get_center(), companies[j].get_center(), color=ACCENT_YELLOW, stroke_width=1, stroke_opacity=0.5)
                    lines.add(l)
        
        self.play(Create(lines), run_time=2)

        sub3 = show_subtitle(self, "めたん",
            "情報の共有もしやすくなり、優秀な人材も見つけやすくなります",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 知の中枢機能
        center_text = Text("知の中枢機能", font_size=36, color=TEXT_MAIN, weight=BOLD).next_to(magnet_circle, UP, buff=0.1) # タイトル下, buff小さく
        
        # アイコン（テキストで代用）
        icons = VGroup(
            Text("銀行 (カネ)", font_size=20, color=ACCENT_GREEN),
            Text("メディア (情報)", font_size=20, color=ACCENT_BLUE),
            Text("商社 (モノ)", font_size=20, color=ACCENT_PURPLE),
            Text("大学 (ヒト)", font_size=20, color=ACCENT_RED),
        ).arrange(RIGHT, buff=0.5)
        # 円の下に配置
        icons.next_to(magnet_circle, DOWN, buff=0.2)

        self.play(Transform(magnet, center_text), FadeOut(magnet_circle), FadeOut(companies), FadeOut(lines))
        self.play(FadeIn(icons))

        sub4 = show_subtitle(self, "ずんだもん",
            "なるほど、単なる工場地帯じゃなくて、頭脳が集まっているから強いのだ",
            CHAR_ZUNDA, duration=5, prev_sub=sub3)
        
        sub5 = show_subtitle(self, "めたん",
            "逆に言えば、「頭脳を使って稼ぐ人」以外には、東京はただコストが高いだけの残酷な街とも言えます",
            CHAR_METAN, duration=6, prev_sub=sub4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 04: 一極集中の歴史的背景 (5:30〜7:30)
# ============================================================================

class Scene04_History(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("一極集中の歴史的背景", font="Noto Sans JP", font_size=32, color=TEXT_DIM, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "めたん",
            "実は戦前は「大大阪時代」と呼ばれるほど、大阪が経済の中心でした",
            CHAR_METAN, duration=5)

        # 簡易日本地図（位置を上げる）
        map_outline = VGroup(
            Ellipse(width=6, height=3, color=TEXT_DIM), # 本州イメージ
            Ellipse(width=2, height=2, color=TEXT_DIM).shift(LEFT*3 + DOWN*1) # 九州イメージ
        ).scale(0.8).move_to(UP * 0.5)

        osaka_dot = Dot(color=ACCENT_RED, radius=0.2).move_to(map_outline.get_center() + LEFT * 1 + DOWN * 0.2)
        osaka_label = Text("大阪", font_size=24, color=ACCENT_RED).next_to(osaka_dot, DOWN)
        
        tokyo_dot = Dot(color=ACCENT_BLUE, radius=0.2).move_to(map_outline.get_center() + RIGHT * 1 + UP * 0.2)
        tokyo_label = Text("東京", font_size=24, color=ACCENT_BLUE).next_to(tokyo_dot, UP)

        self.play(Create(map_outline))
        self.play(FadeIn(osaka_dot), FadeIn(osaka_label))
        
        # 光り輝く大阪
        flash = Flash(osaka_dot, color=ACCENT_RED, line_length=0.5, num_lines=12)
        self.play(flash)

        sub2 = show_subtitle(self, "ずんだもん",
            "えっ、昔は東京一強じゃなかったのだ？",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        # 逆転の理由リスト
        reasons = VGroup(
            Text("1. 地形 (関東平野の広さ)", font="Noto Sans JP", font_size=24, color=TEXT_MAIN),
            Text("2. 権力 (中央集権)", font="Noto Sans JP", font_size=24, color=TEXT_MAIN),
            Text("3. 交通 (新幹線・空港)", font="Noto Sans JP", font_size=24, color=TEXT_MAIN),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        reasons.to_edge(RIGHT, buff=0.5).shift(UP*1)

        self.play(Write(reasons[0]))
        self.play(Write(reasons[1]))
        
        # 東京へのシフト
        self.play(
            osaka_dot.animate.set_color(TEXT_DIM), osaka_label.animate.set_color(TEXT_DIM),
            FadeIn(tokyo_dot), FadeIn(tokyo_label)
        )
        flash_tokyo = Flash(tokyo_dot, color=ACCENT_BLUE, line_length=0.8, num_lines=16) 
        self.play(flash_tokyo)

        sub3 = show_subtitle(self, "めたん",
            "インフラが東京中心に整備されたことで、「ストロー現象」が起きました",
            CHAR_METAN, duration=5, prev_sub=sub2)

        self.play(Write(reasons[2]))

        # ストロー現象アニメーション（矢印が地方から東京へ）
        arrows = VGroup()
        for angle in np.linspace(0, 2*PI, 8):
            start = tokyo_dot.get_center() + np.array([3*np.cos(angle), 3*np.sin(angle), 0])
            arrow = Arrow(start, tokyo_dot.get_center(), buff=0.2, color=ACCENT_YELLOW)
            arrows.add(arrow)
        
        self.play(ShowPassingFlash(arrows.set_color(ACCENT_YELLOW), time_width=0.5, run_time=2))
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 05: 最大の利得者は誰か？（構造的搾取） (7:30〜10:00)
# ============================================================================

class Scene05_Landowner(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("最大の利得者は誰か？", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "ずんだもん",
            "結局、東京で頑張って働いて、一体誰が得をしているのだ？",
            CHAR_ZUNDA, duration=5)

        # ピラミッド図解 (位置調整)
        # 背景が薄いので、文字は濃い色にする。図形の透過度を調整。
        pyramid = VGroup()
        base_width = 6
        height = 4
        
        # Bottom (Layer 1)
        p1 = Polygon(
            [-base_width/2, -height/2, 0], [base_width/2, -height/2, 0],
            [base_width*0.3, -height/6, 0], [-base_width*0.3, -height/6, 0],
            color=TEXT_MAIN, fill_color=TEXT_DIM, fill_opacity=0.5
        )
        
        # Middle (Layer 2)
        p2 = Polygon(
            [-base_width*0.3, -height/6, 0], [base_width*0.3, -height/6, 0],
            [base_width*0.1, height/6, 0], [-base_width*0.1, height/6, 0],
            color=TEXT_MAIN, fill_color=ACCENT_BLUE, fill_opacity=0.6 # 少し濃く
        )
        
        # Top (Layer 3)
        p3 = Polygon(
            [-base_width*0.1, height/6, 0], [base_width*0.1, height/6, 0],
            [0, height/2, 0],
            color=TEXT_MAIN, fill_color=ACCENT_RED, fill_opacity=0.7 # 少し濃く
        )
        
        # 位置決定: UP * 0.5 
        
        # テキスト (色をTEXT_MAINに変更して視認性向上)
        text1 = Text("労働者 (満員電車)", font_size=20, color=TEXT_MAIN).move_to(p1.get_center() + UP*0.5)
        text2 = Text("企業 (利益)", font_size=20, color=TEXT_MAIN).move_to(p2.get_center() + UP*0.5)
        text3 = Text("地主", font_size=24, color=TEXT_MAIN, weight=BOLD).move_to(p3.get_center() + UP*0.5).shift(DOWN*0.1)
        
        pyramid_group = VGroup(p1, p2, p3, text1, text2, text3).move_to(UP * 0.5)

        self.play(FadeIn(pyramid_group))

        sub2 = show_subtitle(self, "めたん",
            "私たちが生み出した利益は、最終的に「高い家賃」として地主に吸い上げられます",
            CHAR_METAN, duration=6, prev_sub=sub1)

        # お金の流れアニメーション
        money = Text("￥", font_size=24, color=ACCENT_YELLOW)
        
        # pyramid_group内の要素インデックス: p1=0, p2=1, p3=2, t1=3, t2=4, t3=5
        target_p1 = pyramid_group[0]
        target_p2 = pyramid_group[1]
        target_p3 = pyramid_group[2]
        
        self.play(money.animate.move_to(target_p1), run_time=0.1)
        self.play(money.animate.move_to(target_p2), run_time=0.5)
        self.play(money.animate.move_to(target_p3), run_time=0.5)
        self.play(Indicate(pyramid_group[5], color=ACCENT_YELLOW, scale_factor=1.5)) # text3

        sub3 = show_subtitle(self, "ずんだもん",
            "ひえええ！ 汗水たらして働いた分が、ただ土地を持ってるだけの人に行くなんて！",
            CHAR_ZUNDA, duration=5, prev_sub=sub2)

        # ヘンリー・ジョージの定理
        theorem = Text("ヘンリー・ジョージの定理", font_size=36, color=ACCENT_RED, weight=BOLD)
        theorem.next_to(pyramid_group, DOWN, buff=0.5) # subtitleと被るか？
        # pyramidはUP*0.5でheight=4なので、bottomは UP*0.5 - 2 = DOWN*1.5
        # next_to DOWN buff=0.5 -> DOWN*2.0
        # 字幕は DOWN*2.5 〜 DOWN*3.5
        # 微妙に被る。pyramidをもっと上げるか、theoremを横に置くか。
        # Pyramidを scale(0.8) して UP*1.0 にする
        
        self.play(FadeOut(pyramid_group), FadeOut(money), run_time=0.5)
        
        # 修正版ピラミッド
        pyramid_group.scale(0.8).move_to(UP * 1.5)
        theorem.next_to(pyramid_group, DOWN, buff=0.5)
        
        self.play(FadeIn(pyramid_group), Write(theorem))

        sub4 = show_subtitle(self, "めたん",
            "これが「ヘンリー・ジョージの定理」。東京という競争に参加するか、地方で生きるか、選ぶのはあなたです",
            CHAR_METAN, duration=7, prev_sub=sub3)

