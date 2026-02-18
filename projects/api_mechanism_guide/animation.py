"""
APIとは何か？ — 自動販売機で学ぶAPIの仕組み
================================================

台本: projects/api_mechanism_guide/script.md

Usage:
  manim -qm projects/api_mechanism_guide/animation.py
"""

from manim import *
import numpy as np
import json
import os
import difflib

config.sound = True

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

# 音声マップ読み込み
AUDIO_MAP = {}
map_path = "projects/api_mechanism_guide/media/audio/audio_map.json"
if os.path.exists(map_path):
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            AUDIO_MAP = json.load(f)
    except Exception as e:
        print(f"Failed to load audio map: {e}")

# ============================================================================
# ヘルパー関数
# ============================================================================

def wrap_text(text, max_chars=28):
    """長いテキストを自動改行する。句読点やスペース付近で折り返す"""
    if len(text) <= max_chars:
        return text
    mid = len(text) // 2
    # 中間点付近で自然な区切りを探す（前後10文字以内）
    for offset in range(min(mid, 12)):
        for pos in [mid + offset, mid - offset]:
            if 0 < pos < len(text) and text[pos] in '、。！？ ,. ':
                return text[:pos + 1] + '\n' + text[pos + 1:]
    # 見つからなければ中間で分割
    return text[:mid] + '\n' + text[mid:]


def get_subtitle(speaker, text, speaker_color=TEXT_MAIN):
    """字幕を返す。話者名（上段）+ セリフ（下段）を中央揃えで配置"""
    name = Text(speaker, font="Noto Sans JP", font_size=20,
                color=speaker_color, weight=BOLD)
    wrapped = wrap_text(text)
    line = Text(wrapped, font="Noto Sans JP", font_size=22, color=TEXT_MAIN)
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
    """字幕を表示し、前の字幕があれば消す (音声があれば再生: ファジーマッチング)"""
    # シーンごとの音声インデックス管理
    if not hasattr(scene, "speech_index"):
        scene.speech_index = 0
    
    scene_name = scene.__class__.__name__
    key = scene_name.split("_")[0]
    audio_data = None
    
    # マップから音声情報を検索
    if key in AUDIO_MAP:
        try:
            audio_list = AUDIO_MAP[key]
            
            # 検索範囲: 現在位置から5つ先まで
            start_idx = scene.speech_index
            end_idx = min(len(audio_list), start_idx + 5)
            candidates = audio_list[start_idx:end_idx]
            
            best_match = None
            highest_ratio = 0.0
            match_offset = 0
            
            for i, cand in enumerate(candidates):
                # 類似度計算
                ratio = difflib.SequenceMatcher(None, text, cand["text"]).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = cand
                    match_offset = i
            
            # 類似度しきい値 (0.2以上なら採用)
            if highest_ratio > 0.2:
                audio_data = best_match
                # マッチした位置の次へインデックスを進める
                scene.speech_index = start_idx + match_offset + 1
            else:
                pass

        except Exception as e:
            print(f"Audio lookup error: {e}")

    wait_time = duration
    
    # 音声再生
    if audio_data:
        file_path = audio_data["file"]
        if os.path.exists(file_path):
            # Manimでのパス解決のために相対パスに変換
            rel_path = os.path.relpath(file_path, os.getcwd())
            scene.add_sound(rel_path)
            wait_time = audio_data["duration"]

    sub = get_subtitle(speaker, text, speaker_color)
    anims = [FadeIn(sub, shift=UP * 0.1)]
    if prev_sub is not None:
        anims.append(FadeOut(prev_sub))
    
    scene.play(*anims, run_time=0.4)
    # 音声の長さだけ待つ (少し余韻)
    scene.wait(wait_time + 0.2)
    
    return sub


# ============================================================================
# Scene 01: イントロダクション
# ============================================================================

class Scene01_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # タイトル
        title = Text("APIの仕組み入門", font="Noto Sans JP", font_size=40, color=TEXT_MAIN, weight=BOLD)
        subtitle = Text("自動販売機で考える", font="Noto Sans JP", font_size=24, color=ACCENT_BLUE)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        self.play(title.animate.to_edge(UP, buff=0.5), FadeOut(subtitle))

        sub1 = show_subtitle(self, "ずんだもん",
            "ねぇねぇ、最近みんな「API」って言ってるのだ。流行ってるお菓子なのだ？",
            CHAR_ZUNDA)

        sub2 = show_subtitle(self, "めたん",
            "残念ながらお菓子ではありませんわ。API（Application Programming Interface）は、IT界の「便利すぎる窓口」のことです。",
            CHAR_METAN, prev_sub=sub1)
            
        window_img = RoundedRectangle(width=4, height=3, color=ACCENT_BLUE, fill_opacity=0.1, corner_radius=0.1)
        window_label = Text("便利な窓口 (API)", font="Noto Sans JP", font_size=24, color=ACCENT_BLUE)
        window_label.move_to(window_img)
        self.play(Create(window_img), Write(window_label))
        
        sub3 = show_subtitle(self, "ずんだもん",
            "窓口？ 役所の手続きみたいなのだ？ 面倒くさそうなのだ…",
            CHAR_ZUNDA, prev_sub=sub2)

        cross = Cross(window_img, scale_factor=0.8, color=ACCENT_RED)
        self.play(Create(cross))
        
        sub4 = show_subtitle(self, "めたん",
            "いえいえ、むしろ逆ですわ。「面倒な手続きを省いて、欲しいものだけくれる魔法の窓口」なんです。",
            CHAR_METAN, prev_sub=sub3)

        star = Star(color=ACCENT_YELLOW, fill_opacity=1, n=5).scale(0.5).move_to(window_img.get_corner(UR))
        self.play(FadeOut(cross), SpinInFromNothing(star))
        
        self.play(FadeOut(window_img), FadeOut(window_label), FadeOut(star), FadeOut(sub4))


# ============================================================================
# Scene 02: 自動販売機の例え
# ============================================================================

class Scene02_Vending(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        sub1 = show_subtitle(self, "めたん",
            "例えば、自動販売機を想像してください。",
            CHAR_METAN)
        
        machine = VGroup(
            RoundedRectangle(width=2.5, height=4, corner_radius=0.2, color=TEXT_DIM, fill_color='#e9ecef', fill_opacity=1),
            Rectangle(width=2, height=2, color=BLUE_B, fill_opacity=0.3).move_to(UP*0.5), # Display
            Rectangle(width=1.5, height=0.5, color=GREY, fill_opacity=1).move_to(DOWN*1.2), # Exit
        ).move_to(ORIGIN)
        
        button = Circle(radius=0.15, color=RED, fill_opacity=1).move_to(machine.get_center() + RIGHT*0.5 + DOWN*0.2)
        
        self.play(DrawBorderThenFill(machine), run_time=1.5)
        self.play(FadeIn(button))

        sub2 = show_subtitle(self, "めたん",
            "お金を入れ、ボタンを押せば、ジュースが出てきますわよね？",
            CHAR_METAN, prev_sub=sub1)

        # Coin animation
        coin = Circle(radius=0.15, color=YELLOW, fill_opacity=1).move_to(LEFT*2 + UP*1)
        self.play(coin.animate.move_to(machine.get_top() + LEFT*0.5), run_time=1)
        self.play(FadeOut(coin))
        
        # Push Button
        finger = Triangle(color=BLACK, fill_opacity=1).scale(0.2).rotate(-PI/2).next_to(button, RIGHT)
        self.play(finger.animate.next_to(button, RIGHT, buff=-0.1), run_time=0.3)
        self.play(button.animate.set_color(RED_E), run_time=0.1)
        self.play(button.animate.set_color(RED), finger.animate.next_to(button, RIGHT, buff=0.1), run_time=0.3)
        self.play(FadeOut(finger))
        
        # Juice out
        juice = Rectangle(width=0.4, height=0.6, color=RED, fill_opacity=1).move_to(machine.get_bottom() + UP*0.8)
        self.play(juice.animate.move_to(machine.get_bottom() + DOWN*0.5), run_time=1)

        sub3 = show_subtitle(self, "ずんだもん",
            "当たり前なのだ！ コーラが大好きなのだ。",
            CHAR_ZUNDA, prev_sub=sub2)

        sub4 = show_subtitle(self, "めたん",
            "でも、自販機の中でどうやってジュースが冷やされているか、知っていますか？",
            CHAR_METAN, prev_sub=sub3)

        gears = VGroup(*[Gear(8).scale(0.3).set_color(GREY) for _ in range(3)]).arrange(RIGHT, buff=0).move_to(machine)
        gears[1].shift(UP*0.3)
        
        # X-ray effect
        self.play(machine.animate.set_opacity(0.1), FadeIn(gears))
        self.play(Rotate(gears[0], PI), Rotate(gears[1], -PI), Rotate(gears[2], PI), run_time=2)

        sub5 = show_subtitle(self, "ずんだもん",
            "知らないのだ。冷やす機械とか、補充とか、全然わからないのだ。",
            CHAR_ZUNDA, prev_sub=sub4)

        self.play(FadeOut(gears), machine.animate.set_opacity(1))

        sub6 = show_subtitle(self, "めたん",
            "そう！ 「中身の仕組みを知らなくても、ボタンを押すだけで機能を使える」。これがAPIの本質ですわ。",
            CHAR_METAN, prev_sub=sub5)

        api_text = Text("API = ボタン", font_size=32, color=ACCENT_RED, weight=BOLD).next_to(button, RIGHT, buff=1)
        arrow = Arrow(api_text.get_left(), button.get_right(), color=ACCENT_RED)
        self.play(Write(api_text), GrowArrow(arrow))

        sub7 = show_subtitle(self, "ずんだもん",
            "なるほど！ ボタンがAPIみたいなものなのだ？",
            CHAR_ZUNDA, prev_sub=sub6)

        sub8 = show_subtitle(self, "めたん",
            "その通りです。「ボタン（API）」という窓口が用意されているおかげで、複雑な自販機（サーバー）を誰でも簡単に使えるのです。",
            CHAR_METAN, prev_sub=sub7)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Gear(VMobject):
    def __init__(self, n_teeth=8, **kwargs):
        super().__init__(**kwargs)
        angle = TAU / n_teeth
        points = []
        for i in range(n_teeth):
            points.extend([
                (np.cos(i * angle), np.sin(i * angle), 0),
                (np.cos(i * angle + angle / 4), np.sin(i * angle + angle / 4), 0),
                (np.cos(i * angle + angle * 3/4), np.sin(i * angle + angle * 3/4), 0),
                (np.cos((i + 1) * angle), np.sin((i + 1) * angle), 0),
            ])
        self.set_points_as_corners(points)
        self.close_path()

# ============================================================================
# Scene 03: Web APIの仕組み
# ============================================================================

class Scene03_Web(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        sub1 = show_subtitle(self, "めたん",
            "実際のWeb APIでは、この「ボタン」が「URL」になります。",
            CHAR_METAN)
        
        url_text = Text("https://api.tenki.jp/tokyo", font="Consolas", font_size=24, color=ACCENT_BLUE)
        button_shape = RoundedRectangle(width=6, height=1, color=ACCENT_BLUE, fill_opacity=0.1)
        button_grp = VGroup(button_shape, url_text).move_to(UP*1)
        
        self.play(DrawBorderThenFill(button_shape), Write(url_text))

        sub2 = show_subtitle(self, "ずんだもん",
            "URL？ あのホームページのアドレスなのだ？",
            CHAR_ZUNDA, prev_sub=sub1)

        sub3 = show_subtitle(self, "めたん",
            "ええ。「https://api.tenki.jp/tokyo」のようなURLにアクセスするのが「ボタンを押す」行為です。",
            CHAR_METAN, prev_sub=sub2)

        # Click animation
        cursor = Triangle(color=BLACK, fill_opacity=1).scale(0.2).rotate(-PI*2/3).next_to(button_grp, DR)
        self.play(cursor.animate.move_to(button_grp.get_center()), run_time=0.5)
        self.play(button_grp.animate.scale(0.95), run_time=0.1)
        self.play(button_grp.animate.scale(1.0/0.95), run_time=0.1)
        
        req_text = Text("Request →", font_size=20, color=ACCENT_BLUE).next_to(button_grp, RIGHT)
        self.play(FadeIn(req_text, shift=RIGHT))

        sub4 = show_subtitle(self, "めたん",
            "すると、サーバーから「今日の天気は晴れ」というデータが返ってきます。これが「ジュース」です。",
            CHAR_METAN, prev_sub=sub3)
            
        json_text = Text("{ \"weather\": \"sunny\" }", font="Consolas", font_size=28, color=ACCENT_GREEN)
        res_text = Text("← Response", font_size=20, color=ACCENT_GREEN).next_to(json_text, RIGHT)
        json_grp = VGroup(json_text, res_text).next_to(button_grp, DOWN, buff=1)
        
        self.play(FadeIn(json_grp, shift=UP))

        sub5 = show_subtitle(self, "ずんだもん",
            "おお！ 天気を予測する難しい計算をしなくても、答えだけもらえるのだ！",
            CHAR_ZUNDA, prev_sub=sub4)
            
        # Cloud doesn't exist in Manim Community default shapes easily, use Ellipses
        cloud = VGroup(
            Ellipse(width=2, height=1.2, color=GREY_A, fill_opacity=0.5),
            Ellipse(width=1.5, height=1, color=GREY_A, fill_opacity=0.5).shift(RIGHT*0.8 + UP*0.2),
            Ellipse(width=1.8, height=1.1, color=GREY_A, fill_opacity=0.5).shift(LEFT*0.6 + UP*0.3),
        ).move_to(UP*2 + RIGHT*3).set_z_index(-1)
        
        self.play(FadeIn(cloud))

        sub6 = show_subtitle(self, "めたん",
            "まさにそうです。「面倒な処理は全部任せて、結果だけ受け取る」。これがAPIを使う最大のメリットですわ。",
            CHAR_METAN, prev_sub=sub5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 04: まとめ
# ============================================================================

class Scene04_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        sub1 = show_subtitle(self, "ずんだもん",
            "つまり、APIを使えば、僕でもすごいアプリが作れるってことなのだ？",
            CHAR_ZUNDA)

        sub2 = show_subtitle(self, "めたん",
            "そうです！ 天気予報も、地図も、決済機能も、APIという「部品」を組み合わせれば、すぐに高性能なアプリが作れますわ。",
            CHAR_METAN, prev_sub=sub1)

        # Lego setup
        lego1 = Rectangle(width=1, height=1, color=RED, fill_opacity=0.8).move_to(LEFT*2)
        lego2 = Rectangle(width=1, height=1, color=BLUE, fill_opacity=0.8).move_to(RIGHT*2)
        lego3 = Rectangle(width=2, height=1, color=GREEN, fill_opacity=0.8).move_to(UP*2)
        
        l1_txt = Text("Weather", font_size=16).move_to(lego1)
        l2_txt = Text("Map", font_size=16).move_to(lego2)
        l3_txt = Text("Payment", font_size=16).move_to(lego3)
        
        g1 = VGroup(lego1, l1_txt)
        g2 = VGroup(lego2, l2_txt)
        g3 = VGroup(lego3, l3_txt)
        
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(g3))
        
        # Combine
        self.play(
            g1.animate.move_to(DOWN*1 + LEFT*0.5),
            g2.animate.move_to(DOWN*1 + RIGHT*0.5),
            run_time=1
        )
        self.play(g3.animate.move_to(ORIGIN), run_time=1)
        
        app_label = Text("Your Super App", font_size=32, color=TEXT_MAIN, weight=BOLD).next_to(g3, UP)
        self.play(Write(app_label))

        sub3 = show_subtitle(self, "ずんだもん",
            "すごいのだ！ レゴブロックみたいに世界を組み立てるのだ！",
            CHAR_ZUNDA, prev_sub=sub2)

        sub4 = show_subtitle(self, "めたん",
            "ふふっ、良い例えですわね。さあ、APIを使って開発を始めましょう！",
            CHAR_METAN, prev_sub=sub3)
            
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
