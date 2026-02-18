"""
SVAE (Structured / Sequential VAE) 解説アニメーション
======================================================

台本: projects/svae_explanation/script.md

Usage:
  python tools/render_parallel.py svae_explanation
"""

from manim import *
import numpy as np

# ============================================================================
# カラー・スタイル
# ============================================================================
BG_COLOR = "#f5f5f5"
TEXT_MAIN = "#1a1a2e"
ACCENT_BLUE = "#1971c2"
ACCENT_GREEN = "#099268"
ACCENT_RED = "#d6336c"
ACCENT_YELLOW = "#e8590c"
ACCENT_PURPLE = "#9c36b5"
TEXT_DIM = "#868e96"

CHAR_ZUNDA = "#099268"
CHAR_METAN = "#d6336c"

import json
import os

# 音声マップ読み込み
AUDIO_MAP = {}
map_path = "projects/svae_explanation/media/audio/audio_map.json"
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
    for offset in range(min(mid, 12)):
        for pos in [mid + offset, mid - offset]:
            if 0 < pos < len(text) and text[pos] in '、。！？ ,. ':
                return text[:pos + 1] + '\n' + text[pos + 1:]
    return text[:mid] + '\n' + text[mid:]


def get_subtitle(speaker, text, speaker_color=TEXT_MAIN):
    """字幕を返す"""
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
    """字幕を表示 (音声があれば再生)"""
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
            # 台本上の順番通りと仮定
            if scene.speech_index < len(audio_list):
                candidate = audio_list[scene.speech_index]
                audio_data = candidate
                scene.speech_index += 1
        except Exception as e:
            print(f"Audio lookup error: {e}")

    wait_time = duration
    
    # 音声再生
    if audio_data:
        file_path = audio_data["file"]
        if os.path.exists(file_path):
            scene.add_sound(file_path)
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
# Scene 01: 導入 - なぜVAEだけでは不十分なのか？
# ============================================================================

class Scene01_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("SVAE: 構造化変分オートエンコーダ", font="Noto Sans JP", font_size=36, color=TEXT_MAIN, weight=BOLD)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        sub1 = show_subtitle(self, "ずんだもん",
            "「生成AI」っていうと、最近はLLMとか拡散モデルばかり聞くのだ。VAEはもうオワコンなのだ？",
            CHAR_ZUNDA, duration=5)

        # VAE, LLM, Diffusion のアイコン的図示
        # LLM (Text)
        llm = VGroup(
            RoundedRectangle(width=2, height=1, color=ACCENT_BLUE, fill_opacity=0.2),
            Text("LLM", font_size=24, color=ACCENT_BLUE)
        ).arrange(ORIGIN)
        
        # Diffusion (Noise -> Image)
        diff = VGroup(
            RoundedRectangle(width=2, height=1, color=ACCENT_RED, fill_opacity=0.2),
            Text("Diffusion", font_size=24, color=ACCENT_RED)
        ).arrange(ORIGIN)
        
        # VAE (Compression)
        vae = VGroup(
            RoundedRectangle(width=2, height=1, color=ACCENT_GREEN, fill_opacity=0.2),
            Text("VAE", font_size=24, color=ACCENT_GREEN)
        ).arrange(ORIGIN)
        
        models = VGroup(llm, diff, vae).arrange(RIGHT, buff=1).move_to(UP * 0.5)
        
        self.play(FadeIn(models))
        self.play(Indicate(llm), Indicate(diff))
        
        sub2 = show_subtitle(self, "めたん",
            "とんでもない！ VAEは今でも生成モデルの基礎ですし、「表現学習」では非常に重要です",
            CHAR_METAN, duration=5, prev_sub=sub1)

        self.play(models[2].animate.scale(1.2).set_color(ACCENT_GREEN), models[0].animate.set_opacity(0.3), models[1].animate.set_opacity(0.3))

        sub3 = show_subtitle(self, "ずんだもん",
            "でも、VAEって画像がボヤけるイメージしかないのだ…",
            CHAR_ZUNDA, duration=4, prev_sub=sub2)

        # ボヤけた画像のイメージ（Blur）
        circle = Circle(radius=1, color=TEXT_DIM, fill_opacity=0.3).next_to(vae, DOWN, buff=0.5)
        blur_text = Text("Blurry...", font_size=20, color=TEXT_DIM).move_to(circle)
        self.play(FadeIn(circle), FadeIn(blur_text))

        sub4 = show_subtitle(self, "めたん",
            "それは単純なVAEの話です。実は、VAEに「構造」を持たせた SVAE (Structured VAE) があるのをご存知ですか？",
            CHAR_METAN, duration=6, prev_sub=sub3)
        
        # SVAEの登場
        svae_text = Text("S-VAE", font_size=48, color=ACCENT_YELLOW, weight=BOLD).move_to(vae)
        structure = VGroup(*[Line(ORIGIN, np.array([np.cos(t), np.sin(t), 0]), color=ACCENT_YELLOW) for t in np.linspace(0, 2*PI, 8)])
        structure.move_to(svae_text)
        
        self.play(Transform(models[2], svae_text), FadeIn(structure), FadeOut(circle), FadeOut(blur_text))

        sub5 = show_subtitle(self, "ずんだもん",
            "SVAE？ 初耳なのだ。スーパーVAEなのだ？",
            CHAR_ZUNDA, duration=4, prev_sub=sub4)
        
        sub6 = show_subtitle(self, "めたん",
            "いいえ、「Structured（構造化）」です。今日は、データの「構造」を明示的に扱うSVAEについて解説しましょう",
            CHAR_METAN, duration=6, prev_sub=sub5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 02: VAEの復習と限界
# ============================================================================

class Scene02_Review(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("VAEの復習と限界", font="Noto Sans JP", font_size=32, color=ACCENT_BLUE, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "めたん",
            "まず普通のVAEを思い出してください。入力データを潜在変数 z に圧縮し、そこから復元しますね",
            CHAR_METAN, duration=5)

        # VAEの仕組み図解
        # Input (Image) -> Encoder -> z (Gaussian) -> Decoder -> Output
        img_in = Square(side_length=1, color=TEXT_MAIN, fill_opacity=0.2)
        encoder = Polygon([-0.5, 0.5, 0], [0.5, 0.2, 0], [0.5, -0.2, 0], [-0.5, -0.5, 0], color=ACCENT_BLUE).scale(0.8)
        
        z_dist = Circle(radius=0.5, color=ACCENT_GREEN, fill_opacity=0.3)
        z_label = MathTex("z \sim N(0, I)", color=TEXT_MAIN).next_to(z_dist, UP, buff=0.4)
        
        decoder = Polygon([-0.5, 0.2, 0], [0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, -0.2, 0], color=ACCENT_RED).scale(0.8)
        img_out = Square(side_length=1, color=TEXT_MAIN, fill_opacity=0.2)

        flow = VGroup(img_in, encoder, z_dist, decoder, img_out).arrange(RIGHT, buff=0.5).move_to(UP * 0.5)
        
        # 矢印
        arrows = VGroup(
            Arrow(img_in.get_right(), encoder.get_left(), buff=0.1, color=TEXT_DIM),
            Arrow(encoder.get_right(), z_dist.get_left(), buff=0.1, color=TEXT_DIM),
            Arrow(z_dist.get_right(), decoder.get_left(), buff=0.1, color=TEXT_DIM),
            Arrow(decoder.get_right(), img_out.get_left(), buff=0.1, color=TEXT_DIM),
        )

        self.play(FadeIn(flow), Create(arrows), Write(z_label))

        sub2 = show_subtitle(self, "ずんだもん",
            "z は確か、標準正規分布に従うように学習するんだったのだ",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)
        
        sub3 = show_subtitle(self, "めたん",
            "そうです。でも、現実のデータって本当に「単純なガウス分布」で表現できるでしょうか？",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 疑問符
        q_mark = Text("?", font_size=48, color=ACCENT_RED).next_to(z_dist, UP, buff=0.5)
        self.play(FadeIn(q_mark))

        sub4 = show_subtitle(self, "ずんだもん",
            "え？ どういうことなのだ？",
            CHAR_ZUNDA, duration=3, prev_sub=sub3)

        sub5 = show_subtitle(self, "めたん",
            "例えば「時系列データ」。今日の気温は昨日の気温と関係がありますよね？",
            CHAR_METAN, duration=5, prev_sub=sub4)
        
        # 時系列データの例
        # 点の列を描画
        dots = VGroup(*[Dot(color=TEXT_MAIN) for _ in range(5)]).arrange(RIGHT, buff=0.5)
        dots.next_to(z_dist, DOWN, buff=1.0)
        
        # 矢印で繋ぐ (依存関係)
        connections = VGroup(*[Arrow(dots[i].get_right(), dots[i+1].get_left(), buff=0.1, color=ACCENT_YELLOW) for i in range(4)])
        
        time_label = Text("時系列依存", font="Noto Sans JP", font_size=20, color=ACCENT_YELLOW).next_to(dots, DOWN)

        self.play(FadeIn(dots), FadeIn(time_label))
        self.play(Create(connections), run_time=2)

        sub6 = show_subtitle(self, "めたん",
            "普通のVAEは、データが独立だと仮定してしまいがちです。そこでSVAEの登場です",
            CHAR_METAN, duration=6, prev_sub=sub5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 03: SVAEの核心 - グラフィカルモデルとの融合
# ============================================================================

class Scene03_Core(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        section = Text("SVAEの核心 (Deep Learning + PGM)", font="Noto Sans JP", font_size=32, color=ACCENT_PURPLE, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "めたん",
            "SVAEは、確率的グラフィカルモデル (PGM) と Deep Learning の融合です",
            CHAR_METAN, duration=5)

        # グラフィカルモデルの図解
        # 例えば状態遷移モデル (HMM like)
        
        states = VGroup(*[Circle(radius=0.4, color=ACCENT_PURPLE, fill_opacity=0.2) for _ in range(4)]).arrange(RIGHT, buff=1)
        observations = VGroup(*[Square(side_length=0.6, color=ACCENT_BLUE, fill_opacity=0.2) for _ in range(4)])
        
        for i, obs in enumerate(observations):
            obs.next_to(states[i], DOWN, buff=0.8)
        
        pgm_group = VGroup(states, observations).move_to(UP * 0.5)

        # 遷移矢印
        trans_arrows = VGroup(*[Arrow(states[i].get_right(), states[i+1].get_left(), color=ACCENT_PURPLE) for i in range(3)])
        # 観測矢印
        emit_arrows = VGroup(*[Arrow(states[i].get_bottom(), observations[i].get_top(), color=ACCENT_BLUE) for i in range(4)])

        labels = VGroup(
            MathTex("z_t", color=ACCENT_PURPLE).next_to(states[0], LEFT),
            MathTex("x_t", color=ACCENT_BLUE).next_to(observations[0], LEFT)
        )

        self.play(FadeIn(states), FadeIn(observations), Write(labels))
        self.play(Create(trans_arrows), Create(emit_arrows), run_time=2)

        sub2 = show_subtitle(self, "ずんだもん",
            "難しそうなのだ…。要するにどういうことなのだ？",
            CHAR_ZUNDA, duration=4, prev_sub=sub1)

        sub3 = show_subtitle(self, "めたん",
            "例えば動画生成。背景（静止）と動き（動的）を分けて扱うことができます",
            CHAR_METAN, duration=5, prev_sub=sub2)

        # 構造化された潜在空間の図
        # Static z (背景) -> 全ての x に矢印
        # Dynamic z (動き) -> 時系列で遷移しつつ x に矢印
        
        self.play(FadeOut(pgm_group), FadeOut(trans_arrows), FadeOut(emit_arrows), FadeOut(labels))
        
        # Static Latent
        z_static = Circle(radius=0.5, color=ACCENT_GREEN, fill_opacity=0.3).move_to(UP * 1.5)
        z_static_label = Text("背景 (不変)", font_size=20, color=ACCENT_GREEN).next_to(z_static, UP)

        # Dynamic Latent
        z_dynamic = VGroup(*[Circle(radius=0.3, color=ACCENT_RED, fill_opacity=0.3) for _ in range(3)]).arrange(RIGHT, buff=1.5)
        z_dynamic.move_to(ORIGIN)
        
        # Frames
        frames = VGroup(*[Square(side_length=0.5, color=TEXT_MAIN) for _ in range(3)])
        for i, f in enumerate(frames):
            f.next_to(z_dynamic[i], DOWN, buff=1.0)
            
        # Arrows
        arrows_dynamic = VGroup(*[Arrow(z_dynamic[i].get_right(), z_dynamic[i+1].get_left(), color=ACCENT_RED) for i in range(2)])
        arrows_static = VGroup(*[Arrow(z_static.get_bottom(), f.get_top(), color=ACCENT_GREEN, buff=0.1) for f in frames])
        arrows_emit = VGroup(*[Arrow(z_dynamic[i].get_bottom(), frames[i].get_top(), color=ACCENT_RED, buff=0.1) for i in range(3)])
        
        struct_group = VGroup(z_static, z_dynamic, frames, arrows_dynamic, arrows_static, arrows_emit, z_static_label)
        struct_group.move_to(UP * 0.5) # 全体配置調整

        self.play(FadeIn(z_static), FadeIn(z_dynamic), FadeIn(frames), Write(z_static_label))
        self.play(Create(arrows_dynamic), Create(arrows_static), Create(arrows_emit), run_time=2)

        sub4 = show_subtitle(self, "ずんだもん",
            "なるほど！ データの「裏側の仕組み」に合わせて、モデルの構造を設計するってことなのだ",
            CHAR_ZUNDA, duration=6, prev_sub=sub3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ============================================================================
# Scene 04: 具体例 - 時系列SVAE (Sequential VAE)
# ============================================================================

class Scene04_App(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        section = Text("応用: カオス時系列予測", font="Noto Sans JP", font_size=32, color=ACCENT_YELLOW, weight=BOLD)
        section.to_edge(UP, buff=0.2)
        self.play(FadeIn(section))

        sub1 = show_subtitle(self, "めたん",
            "時系列予測、例えばカオスや物理シミュレーションでもSVAEは強力です",
            CHAR_METAN, duration=5)

        # 複雑な波形データ (観測)
        ax = Axes(x_range=[0, 10], y_range=[-2, 2], x_length=6, y_length=2, axis_config={"color": TEXT_DIM}).move_to(UP * 2.0)
        curve = ax.plot(lambda x: np.sin(x) + 0.5 * np.sin(3*x) + 0.2 * np.random.randn(), color=TEXT_MAIN)
        obs_label = Text("複雑な観測データ", font="Noto Sans JP", font_size=20, color=TEXT_MAIN).next_to(ax, UP, buff=0.2)
        
        # シンプルな潜在軌道 (真のダイナミクス)
        ax_latent = Axes(x_range=[0, 10], y_range=[-2, 2], x_length=6, y_length=2, axis_config={"color": TEXT_DIM}).move_to(DOWN * 1.0)
        curve_latent = ax_latent.plot(lambda x: np.sin(x), color=ACCENT_BLUE) # ノイズなし
        lat_label = Text("潜在空間の法則 (Simple)", font="Noto Sans JP", font_size=20, color=ACCENT_BLUE).next_to(ax_latent, UP, buff=0.2)
        
        # マッピング矢印
        map_arrow = Arrow(ax.get_bottom(), ax_latent.get_top(), color=TEXT_DIM, buff=0.2)
        enc_text = Text("Encoder", font_size=16, color=TEXT_DIM).next_to(map_arrow, RIGHT)

        self.play(Create(ax), Create(curve), FadeIn(obs_label))
        self.play(Create(map_arrow), FadeIn(enc_text))
        self.play(Create(ax_latent), Create(curve_latent), FadeIn(lat_label))

        sub2 = show_subtitle(self, "ずんだもん",
            "生データで予測するより、本質的な「法則」を掴んでから予測するから精度が良いのだ？",
            CHAR_ZUNDA, duration=6, prev_sub=sub1)

        # 予測部分 (点線)
        curve_pred = ax_latent.plot(lambda x: np.sin(x), x_range=[10, 13], color=ACCENT_RED) # 本当は予測
        pred_label = Text("Future Prediction", font_size=16, color=ACCENT_RED).next_to(curve_pred, RIGHT)

        self.play(Create(curve_pred), FadeIn(pred_label))

        sub3 = show_subtitle(self, "めたん",
            "その通り！ これが「解釈可能性」にも繋がります。AIが何を学習したかが分かりやすくなるんです",
            CHAR_METAN, duration=6, prev_sub=sub2)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
