import subprocess
import os
import multiprocessing
import time
import shutil
import argparse
import re
import sys

# デフォルト設定
QUALITY = "-qm"  # -qm: 720p30, -qh: 1080p60
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

def get_scenes_from_file(file_path):
    """ファイル内のSceneクラス定義を正規表現で抽出する"""
    scenes = []
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        # class SceneName(Scene): または class SceneName(MovingCameraScene): などを検出
        # 継承元の括弧内に 'Scene' が含まれるものを対象とする
        matches = re.findall(r"class\s+(\w+)\s*\(.*Scene.*\):", content)
        scenes = matches
    return scenes

def run_render_wrapper(args):
    """multiprocessing用のラッパー関数"""
    return run_render(*args)

def run_render(project_name, scene_name, quality):
    """単一のシーンをレンダリングする関数"""
    
    project_dir = os.path.join(PROJECTS_DIR, project_name)
    file_path = os.path.join(project_dir, "animation.py")
    
    # プロジェクトごとの一時mediaディレクトリ
    temp_media_dir = os.path.join(project_dir, "temp_media", scene_name)
    os.makedirs(temp_media_dir, exist_ok=True)
    
    print(f"Starting: {scene_name}")
    start_time = time.time()
    
    # --media_dir を指定して完全に分離
    cmd = ["manim", "render", quality, "--media_dir", temp_media_dir, file_path, scene_name]
    
    # 既存の環境変数にMiKTeXパスを追加
    env = os.environ.copy()
    miktex_bin = r"C:\Users\81804\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
    if miktex_bin not in env["PATH"]:
        env["PATH"] += f";{miktex_bin}"
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    elapsed = time.time() - start_time
    status = "SUCCESS" if result.returncode == 0 else "FAILED"
    
    if status == "SUCCESS":
        # 生成された動画を本来の場所に移動
        # 構造: temp_media/SceneName/videos/animation/720p30/SceneName.mp4
        res_folder = "720p30" if quality == "-qm" else "1080p60"
        
        src_video = os.path.join(temp_media_dir, "videos", "animation", res_folder, f"{scene_name}.mp4")
        
        # プロジェクト内のmedia/videosに出力
        # projects/<project_name>/media/videos/animation/<quality>
        dest_dir = os.path.join(project_dir, "media", "videos", "animation", res_folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest_video = os.path.join(dest_dir, f"{scene_name}.mp4")
        
        if os.path.exists(src_video):
            shutil.move(src_video, dest_video)
        else:
            print(f"Warning: Video file not found at {src_video}")
            status = "MISSING_FILE"

    print(f"Finished: {scene_name} ({status}) in {elapsed:.1f}s")
    if result.returncode != 0:
        print(f"--- Error Log for {scene_name} ---")
        print(result.stderr)
        print("--------------------------------")
    
    return status

def main():
    parser = argparse.ArgumentParser(description="Parallel render script for Manim projects")
    parser.add_argument("project_name", help="Name of the project folder in 'projects/'")
    parser.add_argument("--quality", "-q", default="-qm", help="Render quality (-qm or -qh)")
    parser.add_argument("--scenes", "-s", nargs="+", help="Specific scenes to render (default: all)")
    args = parser.parse_args()

    project_dir = os.path.join(PROJECTS_DIR, args.project_name)
    file_path = os.path.join(project_dir, "animation.py")

    if not os.path.exists(project_dir):
        print(f"Error: Project '{args.project_name}' not found in {PROJECTS_DIR}")
        return
    
    if not os.path.exists(file_path):
        print(f"Error: animation.py not found in {project_dir}")
        return

    # シーンの自動検出
    if args.scenes:
        scenes = args.scenes
    else:
        scenes = get_scenes_from_file(file_path)
        if not scenes:
            print("No scenes found in animation.py")
            return

    print(f"Target Project: {args.project_name}")
    print(f"Target Scenes ({len(scenes)}): {scenes}")
    print(f"Quality: {args.quality}")
    print("-" * 40)

    # 並列処理の実行
    num_processes = min(multiprocessing.cpu_count(), 4)
    if len(scenes) < num_processes:
        num_processes = len(scenes)

    pool_args = [(args.project_name, scene, args.quality) for scene in scenes]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(run_render_wrapper, pool_args)

    print("-" * 40)
    print("Results:", results)
    
    create_concat_list(args.project_name, args.quality)

def create_concat_list(project_name, quality):
    """結合用のリストファイルを作成し、ffmpegコマンドを表示する"""
    res_folder = "720p30" if quality == "-qm" else "1080p60"
    
    # プロジェクト内の出力ディレクトリ: projects/<project_name>/media/videos/animation/<quality>
    project_dir = os.path.join(PROJECTS_DIR, project_name)
    output_dir = os.path.join(project_dir, "media", "videos", "animation", res_folder)
    concat_file = os.path.join(output_dir, "concat_list.txt")
    
    if not os.path.exists(output_dir):
        print(f"Directory not found: {output_dir}")
        return

    file_path = os.path.join(project_dir, "animation.py")
    all_scenes = get_scenes_from_file(file_path)
    
    if not all_scenes:
        print("No scenes found in animation.py, cannot create concat list.")
        return

    valid_scenes = []
    for scene in all_scenes:
        mp4_path = os.path.join(output_dir, f"{scene}.mp4")
        if os.path.exists(mp4_path):
            valid_scenes.append(scene)
    
    if not valid_scenes:
        print("No rendered videos found to concatenate.")
        return

    with open(concat_file, "w", encoding="utf-8") as f:
        for scene in valid_scenes:
            f.write(f"file '{scene}.mp4'\n")
    
    print(f"Concat list created at: {concat_file}")
    
    # 結合コマンドの表示
    # outputsフォルダへの相対パス: ../../../../../outputs/<project_name>.mp4
    # current: projects/project/media/videos/animation/720p30 (5階層下)
    final_output_path = f"../../../../../outputs/{project_name}.mp4"
    
    print("\nTo concatenate all scenes, run:")
    print(f"cd \"{output_dir}\"")
    print(f"ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy \"{final_output_path}\"")

if __name__ == "__main__":
    multiprocessing.freeze_support() # Windowsでのmultiprocessing対策
    main()
