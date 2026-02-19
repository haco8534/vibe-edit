---
name: Manim Technical Explainer Video Workflow (API Basics Style)
description: A comprehensive guide for creating high-quality, character-driven technical explainer videos using the specific Manim style from the 'api_basics_yt' project. Use this for ALL new explainer video requests.
---

# Manim Technical Explainer Video Workflow (API Basics Standard)

This skill defines the **MANDATORY** workflow and code standards for creating technical explainer videos. You must follow this style exactly to ensure consistency with the `api_basics_yt` project.

## 1. Project Setup
When the user asks for a new video (e.g., "Explain Quantum Computing"):
1.  **Create Directory**: `projects/<topic_name>/`
2.  **Create Files**:
    *   `projects/<topic_name>/script.md`
    *   `projects/<topic_name>/animation.py`
    *   `projects/<topic_name>/media/audio/audio_map.json` (Initialize with empty `{}`)

## 2. Research & visual inspiration
Before starting the animation code, you **MUST** research reference implementations to ensure high-quality visuals.
1.  **Check 3b1b Patterns**: Look at `reference/3b1b_patterns.md` (or the `reference/3b1b_videos/` directory if available) to find existing code patterns for similar concepts.
2.  **Do NOT ignore the reference folder**: You are expected to use these references to elevate the quality of your animation beyond the basics.

## 3. Scripting Phase (`script.md`)
Create a designated script file using the following Markdown format. **Do not use tables.**

**Format:**
```markdown
### Scene 01: [Scene Title]
- **[Character Name]**: [Dialogue Line]
- **[Character Name]**: [Dialogue Line]
...
```

**Characters & Tone:**
*   **ずんだもん (Zundamon)**: The learner. Ends sentences with "〜なのだ". Green theme.
*   **めたん (Metan)**: The teacher. Ends sentences with "〜ですわ", "〜ますわ". Pink theme.

## 4. Implementation Phase (`animation.py`)

You **MUST** use the following code structure and helper functions. **Do not deviate** from the subtitle styling or audio logic.

### 4.1 Standard Imports & Constants
Top of `animation.py`:

```python
from manim import *
import numpy as np
import json
import os
import difflib

# ============================================================================
# Theme & Style (MANDATORY)
# ============================================================================
BG_COLOR = "#f5f5f5"         # Light Gray Background
TEXT_MAIN = "#1a1a2e"        # Main Text (Dark Navy)
ACCENT_RED = "#d6336c"       # Deep Rose
ACCENT_YELLOW = "#e8590c"    # Deep Orange
ACCENT_BLUE = "#1971c2"      # Deep Blue
ACCENT_GREEN = "#099268"     # Deep Green
ACCENT_PURPLE = "#7048e8"    # Deep Purple
ACCENT_CYAN = "#0c8599"      # Deep Cyan
TEXT_DIM = "#868e96"         # Dimmed Text (Gray)
CHAR_METAN = "#d6336c"       # Metan Color
CHAR_ZUNDA = "#099268"       # Zundamon Color

# Audio Map Loader
AUDIO_MAP = {}
# Update this path to your current project!
map_path = "projects/<YOUR_PROJECT_NAME>/media/audio/audio_map.json"
if os.path.exists(map_path):
    try:
        with open(map_path, "r", encoding="utf-8") as f:
            AUDIO_MAP = json.load(f)
    except Exception as e:
        print(f"Failed to load audio map: {e}")
```

### 4.2 Helper Functions (COPY THESE EXACTLY)

These functions ensure the subtitle look and feel matches exactly.

```python
# ============================================================================
# Helper Functions
# ============================================================================

def wrap_text(text, max_chars=28):
    """Auto-wrap long text for subtitles."""
    if len(text) <= max_chars:
        return text
    mid = len(text) // 2
    for offset in range(min(mid, 12)):
        for pos in [mid + offset, mid - offset]:
            if 0 < pos < len(text) and text[pos] in '、。！？ ,. ':
                return text[:pos + 1] + '\n' + text[pos + 1:]
    return text[:mid] + '\n' + text[mid:]

def get_subtitle(speaker, text, speaker_color=TEXT_MAIN):
    """Creates the standard subtitle VGroup."""
    name = Text(speaker, font="Noto Sans JP", font_size=20,
                color=speaker_color, weight=BOLD)
    wrapped = wrap_text(text)
    line = Text(wrapped, font="Noto Sans JP", font_size=24, color=TEXT_MAIN, line_spacing=1.2)
    content = VGroup(name, line).arrange(DOWN, buff=0.15, center=True)
    
    # Background Bubble
    bg = RoundedRectangle(
        corner_radius=0.1,
        width=content.get_width() + 1.0, height=content.get_height() + 0.5,
        fill_color=WHITE, fill_opacity=0.9, stroke_color="#dee2e6", stroke_width=1
    )
    bg.move_to(content)
    result = VGroup(bg, content)
    result.to_edge(DOWN, buff=0.5)
    return result

def show_subtitle(scene, speaker, text, speaker_color=TEXT_MAIN, duration=3.0, prev_sub=None):
    """
    Displays subtitle and plays audio (if available in AUDIO_MAP).
    Returns the subtitle object to be used as 'prev_sub' for the next call.
    """
    if not hasattr(scene, "speech_index"):
        scene.speech_index = 0
    
    scene_name = scene.__class__.__name__
    key = scene_name.split("_")[0] # e.g. Scene01_Intro -> Scene01
    audio_data = None
    
    # Audio Sync Logic
    if key in AUDIO_MAP:
        try:
            audio_list = AUDIO_MAP[key]
            start_idx = scene.speech_index
            end_idx = min(len(audio_list), start_idx + 5)
            candidates = audio_list[start_idx:end_idx]
            
            best_match = None
            highest_ratio = 0.0
            match_offset = 0
            
            for i, cand in enumerate(candidates):
                ratio = difflib.SequenceMatcher(None, text, cand["text"]).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = cand
                    match_offset = i
            
            if highest_ratio > 0.4:
                audio_data = best_match
                scene.speech_index = start_idx + match_offset + 1
        except Exception as e:
            print(f"Audio error: {e}")

    wait_time = duration
    
    if audio_data:
        file_path = audio_data["file"]
        if os.path.exists(file_path):
            scene.add_sound(file_path)
            wait_time = audio_data["duration"]

    sub = get_subtitle(speaker, text, speaker_color)
    anims = [FadeIn(sub, shift=UP * 0.2)]
    
    # Auto-fade out previous subtitle if provided
    if prev_sub is not None:
        anims.append(FadeOut(prev_sub))
    
    scene.play(*anims, run_time=0.3)
    scene.wait(wait_time + 0.1)
    
    return sub
```

### 4.3 Scene Implementation Pattern

1.  **Class Name**: `SceneXX_Name` (e.g., `Scene01_Intro`).
2.  **Background**: Always set `self.camera.background_color = BG_COLOR`.
3.  **Subtitle Loop**:
    *   Use `sub1 = show_subtitle(...)`, `sub2 = show_subtitle(..., prev_sub=sub1)` pattern.
    *   Pass `CHAR_METAN` or `CHAR_ZUNDA` for speaker colors.
4.  **Layout**:
    *   **Keep Bottom area clear**: The bottom 20-25% is for subtitles.
    *   **Main Visuals**: `UP*0.5` is roughly the center of the available safe area.

**Example Scene:**

```python
class Scene01_Intro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # TITLE
        title = Text("My Topic", font_size=60, color=ACCENT_BLUE).move_to(UP*0.5)
        self.play(Write(title))
        
        # DIALOGUE
        sub1 = show_subtitle(self, "ずんだもん", "これは何なのだ？", CHAR_ZUNDA)
        sub2 = show_subtitle(self, "めたん", "これはサンプルですわ。", CHAR_METAN, prev_sub=sub1)
        
        self.play(FadeOut(title))
```

## 5. Visual Assets
If you need images, use placeholders first or generate simple geometric shapes using Manim `VGroup`s as shown in the `api_basics_yt` project (e.g., drawing a vending machine with Rectangles and Circles).

## 6. Final Checklist
*   [ ] Did you check `reference/3b1b_patterns.md` for inspiration?
*   [ ] Did you use `BG_COLOR = "#f5f5f5"`?
*   [ ] Did you copy `get_subtitle` and `show_subtitle` exactly?
*   [ ] Are you chaining subtitles using `prev_sub`?
*   [ ] Does the Scene class name start with `SceneXX`?
