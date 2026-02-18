from manim import *
import os
import difflib
import json

# Setup
config.background_color = "#1e1e1e" # Darker background for "Dark side" theme
config.frame_width = 16
config.frame_height = 9

TEXT_MAIN = WHITE
TEXT_SUB = "#d0d0d0"
ACCENT_COLOR = "#00d2ff" # Cyan for tech
ACCENT_WARN = "#ff4b4b" # Red for danger/errors
CHAR_ZUNDA = "#34eb7d" # Zundamon Green
CHAR_METAN = "#ff7ae2" # Metan Pink

# Helper Functions (Copied/Adapted)
def wrap_text(text, max_chars=28):
    if len(text) <= max_chars:
        return text
    
    parts = []
    current_part = ""
    for char in text:
        current_part += char
        if len(current_part) >= max_chars:
            parts.append(current_part)
            current_part = ""
            
    if current_part:
        parts.append(current_part)
        
    return "\n".join(parts)

def get_subtitle(scene, speaker, text, speaker_color=TEXT_MAIN, prev_sub=None):
    # Remove previous subtitle if exists
    if prev_sub:
        scene.remove(prev_sub)
        
    # Create new subtitle
    wrapped = wrap_text(text)
    line = Text(wrapped, font="Noto Sans JP", font_size=28, color=TEXT_MAIN, line_spacing=1.2)
    
    # Speaker label
    label = Text(speaker, font="Noto Sans JP", font_size=24, color=speaker_color, weight=BOLD)
    label.next_to(line, UP, buff=0.2, aligned_edge=LEFT)
    
    # Background for readability
    bg = BackgroundRectangle(VGroup(label, line), color=BLACK, fill_opacity=0.7, buff=0.2)
    
    group = VGroup(bg, label, line).to_edge(DOWN, buff=0.5)
    scene.add(group)
    
    # Audio sync
    wait_time = 2.0 # Default
    
    if hasattr(scene, "audio_map") and scene.audio_map:
        # Find matching audio
        best_match = None
        highest_ratio = 0.0
        
        for item in scene.audio_map:
            ratio = difflib.SequenceMatcher(None, item["text"], text).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = item
        
        if best_match and highest_ratio > 0.6:
            audio_file = best_match["file"]
            if os.path.exists(audio_file):
                scene.add_sound(audio_file)
                wait_time = best_match["duration"]
    
    # Text animation
    scene.play(Write(line), run_time=0.3)
    scene.wait(wait_time + 0.2)
    
    return group

def get_image(name, scale=1.0):
    """画像があれば表示、なければカスタム描画"""
    key_name = name.replace(".png", "").replace(".jpg", "")
    if not name.endswith((".png", ".jpg")):
        name += ".png"
        
    path = os.path.join("projects", "stable_diffusion_yt", "media", "images", name)
    if os.path.exists(path):
        return ImageMobject(path).scale(scale)
    
    # Fallbacks
    if "noise" in key_name:
        return draw_noise().scale(scale)
    elif "robot" in key_name or "ai" in key_name:
        return draw_robot().scale(scale)
    elif "magic" in key_name:
        return draw_magic_circle().scale(scale)
    elif "canvas" in key_name:
        return Rectangle(width=4, height=3, color=WHITE, fill_opacity=0.1)
        
    return Text(key_name, color=GREY).scale(0.5)

# Custom Drawings
def draw_noise():
    # Simulated noise with dots
    dots = VGroup()
    colors = [WHITE, GREY, DARK_GREY]
    for _ in range(100):
        d = Dot(point=[
            np.random.uniform(-1.5, 1.5),
            np.random.uniform(-1.5, 1.5),
            0
        ], color=np.random.choice(colors), radius=0.05)
        dots.add(d)
    return dots

def draw_robot():
    head = RoundedRectangle(width=1, height=0.8, corner_radius=0.2, color=ACCENT_COLOR, fill_opacity=0.5)
    eyes = VGroup(
        Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(head.get_center() + LEFT*0.2 + UP*0.1),
        Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(head.get_center() + RIGHT*0.2 + UP*0.1)
    )
    antennas = VGroup(
        Line(head.get_top() + LEFT*0.3, head.get_top() + LEFT*0.4 + UP*0.3, color=ACCENT_COLOR),
        Line(head.get_top() + RIGHT*0.3, head.get_top() + RIGHT*0.4 + UP*0.3, color=ACCENT_COLOR),
        Circle(radius=0.05, color=RED, fill_opacity=1).move_to(head.get_top() + LEFT*0.4 + UP*0.3),
        Circle(radius=0.05, color=RED, fill_opacity=1).move_to(head.get_top() + RIGHT*0.4 + UP*0.3)
    )
    return VGroup(head, eyes, antennas)

def draw_magic_circle():
    c1 = Circle(radius=1.5, color=PURPLE)
    c2 = Circle(radius=1.2, color=PURPLE)
    star = Star(n=5, outer_radius=1.2, inner_radius=0.5, color=PURPLE)
    runes = VGroup(*[Text(char, font="Consolas", color=PURPLE).scale(0.5).move_to(
        1.35 * np.array([np.cos(theta), np.sin(theta), 0])
    ) for i, char in enumerate("STABLEDIFFUSION") for theta in [i * 2 * PI / 15]])
    return VGroup(c1, c2, star, runes)

# ============================================================================
# Base Scene with Audio Loading
# ============================================================================
class BaseScene(Scene):
    def setup(self):
        self.camera.background_color = "#1e1e1e"
        
        # Load audio map
        map_path = os.path.join("projects", "stable_diffusion_yt", "media", "audio", "audio_map.json")
        scene_name = self.__class__.__name__
        # Normalize scene name for map lookup (e.g. Scene01_Intro -> Scene01)
        # Use simple prefix matching
        
        self.audio_map = []
        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Try to find matching key
                for key in data.keys():
                    if key in scene_name: # e.g. "Scene01" in "Scene01_Intro"
                        self.audio_map = data[key]
                        break

# ============================================================================
# Scenes
# ============================================================================

class Scene01_Intro(BaseScene):
    def construct(self):
        sub1 = get_subtitle(self, "ずんだもん", "ねぇめたん、僕も神絵師になりたいのだ！ チヤホヤされたいのだ！", CHAR_ZUNDA)
        
        zunda = Text("ずんだもん", color=CHAR_ZUNDA).move_to(LEFT*4)
        metan = Text("めたん", color=CHAR_METAN).move_to(RIGHT*4)
        self.play(FadeIn(zunda), FadeIn(metan))
        
        canvas = Rectangle(width=4, height=3, color=WHITE).move_to(UP*1)
        scribble = Text("💩", font_size=80).move_to(canvas) # Bad drawing
        self.play(Create(canvas), Write(scribble))
        
        sub2 = get_subtitle(self, "めたん", "また安直な悩みですわね。どうせ絵心はゼロなんでしょう？", CHAR_METAN, sub1)
        sub3 = get_subtitle(self, "ずんだもん", "画伯って呼ばれてるのだ。でも今はAIがあるのだ！ Stable Diffusionがあれば僕もクリエイターなのだ！", CHAR_ZUNDA, sub2)
        
        ai_logo = Text("Stable Diffusion", font_size=40, gradient=(BLUE, PURPLE)).next_to(canvas, UP)
        self.play(Transform(scribble, draw_magic_circle().scale(0.5)), FadeIn(ai_logo))
        
        sub4 = get_subtitle(self, "めたん", "やれやれ、また「他人のふんどし」で相撲を取る気満々ですわね。", CHAR_METAN, sub3)
        
        sumo = Text("🥋", font_size=80).move_to(DOWN*1)
        self.play(FadeIn(sumo))
        
        sub5 = get_subtitle(self, "ずんだもん", "人聞きが悪すぎるのだ！ AIだって道具なのだ！", CHAR_ZUNDA, sub4)
        sub6 = get_subtitle(self, "めたん", "ええ、禁断の果実とも言える道具ですわ。今回はその中身、「Stable Diffusion」の闇を覗いてみましょうか。覚悟はよくて？", CHAR_METAN, sub5)
        
        flash = Rectangle(width=16, height=9, color=WHITE, fill_opacity=1)
        self.play(FadeIn(flash, run_time=0.1), FadeOut(flash, run_time=0.5))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene02_Diffusion(BaseScene):
    def construct(self):
        title = Text("Stable Diffusion = 拡散モデル", font_size=48).to_edge(UP)
        self.play(Write(title))
        
        sub1 = get_subtitle(self, "めたん", "Stable Diffusionの正体は「拡散モデル」です。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "拡散？ ウイルスみたいなのだ？", CHAR_ZUNDA, sub1)
        
        virus = Text("🦠", font_size=60).move_to(LEFT*3)
        self.play(FadeIn(virus))
        
        sub3 = get_subtitle(self, "めたん", "ある意味、ウイルス並みの爆発力はありますわ。でも、やっていることは「ノイズの除去」です。", CHAR_METAN, sub2)
        
        noise_box = commands = Square(color=WHITE).move_to(RIGHT*3)
        noise = draw_noise().move_to(noise_box)
        self.play(Create(noise_box), FadeIn(noise))
        self.play(FadeOut(virus))
        
        sub4 = get_subtitle(self, "めたん", "真っ白な紙にインクをぶちまけて、そこから「モナリザ」を見つけ出すような狂気の作業ですわ。", CHAR_METAN, sub3)
        
        ink = Circle(radius=1, color=BLACK, fill_opacity=0.8).move_to(ORIGIN)
        mona = Text("🖼️", font_size=80).move_to(ORIGIN)
        
        self.play(Transform(noise, ink))
        self.play(Transform(ink, mona))
        
        sub5 = get_subtitle(self, "ずんだもん", "意味がわからないのだ！ それってただの幻覚なのだ！", CHAR_ZUNDA, sub4)
        sub6 = get_subtitle(self, "めたん", "天才と狂人は紙一重と言いますからね。AIは意図的に幻覚を見ているのかもしれませんわ。", CHAR_METAN, sub5)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene03_Forward(BaseScene):
    def construct(self):
        t = Text("Forward Process (破壊)", color=RED).to_edge(UP)
        self.play(Write(t))
        
        img = Text("🐱", font_size=100)
        self.play(FadeIn(img))
        
        sub1 = get_subtitle(self, "めたん", "まずAIに「破壊」を教えます。綺麗な写真に少しずつ砂嵐（ノイズ）を混ぜていくんです。", CHAR_METAN)
        
        # Add noise gradually
        noises = VGroup()
        for i in range(5):
            n = draw_noise().set_opacity(0.2 * (i+1))
            noises.add(n)
            self.play(FadeIn(n), run_time=0.5)
            
        sub2 = get_subtitle(self, "ずんだもん", "せっかくの写真をボロボロにするなんて、サイコパスなのだ！", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "これが学習ですわ。最終的にはただの砂嵐になります。", CHAR_METAN, sub2)
        
        self.play(img.animate.set_opacity(0))
        
        sub4 = get_subtitle(self, "ずんだもん", "何の意味があるのだ？", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "「壊し方」を知っていれば、「直し方」もわかる。そういう理屈ですわ。", CHAR_METAN, sub4)
        sub6 = get_subtitle(self, "ずんだもん", "逆再生ビデオみたいなものなのだ？", CHAR_ZUNDA, sub5)
        
        arrow = Arrow(RIGHT*3, LEFT*3, color=YELLOW)
        self.play(GrowArrow(arrow))
        
        sub7 = get_subtitle(self, "めたん", "鋭いですわね。でも、ただの逆再生じゃありません。AIは「どんなノイズが足されたか」を予測する能力を身につけるんです。", CHAR_METAN, sub6)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene04_Reverse(BaseScene):
    def construct(self):
        t = Text("Reverse Process (創造)", color=GREEN).to_edge(UP)
        self.play(Write(t))
        
        noise = draw_noise().scale(2)
        self.play(FadeIn(noise))
        
        sub1 = get_subtitle(self, "めたん", "次に「創造」の工程です。完全にランダムな砂嵐を用意します。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "さっきの壊れた画像なのだ？", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "いいえ、ただの無秩序なノイズです。ここからAIが「さっき覚えたノイズ除去」を繰り返します。", CHAR_METAN, sub2)
        
        # Removal animation
        robot = draw_robot().move_to(RIGHT*4)
        self.play(FadeIn(robot))
        
        sub4 = get_subtitle(self, "ずんだもん", "ノイズを取ったら、元の画像に戻るんじゃないの？", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "ここがミソですわ。元の画像なんてありません。「ノイズを取り除いたら、たまたま猫っぽくなった」という奇跡を繰り返すんです。", CHAR_METAN, sub4)
        
        cat = Text("🐱", font_size=100)
        
        self.play(Transform(noise, cat, run_time=3))
        
        sub6 = get_subtitle(self, "ずんだもん", "つまり、雲を見て「あれドラ〇もんっぽい」って言う遊びを全力でやってるのだ？", CHAR_ZUNDA, sub5)
        sub7 = get_subtitle(self, "めたん", "まさにそうですわ！ AIは雲の中に、我々が指定した「何か」を必死に探しているんです。健気でしょう？", CHAR_METAN, sub6)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene05_Fingers(BaseScene):
    def construct(self):
        t = Text("AIの弱点：指", color=RED).to_edge(UP)
        self.play(Write(t))
        
        hand = Text("🖐️", font_size=80)
        self.play(FadeIn(hand))
        
        sub1 = get_subtitle(self, "めたん", "ここで余談ですが、初期のAI絵師たちが一番苦しんだものを知っていますか？", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "著作権問題なのだ？", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "それもそうですが、もっと根本的な…「指」ですわ。", CHAR_METAN, sub2)
        
        # Add extra fingers
        fingers = VGroup(*[Line(UP*0.5, UP*1).rotate(angle).move_to(hand.get_center() + UP*0.5 + RIGHT*0.2*i) for i, angle in enumerate(np.linspace(-0.5, 0.5, 7))])
        self.play(FadeOut(hand), Create(fingers))
        
        sub4 = get_subtitle(self, "ずんだもん", "指？ そういえば6本あったりスパゲッティみたいになってたのだ！", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "あれはAIが「人間には指がある」とは知ってても、「5本しかない」という概念を理解していなかったからですわ。", CHAR_METAN, sub4)
        sub6 = get_subtitle(self, "ずんだもん", "詰めが甘いのだ！", CHAR_ZUNDA, sub5)
        sub7 = get_subtitle(self, "めたん", "でも最近は改善されてきました。人類の指の数を学習するのに数年かかるとは、AIも意外とポンコツですわね。", CHAR_METAN, sub6)
        
        sub8 = get_subtitle(self, "ずんだもん", "めたんもたまに指が増えてる気がするけどね…。", CHAR_ZUNDA, sub7)
        sub9 = get_subtitle(self, "めたん", "…何か言いました？", CHAR_METAN, sub8)

        flash = Flash(ORIGIN, color=RED, line_length=0.5)
        self.play(flash)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene06_Latent(BaseScene):
    def construct(self):
        t = Text("Latent Space (潜在空間)", color=PURPLE).to_edge(UP)
        self.play(Write(t))
        
        # Visualize latent compression
        # Big image -> Small cube
        big_img = Square(side_length=4, color=BLUE, fill_opacity=0.3).move_to(LEFT*4)
        arrow = Arrow(LEFT*2, RIGHT*2)
        cube = Cube(side_length=1, fill_opacity=0.5, stroke_width=2).set_color(PURPLE).move_to(RIGHT*4)
        
        self.play(Create(big_img))
        
        sub1 = get_subtitle(self, "めたん", "さて、Stable Diffusionが画期的なのは「潜在空間」を使ったことです。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "潜在？ センザイ？ 洗剤の話なのだ？", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "いいえ、画像のデータをギュッと圧縮した「裏の世界」のことです。", CHAR_METAN, sub2)
        
        self.play(GrowArrow(arrow), FadeIn(cube))
        self.play(cube.animate.rotate(PI/4, axis=UP).rotate(PI/4, axis=RIGHT), run_time=2)
        
        sub4 = get_subtitle(self, "めたん", "普通の画像データは重すぎるので、AIはこの「裏の世界」で計算を行います。", CHAR_METAN, sub3)
        sub5 = get_subtitle(self, "ずんだもん", "圧縮したまま計算できるのすごいのだ。", CHAR_ZUNDA, sub4)
        sub6 = get_subtitle(self, "めたん", "これのおかげで、スーパーコンピューターじゃなくても、あなたの貧弱なゲーミングPCで動くようになったんです。", CHAR_METAN, sub5)
        
        pc = Text("💻", font_size=60).next_to(cube, DOWN)
        self.play(FadeIn(pc))
        
        sub7 = get_subtitle(self, "ずんだもん", "僕のPCは貧弱じゃないのだ！ フォートナイトもヌルヌルなのだ！", CHAR_ZUNDA, sub6)
        sub8 = get_subtitle(self, "めたん", "はいはい。とにかく、この軽量化が「民主化」を引き起こし、世界中にAI絵師を誕生させてしまったわけです。", CHAR_METAN, sub7)
        
        crowd = Text("👨‍🎨👩‍🎨👨‍🎨", font_size=40).move_to(DOWN*2)
        self.play(FadeIn(crowd))
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene07_CLIP(BaseScene):
    def construct(self):
        t = Text("CLIP (AIの翻訳機)", color=ACCENT_COLOR).to_edge(UP)
        self.play(Write(t))
        
        sub1 = get_subtitle(self, "めたん", "でも、ただノイズを除去するだけじゃ、何が出てくるかわかりません。ここで登場するのが「CLIP」です。", CHAR_METAN)
        
        clip_bot = draw_robot().scale(1.5)
        self.play(FadeIn(clip_bot))
        
        sub2 = get_subtitle(self, "ずんだもん", "クリップ？ 文房具なのだ？", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "AI界の「翻訳者」であり「批評家」ですわ。画像とテキストの関連性を完璧に理解しています。", CHAR_METAN, sub2)
        
        txt_node = Text("Text: Cat", font_size=24).move_to(LEFT*4)
        img_node = Text("Img: 🐱", font_size=24).move_to(RIGHT*4)
        
        self.play(Write(txt_node), Write(img_node))
        
        arrow_l = Arrow(txt_node.get_right(), clip_bot.get_left())
        arrow_r = Arrow(img_node.get_left(), clip_bot.get_right())
        
        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r))
        
        sub4 = get_subtitle(self, "ずんだもん", "どういうことなのだ？", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "例えば「猫」というテキストと、生成中の画像を見比べて、「もっと猫っぽくしろ！」と拡散モデルに指示を出すんです。", CHAR_METAN, sub4)
        
        bubble = Text("More Cat!", color=RED, font_size=24).next_to(clip_bot, UP)
        self.play(Write(bubble))
        
        sub6 = get_subtitle(self, "ずんだもん", "なるほど！ CLIP先生がいないと、AIは何を描けばいいかわからないのだ。", CHAR_ZUNDA, sub5)
        sub7 = get_subtitle(self, "めたん", "そうです。二人のAIが協力して、あなたの妄想を具現化しているわけです。", CHAR_METAN, sub6)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene08_Prompt(BaseScene):
    def construct(self):
        t = Text("Prompt Engineering (呪文詠唱)", color=GOLD).to_edge(UP)
        self.play(Write(t))
        
        sub1 = get_subtitle(self, "めたん", "こうして生まれたのが「プロンプトエンジニアリング」…俗に言う「呪文詠唱」です。", CHAR_METAN)
        
        magic = draw_magic_circle().scale(1.5).move_to(ORIGIN)
        self.play(Rotate(magic, angle=2*PI, run_time=2))
        
        sub2 = get_subtitle(self, "ずんだもん", "((masterpiece)), ((best quality))... みたいなやつなのだ！", CHAR_ZUNDA, sub1)
        
        prompt = Text("((masterpiece)), best quality, ultra detailed, 8k...", font="Consolas", font_size=20, color=GOLD).next_to(magic, DOWN)
        self.play(Write(prompt))
        
        sub3 = get_subtitle(self, "めたん", "実にあほらしい光景ですわ。英語の羅列でAIのご機嫌を伺うなんて。", CHAR_METAN, sub2)
        sub4 = get_subtitle(self, "ずんだもん", "でも、呪文一つで絵が変わるから面白いのだ。", CHAR_ZUNDA, sub3)
        
        # Gacha simulation
        card = Rectangle(width=2, height=3, color=WHITE).move_to(UP*1)
        self.play(FadeIn(card))
        self.play(card.animate.set_color(GOLD), Flash(card, color=GOLD))
        
        sub5 = get_subtitle(self, "めたん", "まぁ、ガチャみたいなものですわ。レアな絵が出るまでひたすら呪文を唱え続ける…完全に依存症の行動パターンですけどね。", CHAR_METAN, sub4)
        sub6 = get_subtitle(self, "ずんだもん", "ぐぬぬ、否定できないのだ。", CHAR_ZUNDA, sub5)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene09_Ethics(BaseScene):
    def construct(self):
        t = Text("Copyright Issues (著作権)", color=RED).to_edge(UP)
        self.play(Write(t))
        
        sub1 = get_subtitle(self, "めたん", "しかし、この技術には大きな闇があります。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "やっぱり著作権なのだ？", CHAR_ZUNDA, sub1)
        
        skull = Text("💀", font_size=80)
        self.play(FadeIn(skull))
        
        sub3 = get_subtitle(self, "めたん", "学習データの出処ですわ。ネット上の画像を勝手に吸い取って学習させた「無断学習」の塊だと言う人もいます。", CHAR_METAN, sub2)
        
        # Vacuum cleaner concept
        cloud = Ellipse(width=5, height=3, color=GREY, fill_opacity=0.3).move_to(UP*2)
        self.play(FadeIn(cloud))
        lines = VGroup(*[Line(cloud.get_bottom(), skull.get_top(), stroke_width=2, color=GREY) for _ in range(5)])
        self.play(ShowPassingFlash(lines, time_width=0.5))
        
        sub4 = get_subtitle(self, "ずんだもん", "泥棒みたいなのだ？", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "法的にはグレーゾーン…いや、国によってはホワイトですが、倫理的には真っ黒に近いグレーですわね。", CHAR_METAN, sub4)
        sub6 = get_subtitle(self, "ずんだもん", "絵師さんが怒るのも無理はないのだ。", CHAR_ZUNDA, sub5)
        sub7 = get_subtitle(self, "めたん", "AIイラストを投稿して「神絵師ですｗ」とドヤ顔するのは、盗品を売りさばく故買屋と同じメンタルかもしれませんわよ…。", CHAR_METAN, sub6)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene10_Future(BaseScene):
    def construct(self):
        t = Text("The Future", color=BLUE).to_edge(UP)
        self.play(Write(t))
        
        sub1 = get_subtitle(self, "めたん", "今後は動画生成AI、3D生成AIと、さらにカオスな時代が来ます。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "クリエイターは全滅しちゃうのだ？", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "全滅はしませんが、「描くだけ」の価値は暴落しますわね。", CHAR_METAN, sub2)
        
        graph = Axes(x_range=[0, 10], y_range=[0, 10], x_length=4, y_length=3).move_to(LEFT*3)
        curve = graph.plot(lambda x: 10/(x+1), color=RED)
        self.play(Create(graph), Create(curve))
        label = Text("Value", font_size=20).next_to(curve, UP)
        self.play(Write(label))
        
        sub4 = get_subtitle(self, "ずんだもん", "怖い時代なのだ…。", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "逆に言えば、誰でもアイデアを形にできる時代です。センスさえあれば、画力がなくても戦える。", CHAR_METAN, sub4)
        
        idea = Text("💡", font_size=80).move_to(RIGHT*3)
        self.play(FadeIn(idea))
        
        sub6 = get_subtitle(self, "めたん", "まぁ、センスがない人にとっては地獄でしょうけど。", CHAR_METAN, sub5)
        sub7 = get_subtitle(self, "ずんだもん", "最後の一言が余計なのだ！", CHAR_ZUNDA, sub6)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene11_Summary(BaseScene):
    def construct(self):
        t = Text("Summary", color=WHITE).to_edge(UP)
        self.play(Write(t))
        
        sub1 = get_subtitle(self, "めたん", "今回はStable Diffusionの仕組みを解説しました。", CHAR_METAN)
        
        points = VGroup(
            Text("• ノイズ除去 (Denoising)"),
            Text("• 潜在空間 (Latent Space)"),
            Text("• CLIP (Text-Image Link)")
        ).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(points))
        
        sub2 = get_subtitle(self, "ずんだもん", "ノイズからの破壊と創造、潜在空間での計算、CLIP先生の指導。だいたい分かったのだ！", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "仕組みを知れば、ただの魔法じゃないと分かりますわね。", CHAR_METAN, sub2)
        sub4 = get_subtitle(self, "ずんだもん", "でも、やっぱり魔法みたいなのだ。", CHAR_ZUNDA, sub3)
        sub5 = get_subtitle(self, "めたん", "ふふっ、十分に発達した科学技術は魔法と区別がつかない、と言いますからね。", CHAR_METAN, sub4)
        
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

class Scene12_Ending(BaseScene):
    def construct(self):
        sub1 = get_subtitle(self, "めたん", "というわけで、AIに支配される前に、AIを使いこなす側になりましょう。", CHAR_METAN)
        sub2 = get_subtitle(self, "ずんだもん", "僕も今日から呪文詠唱を極めるのだ！ エクスプロージョン！", CHAR_ZUNDA, sub1)
        sub3 = get_subtitle(self, "めたん", "それは別の爆裂魔法ですわ。", CHAR_METAN, sub2)
        
        btn = RoundedRectangle(width=4, height=1, color=RED, fill_opacity=1)
        txt = Text("SUBSCRIBE", weight=BOLD).move_to(btn)
        grp = VGroup(btn, txt).move_to(UP*0.5)
        
        self.play(FadeIn(grp))
        self.play(grp.animate.scale(1.1).set_color(ACCENT_WARN), run_time=0.5)
        
        sub4 = get_subtitle(self, "めたん", "チャンネル登録してくれないと、あなたのPCのGPU、マイニングウイルスを仕込みますわよ。", CHAR_METAN, sub3)
        sub5 = get_subtitle(self, "ずんだもん", "やめるのだー！", CHAR_ZUNDA, sub4)
        
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
