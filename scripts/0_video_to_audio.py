import os
import subprocess
import shutil
import platform

def get_ffmpeg_path():
    ffmpeg_env = os.environ.get("FFMPEG_PATH")
    if ffmpeg_env:
        return ffmpeg_env

    system = platform.system()
    if system == "Windows":
        return r"C:\ffmpeg\bin\ffmpeg.exe"
    elif system == "Darwin":
        return "/opt/homebrew/bin/ffmpeg"
    else:
        return "ffmpeg"

FFMPEG_PATH = get_ffmpeg_path()

def convert_videos_to_audio(video_dir, audio_dir, history_dir):
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(history_dir, exist_ok=True)

    for filename in os.listdir(video_dir):
        if filename.endswith((".mp4", ".avi", ".mkv")):
            video_path = os.path.join(video_dir, filename)
            audio_filename = f"{os.path.splitext(filename)[0]}.wav"
            audio_path = os.path.join(audio_dir, audio_filename)

            try:
                subprocess.run([
                    FFMPEG_PATH, "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", audio_path
                ], check=True)
                print(f"✔ [已转换] {filename} → {audio_path}")
            except subprocess.CalledProcessError:
                print(f"❌ [转换失败] {filename}，请检查 FFMPEG 路径与视频格式")
                continue

            shutil.move(video_path, os.path.join(history_dir, filename))
            print(f"↪ [已归档] {filename} → {history_dir}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    video_dir = os.path.join(base_dir, "data", "0_videos")
    audio_dir = os.path.join(base_dir, "data", "1_raw_audio")
    history_dir = os.path.join(video_dir, "history")

    convert_videos_to_audio(video_dir, audio_dir, history_dir)
    print("\n✅ 所有视频转换并归档完成！")