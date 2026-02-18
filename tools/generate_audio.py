import os
import re
import json
import argparse
import requests
import wave
import contextlib
from pathlib import Path

# Voicevox API設定
BASE_URL = "http://127.0.0.1:50021"

# Voicevox Speaker IDs
# ずんだもん: 3 (ノーマル), 1 (あまあま)
# 四国めたん: 2 (ノーマル), 0 (あまあま)
# 春日部つむぎ: 8
speaker_ids = {
    "ずんだもん": 3,
    "めたん": 2,
    "つむぎ": 8,
    "四国めたん": 2,
    "春日部つむぎ": 8
}

def get_wav_duration(path):
    """WAVファイルの再生時間を取得"""
    with contextlib.closing(wave.open(str(path), 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)

def generate_wav(text, speaker_id, output_path):
    """Voicevox APIを叩いてWAVを生成"""
    try:
        # 1. Audio Query
        params = {'text': text, 'speaker': speaker_id}
        response = requests.post(f"{BASE_URL}/audio_query", params=params)
        if response.status_code != 200:
            print(f"Error in audio_query: {response.text}")
            return False
        query_data = response.json()
        
        # 速度調整 (1.2倍)
        query_data["speedScale"] = 1.2

        # 2. Synthesis
        res2 = requests.post(
            f"{BASE_URL}/synthesis",
            params={"speaker": speaker_id},
            json=query_data
        )
        if res2.status_code != 200:
            print(f"Error (Synthesis): {res2.text}")
            return False

        # Save
        with open(output_path, "wb") as f:
            f.write(res2.content)
        return True

    except Exception as e:
        print(f"Exception connecting to Voicevox: {e}")
        return False

def parse_script(script_path):
    """Markdown台本をパースしてシーンごとのセリフリストを返す"""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # シーン分割 (例: ### Scene 01: ...)
    # 行頭の ### Scene ... で分割する
    scene_pattern = re.compile(r'^#+\s*(Scene\s*\w+).*$', re.MULTILINE)
    
    # セリフ抽出 (例: - **ずんだもん**: こんにちは)
    # **Name**: Text
    dialogue_pattern = re.compile(r'^\s*-\s*\*\*(.*?)\*\*\s*[:：]\s*(.*)$', re.MULTILINE)

    scenes = {}
    current_scene = "General"
    
    # 簡易的に行ごとに処理
    lines = content.split('\n')
    
    for line in lines:
        # Scene判定
        scene_match = scene_pattern.match(line)
        if scene_match:
            # "Scene 01" のような正規化されたキーを作る
            raw_scene_name = scene_match.group(1) # "Scene 01"
            # 空白除去して "Scene01" にする
            current_scene = raw_scene_name.replace(" ", "")
            scenes[current_scene] = []
            continue
            
        # Dialogue判定
        diag_match = dialogue_pattern.match(line)
        if diag_match:
            speaker = diag_match.group(1)
            text = diag_match.group(2)
            
            # カッコ書き（笑）などを除去
            text = re.sub(r'（.*?）', '', text)
            text = re.sub(r'\(.*?\)', '', text)
            
            if current_scene not in scenes:
                scenes[current_scene] = []
            
            scenes[current_scene].append({
                "speaker": speaker,
                "text": text
            })

    return scenes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project")
    args = parser.parse_args()

    project_dir = Path("d:/Program Projects/python/manim/projects") / args.project_name
    script_path = project_dir / "script.md"
    audio_dir = project_dir / "media" / "audio"
    
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return

    # 台本パース
    print(f"Parsing script: {script_path}")
    scenes_data = parse_script(script_path)
    
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # 音声生成
    audio_map = {}
    
    for scene_name, dialogues in scenes_data.items():
        print(f"Processing {scene_name}...")
        audio_map[scene_name] = []
        
        for i, diag in enumerate(dialogues):
            speaker = diag["speaker"]
            text = diag["text"]
            
            # ID決定
            sid = speaker_ids.get(speaker, 3) # デフォルトずんだもん
            
            # ファイル名: Scene01_001.wav
            filename = f"{scene_name}_{i:03d}.wav"
            filepath = audio_dir / filename
            
            # 生成 (ファイルがあればスキップするか？今は上書き)
            if not filepath.exists() or True: 
                print(f"  Generating: {speaker}: {text[:10]}...")
                success = generate_wav(text, sid, filepath)
                if not success:
                    print("  Failed to generate audio.")
                    continue
            
            duration = get_wav_duration(filepath)
            
            audio_map[scene_name].append({
                "index": i,
                "speaker": speaker,
                "text": text,
                "file": str(filepath.absolute()), # Manimには絶対パスを渡すのが無難
                "duration": duration
            })

    # マップ保存
    map_path = audio_dir / "audio_map.json"
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(audio_map, f, indent=2, ensure_ascii=False)
    
    print(f"Done! Audio map saved to {map_path}")

if __name__ == "__main__":
    main()
