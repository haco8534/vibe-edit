import os

file_path = r"d:\Program Projects\python\manim\scenes\diffusion_model_animation.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 置換ルール
replacements = [
    ("color=WHITE", "color=TEXT_MAIN"),
    ("color=GREY_B", "color=TEXT_DIM"),
    ("color=GREY_A", "color=TEXT_DIM"),
    ("speaker_color=WHITE", "speaker_color=TEXT_MAIN"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Theme applied successfully.")
