"""
APIとは何か？ — エンジニア初学者向け解説アニメーション
================================================

台本: scenes/api_explanation_script.md

Usage:
  manim -qm scenes/api_explanation_animation.py Scene01_Intro
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


def get_labeled_box(label, color, width=2.5, height=1.0, font_size=24):
    """ラベル付きの四角形を返す"""
    box = RoundedRectangle(
        corner_radius=0.1, width=width, height=height,
        fill_color=WHITE, fill_opacity=0.9, stroke_color=color, stroke_width=2
    )
    text = Text(label, font="Noto Sans JP", font_size=font_size, color=color)
    text.move_to(box)
    return VGroup(box, text)


# ============================================================================
# Scene 01: イントロダクション (0:00〜1:15)
# ============================================================================

class Scene01_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # タイトル表示
        title = Text("API とは何か？", font="Noto Sans JP", font_size=48, color=TEXT_MAIN, weight=BOLD)
        subtitle = Text("Application Programming Interface", font="Noto Sans JP", font_size=24, color=TEXT_DIM)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)
        
        self.play(title.animate.to_edge(UP, buff=0.5), FadeOut(subtitle))

        sub1 = show_subtitle(self, "ずんだもん",
            "「API」って言葉、最近どこでも聞くのだ。でも実は何なのか全然わかってないのだ…",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "エンジニアを目指すなら避けては通れない道ですわね",
            CHAR_METAN, duration=4, prev_sub=sub1)

        # APIの文字分解
        api_text = Text("API", font_size=72, color=ACCENT_BLUE, weight=BOLD)
        api_text.move_to(UP * 0.5)
        self.play(FadeIn(api_text, scale=0.5), run_time=0.8)

        sub3 = show_subtitle(self, "ずんだもん",
            "「アプリ・プロ…」なんだっけ？",
            CHAR_ZUNDA, duration=3, prev_sub=sub2)

        full_text = VGroup(
            Text("Application", font_size=36, color=ACCENT_RED),
            Text("Programming", font_size=36, color=ACCENT_YELLOW),
            Text("Interface", font_size=36, color=ACCENT_GREEN)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        full_text.next_to(api_text, RIGHT, buff=1.0)

        sub4 = show_subtitle(self, "めたん",
            "「Application Programming Interface」ですわ",
            CHAR_METAN, duration=4, prev_sub=sub3)

        self.play(
            api_text.animate.shift(LEFT * 2),
            LaggedStart(*[FadeIn(t, shift=LEFT) for t in full_text], lag_ratio=0.3),
            run_time=2
        )

        sub5 = show_subtitle(self, "ずんだもん",
            "長いのだ！ 日本語でおｋなのだ",
            CHAR_ZUNDA, duration=3, prev_sub=sub4)

        jp_text = Text("アプリをプログラムで繋ぐための「窓口」", font="Noto Sans JP",
                      font_size=28, color=TEXT_MAIN)
        jp_text.next_to(full_text, DOWN, buff=0.8)
        jp_text.set_x(0)

        sub6 = show_subtitle(self, "めたん",
            "直訳すると「アプリをプログラムで繋ぐための窓口」ですわ",
            CHAR_METAN, duration=5, prev_sub=sub5)

        self.play(FadeIn(jp_text), run_time=1)
        self.wait(1)

        sub7 = show_subtitle(self, "めたん",
            "今日はこれを徹底的に噛み砕いて説明しますわよ",
            CHAR_METAN, duration=4, prev_sub=sub6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 02: レストランの比喩 (1:15〜2:45)
# ============================================================================

class Scene02_Restaurant(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("APIの役割 = ウェイター", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "まずはイメージから入りましょう。レストランに行ったことは？",
            CHAR_METAN, duration=5)

        sub2 = show_subtitle(self, "ずんだもん",
            "もちなのだ！ ずんだ餅食べ放題によく行くのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        # レストランの構成
        customer = Circle(radius=0.5, color=ACCENT_BLUE, fill_opacity=0.5)
        customer_label = Text("客席 (You)", font_size=16, color=TEXT_MAIN).next_to(customer, DOWN)
        customer_group = VGroup(customer, customer_label).to_edge(LEFT, buff=1.5)

        kitchen = Rectangle(width=2, height=3, color=ACCENT_YELLOW, fill_opacity=0.2)
        kitchen_label = Text("キッチン", font_size=20, color=TEXT_MAIN).move_to(kitchen)
        kitchen_group = VGroup(kitchen, kitchen_label).to_edge(RIGHT, buff=1.5)
        
        waiter = Triangle(color=ACCENT_GREEN, fill_opacity=0.5).scale(0.5).rotate(-PI/2) # 左向き
        waiter_label = Text("ウェイター", font_size=16, color=TEXT_MAIN).next_to(waiter, DOWN)
        waiter_group = VGroup(waiter, waiter_label).move_to(ORIGIN)

        self.play(
            FadeIn(customer_group),
            FadeIn(kitchen_group),
            run_time=1.5
        )

        sub3 = show_subtitle(self, "めたん",
            "客席から直接キッチンに入って勝手に冷蔵庫を開けますか？",
            CHAR_METAN, duration=5, prev_sub=sub2)

        dashed_arrow = DashedLine(customer.get_right(), kitchen.get_left(), color=ACCENT_RED)
        cross_mark = Cross(dashed_arrow, scale_factor=0.5)

        self.play(Create(dashed_arrow), run_time=1)
        self.play(Create(cross_mark), run_time=0.5)

        sub4 = show_subtitle(self, "ずんだもん",
            "そんなことしたら怒られるのだ！ 衛生的にアウトなのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub3)

        self.play(FadeOut(dashed_arrow), FadeOut(cross_mark))

        sub5 = show_subtitle(self, "めたん",
            "そう、だから間に「メニュー」と「ウェイター」がいますわね",
            CHAR_METAN, duration=5, prev_sub=sub4)

        menu = Text("📋メニュー", font="Noto Sans JP", font_size=24, color=TEXT_MAIN)
        menu.next_to(waiter_group, UP, buff=0.5)
        
        self.play(FadeIn(waiter_group), FadeIn(menu), run_time=1)
        self.wait(1)

        # 注文の流れ
        order = Text("📩注文", font="Noto Sans JP", font_size=20, color=ACCENT_BLUE)
        order.next_to(customer, UP)
        
        # 客 -> ウェイター
        self.play(FadeIn(order))
        self.play(order.animate.move_to(waiter.get_left() + LEFT * 0.2), run_time=1)
        self.wait(0.5)
        
        # ウェイター -> キッチン
        self.play(
            waiter_group.animate.shift(RIGHT * 1),
            order.animate.move_to(kitchen.get_left() + LEFT * 0.2),
            run_time=1
        )
        self.play(FadeOut(order)) # キッチンが受け取る

        sub6 = show_subtitle(self, "めたん",
            "「注文（リクエスト）」を受け取って、キッチンに伝え、料理を運ぶ",
            CHAR_METAN, duration=6, prev_sub=sub5)

        # 料理が出る
        food = Text("🍱料理", font="Noto Sans JP", font_size=24, color=ACCENT_YELLOW)
        food.move_to(kitchen.get_left())
        
        self.play(FadeIn(food))
        self.play(
            waiter_group.animate.move_to(ORIGIN),
            food.animate.move_to(customer.get_right() + RIGHT * 0.5),
            run_time=1.5
        )

        sub7 = show_subtitle(self, "ずんだもん",
            "ウェイターさんがAPI？",
            CHAR_ZUNDA, duration=3, prev_sub=sub6)

        api_label = Text("API", font_size=32, color=ACCENT_RED, weight=BOLD)
        api_label.next_to(waiter_group, UP, buff=0.1)
        self.play(Transform(menu, api_label))

        sub8 = show_subtitle(self, "めたん",
            "お客さんはキッチンの作り方を知らなくても、ルール通りに頼めば料理が出てくる",
            CHAR_METAN, duration=6, prev_sub=sub7)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 03: インターフェースとは？ (2:45〜4:00)
# ============================================================================

class Scene03_Interface(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("Interface = 接点・境界面", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "「Interface」は「接点」や「境界面」という意味です",
            CHAR_METAN, duration=5)

        sub2 = show_subtitle(self, "ずんだもん",
            "USBとかもインターフェースって言うのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        # ブラックボックスとUSB
        box = Rectangle(width=4, height=3, fill_color=BLACK, fill_opacity=0.8)
        box_label = Text("複雑な中身\n(Black Box)", font="Noto Sans JP", font_size=24, color=WHITE)
        box_label.move_to(box)
        
        port = Rectangle(width=1.5, height=0.5, color=GREY_A, fill_color=WHITE, fill_opacity=1)
        port.next_to(box, RIGHT, buff=0)
        port_label = Text("USB端子", font="Noto Sans JP", font_size=16, color=TEXT_DIM)
        port_label.next_to(port, DOWN)

        group = VGroup(box, box_label, port, port_label).move_to(ORIGIN)
        
        self.play(FadeIn(group), run_time=1.5)

        sub3 = show_subtitle(self, "めたん",
            "その通り。中身を知らなくても、あの四角い穴（端子）に挿せば使えますわよね？",
            CHAR_METAN, duration=6, prev_sub=sub2)

        usb_device = RoundedRectangle(width=2, height=0.5, corner_radius=0.1, color=ACCENT_BLUE, fill_opacity=0.6)
        usb_label = Text("USBメモリ", font="Noto Sans JP", font_size=16, color=WHITE)
        usb_label.move_to(usb_device)
        usb_device_group = VGroup(usb_device, usb_label).next_to(port, RIGHT, buff=2)

        self.play(FadeIn(usb_device_group))
        self.play(usb_device_group.animate.next_to(port, RIGHT, buff=0.1), run_time=1)
        self.wait(1)

        flash = Flash(port, color=ACCENT_YELLOW, line_length=0.3)
        self.play(flash)

        sub4 = show_subtitle(self, "めたん",
            "外から簡単に使える「取っ手」や「窓口」。それをプログラム用に用意したのがAPIです",
            CHAR_METAN, duration=7, prev_sub=sub3)

        api_tag = Text("API", font_size=48, color=ACCENT_RED, weight=BOLD)
        api_tag.next_to(port, UP, buff=0.5)
        self.play(FadeIn(api_tag, shift=DOWN), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 04: Web APIの仕組み (4:00〜6:00)
# ============================================================================

class Scene04_WebAPI(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("Web APIの仕組み", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "現代の開発で最も使われる「Web API」を例に見ましょう",
            CHAR_METAN, duration=5)

        # クライアント(スマホ)とサーバー
        client = RoundedRectangle(width=1.5, height=2.5, corner_radius=0.2, color=ACCENT_BLUE, fill_opacity=0.1)
        client_screen = Rectangle(width=1.2, height=2.0, color=ACCENT_BLUE).move_to(client)
        client_label = Text("Client", font_size=20, color=TEXT_DIM).next_to(client, DOWN)
        client_group = VGroup(client, client_screen, client_label).to_edge(LEFT, buff=1.5)

        server = VGroup(
            RoundedRectangle(width=2, height=1, color=ACCENT_GREEN, fill_opacity=0.2),
            RoundedRectangle(width=2, height=1, color=ACCENT_GREEN, fill_opacity=0.2),
            RoundedRectangle(width=2, height=1, color=ACCENT_GREEN, fill_opacity=0.2)
        ).arrange(UP, buff=0)
        server_label = Text("Server", font_size=20, color=TEXT_DIM).next_to(server, DOWN)
        server_group = VGroup(server, server_label).to_edge(RIGHT, buff=1.5)

        self.play(FadeIn(client_group), FadeIn(server_group), run_time=1.5)

        sub2 = show_subtitle(self, "ずんだもん",
            "スマホからサーバーにお願いするのだ？",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        req_arrow = Arrow(client.get_right(), server.get_left(), buff=0.5, color=ACCENT_BLUE)
        req_label = Text("HTTP Request", font_size=18, color=ACCENT_BLUE).next_to(req_arrow, UP)

        self.play(GrowArrow(req_arrow), FadeIn(req_label), run_time=1)

        sub3 = show_subtitle(self, "めたん",
            "ええ。「HTTPリクエスト」には4つの重要な要素があります",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 4要素の解説
        list_group = VGroup()
        items = [
            ("Endpoint", "どこに？ (URL)", ACCENT_PURPLE),
            ("Method", "何を？ (GET/POST)", ACCENT_YELLOW),
            ("Header", "付加情報 (鍵など)", ACCENT_CYAN),
            ("Body", "中身 (データ)", ACCENT_RED),
        ]
        
        for en, ja, col in items:
            t = VGroup(
                Text(en, font_size=22, color=col, weight=BOLD),
                Text(ja, font="Noto Sans JP", font_size=20, color=TEXT_MAIN)
            ).arrange(RIGHT, buff=0.3)
            list_group.add(t)
        
        list_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        list_group.move_to(UP * 0.5)

        # 一旦矢印たちを薄くする
        self.play(
            req_arrow.animate.set_opacity(0.2),
            req_label.animate.set_opacity(0.2),
            client_group.animate.to_edge(LEFT, buff=0.5),
            server_group.animate.to_edge(RIGHT, buff=0.5),
            run_time=1
        )
        
        self.play(Write(list_group), run_time=3)
        self.wait(2)

        sub4 = show_subtitle(self, "めたん",
            "「GET /users/zundamon」なら「ずんだもんの情報をください」という依頼になります",
            CHAR_METAN, duration=6, prev_sub=sub3)

        example_req = Text("GET /api/users/zundamon", font_size=28, color=ACCENT_BLUE, weight=BOLD)
        example_req.next_to(list_group, DOWN, buff=0.5)
        
        self.play(FadeIn(example_req, shift=UP * 0.2))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 05: JSONデータ (6:00〜7:30)
# ============================================================================

class Scene05_JSON(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("JSON (JavaScript Object Notation)", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "ずんだもん",
            "じゃあ、サーバーからは何が返ってくるのだ？ 画像？ HTML？",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "Web APIでは主に「JSON」というテキストデータが返ります",
            CHAR_METAN, duration=5, prev_sub=sub1)

        # JSONコードの表示
        json_str = """{
  "name": "ずんだもん",
  "age": 5,
  "favorite": "ずんだ餅",
  "skills": ["弓道", "変身"],
  "is_human": false
}"""
        # JSONコードの表示 (Textオブジェクトで代用)
        json_str_display = """{
  "name": "ずんだもん",
  "age": 5,
  "favorite": "ずんだ餅",
  "skills": ["弓道", "変身"],
  "is_human": false
}"""
        text_obj = Text(json_str_display, font="Consolas", font_size=24, color=TEXT_MAIN, line_spacing=1.2)
        bg_rect = SurroundingRectangle(text_obj, color=TEXT_DIM, fill_color=WHITE, fill_opacity=0.9, corner_radius=0.1, buff=0.2)
        code_group = VGroup(bg_rect, text_obj)
        
        code_group.next_to(section, DOWN, buff=0.5)

        self.play(FadeIn(code_group), run_time=1.5)
        self.wait(1)

        sub3 = show_subtitle(self, "ずんだもん",
            "おお、なんか読めるのだ！ 「名前：ずんだもん」って書いてあるのだ",
            CHAR_ZUNDA, duration=5, prev_sub=sub2)

        # ハイライト用の枠（Codeオブジェクトの構造依存を避けるためコメントアウト）
        # highlight_rect = SurroundingRectangle(code_obj.code.chars[0][3:19], color=ACCENT_RED, buff=0.05)
        
        # ハイライト用の矢印
        arrow = Arrow(RIGHT*2.5, code_group.get_right() + UP*0.5, color=ACCENT_RED)
        label = Text("Key: Value のペア", font="Noto Sans JP", font_size=20, color=ACCENT_RED)
        label.next_to(arrow, LEFT, buff=0.1)

        self.play(GrowArrow(arrow), FadeIn(label))
        self.wait(1)

        sub4 = show_subtitle(self, "めたん",
            "これがJSONです。人間にも読みやすく、プログラムでも扱いやすい形式なんです",
            CHAR_METAN, duration=6, prev_sub=sub3)

        sub5 = show_subtitle(self, "ずんだもん",
            "これなら僕のアプリでも簡単に取り込めそうなのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 06: ステータスコードとエラー (7:30〜8:30)
# ============================================================================

class Scene06_StatusCode(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("Status Code (ステータスコード)", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "めたん",
            "サーバーは必ず「ステータスコード」という番号で結果を教えてくれます",
            CHAR_METAN, duration=6)

        # コード一覧
        codes = [
            ("200 OK", "成功！", ACCENT_GREEN),
            ("404 Not Found", "見つからない…", ACCENT_YELLOW),
            ("500 Internal Server Error", "サーバーのエラー", ACCENT_RED),
        ]

        group = VGroup()
        for code, desc, col in codes:
            row = VGroup(
                Text(code, font_size=36, color=col, weight=BOLD),
                Text(desc, font="Noto Sans JP", font_size=24, color=TEXT_MAIN)
            ).arrange(RIGHT, buff=0.5)
            # 背景枠
            bg = SurroundingRectangle(row, color=col, fill_color=col, fill_opacity=0.1, buff=0.2, stroke_width=0)
            group.add(VGroup(bg, row))
        
        group.arrange(DOWN, buff=0.4).move_to(UP * 0.5)

        for item in group:
            self.play(FadeIn(item, shift=UP * 0.2), run_time=0.8)
            self.wait(0.5)

        sub2 = show_subtitle(self, "ずんだもん",
            "「404」ってよく見るあれなのだ！",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        # 404を強調
        self.play(
            group[0].animate.set_opacity(0.3),
            group[2].animate.set_opacity(0.3),
            group[1].animate.scale(1.2),
            run_time=1
        )

        sub3 = show_subtitle(self, "めたん",
            "「指定されたエンドポイント（住所）にリソースがないよ」という返事です",
            CHAR_METAN, duration=5, prev_sub=sub2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 07: なぜAPIが必要？ (8:30〜10:00)
# ============================================================================

class Scene07_WhyAPI(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("Why API? (APIのメリット)", font="Noto Sans JP", font_size=32, color=ACCENT_RED, weight=BOLD)
        section.to_edge(UP, buff=0.5)
        self.play(FadeIn(section), run_time=0.8)

        sub1 = show_subtitle(self, "ずんだもん",
            "仕組みはわかったけど、自分で全部作ればいいんじゃないのだ？",
            CHAR_ZUNDA, duration=5)

        sub2 = show_subtitle(self, "めたん",
            "例えば、アプリに「地図」を表示したいとします。世界中の測量をしますか？",
            CHAR_METAN, duration=6, prev_sub=sub1)

        map_icon = Text("🗺️", font_size=64).move_to(UP * 1.5)
        self.play(FadeIn(map_icon))

        sub3 = show_subtitle(self, "ずんだもん",
            "無理なのだ！ 死んじゃうのだ",
            CHAR_ZUNDA, duration=3, prev_sub=sub2)

        # ブロック積みアニメーション
        base = Rectangle(width=6, height=1.5, color=TEXT_DIM, fill_color=WHITE, fill_opacity=1)
        base_label = Text("Your Application", font_size=24, color=TEXT_MAIN).move_to(base)
        base_group = VGroup(base, base_label).to_edge(DOWN, buff=1.5)

        api1 = get_labeled_box("Google Maps API", ACCENT_BLUE, width=2.5, height=1)
        api2 = get_labeled_box("Stripe API (決済)", ACCENT_PURPLE, width=2.5, height=1)
        api3 = get_labeled_box("OpenAI API", ACCENT_GREEN, width=2.5, height=1)

        api_group = VGroup(api1, api2, api3).arrange(RIGHT, buff=0.2)
        api_group.next_to(base_group, UP, buff=0)

        self.play(FadeIn(base_group), run_time=1)
        self.play(FadeOut(map_icon)) # マップアイコン消す

        sub4 = show_subtitle(self, "めたん",
            "Google Maps APIなどを使えば、巨人の肩に乗ることができます",
            CHAR_METAN, duration=5, prev_sub=sub3)

        self.play(
            FadeIn(api1, shift=DOWN),
            FadeIn(api2, shift=DOWN),
            FadeIn(api3, shift=DOWN),
            run_time=1.5
        )

        wheel_text = Text("🚫 車輪の再発明を防ぐ", font="Noto Sans JP", font_size=28, color=ACCENT_RED)
        wheel_text.next_to(api_group, UP, buff=0.5)
        self.play(FadeIn(wheel_text))

        sub5 = show_subtitle(self, "めたん",
            "これが「車輪の再発明」を防ぐということ。効率開発の基本です",
            CHAR_METAN, duration=6, prev_sub=sub4)

        sub6 = show_subtitle(self, "ずんだもん",
            "APIって、世界中の便利な機能を繋ぐ魔法のパイプみたいなものなのだ！",
            CHAR_ZUNDA, duration=6, prev_sub=sub5)

        # Security
        db_icon = Cylinder(radius=0.5, height=1, color=TEXT_DIM, fill_opacity=0.5).to_edge(RIGHT, buff=1)
        db_label = Text("Database", font_size=16, color=TEXT_DIM).next_to(db_icon, DOWN)
        db_group = VGroup(db_icon, db_label)
        
        wall = Rectangle(width=0.2, height=3, fill_color=TEXT_MAIN, fill_opacity=0.8)
        wall.next_to(db_icon, LEFT, buff=0.5)
        wall_label = Text("API Wall", font_size=16, color=WHITE).rotate(PI/2).move_to(wall)
        
        security_text = Text("セキュリティ保護", font="Noto Sans JP", font_size=20, color=ACCENT_GREEN)
        security_text.next_to(wall, UP)

        self.play(
            base_group.animate.to_edge(LEFT, buff=0.5).scale(0.8),
            api_group.animate.next_to(base_group, UP, buff=0).scale(0.8).to_edge(LEFT, buff=0.5 + 0.3),
            wheel_text.animate.scale(0.8).next_to(api_group, UP, buff=0.2).to_edge(LEFT, buff=1.0),
            run_time=1
        )
        self.play(
            FadeIn(db_group),
            GrowFromCenter(wall), FadeIn(wall_label),
            FadeIn(security_text),
            run_time=1.5
        )

        sub7 = show_subtitle(self, "めたん",
            "裏側を直接触らせないことでセキュリティも守れます。さあ、最強のアプリを作りましょう！",
            CHAR_METAN, duration=7, prev_sub=sub6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
