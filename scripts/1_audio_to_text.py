import os
import whisper
import shutil
import torch

def get_paths():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    audio_folder = os.path.join(base_dir, "data", "1_raw_audio")
    transcript_folder = os.path.join(base_dir, "data", "2_transcripts")
    history_folder = os.path.join(audio_folder, "history")
    os.makedirs(transcript_folder, exist_ok=True)
    os.makedirs(history_folder, exist_ok=True)
    return audio_folder, transcript_folder, history_folder

def transcribe_audio_files(model, audio_folder, transcript_folder, history_folder):
    # 处理音频文件并生成转录文本
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith(".wav")]

    for filename in audio_files:
        print(f"🎧 开始处理：{filename}")
        audio_path = os.path.join(audio_folder, filename)

        #选定转译语言
        # result = model.transcribe(audio_path, language="zh")
        result = model.transcribe(audio_path, language="en")
        transcript = result["text"]

        text_filename = f"{os.path.splitext(filename)[0]}.txt"
        text_path = os.path.join(transcript_folder, text_filename)

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        shutil.move(audio_path, os.path.join(history_folder, filename))
        print(f"✅ 已完成并归档：{text_filename}")

if __name__ == "__main__":
    audio_folder, transcript_folder, history_folder = get_paths()
    
    # 自动检测是否支持 CUDA（NVIDIA GPU），否则回退为 CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 加载 Whisper 模型，可选模型包括：
    # ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en',
    #  'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 'large-v3']
    # 可将 "medium.en" 替换为其他模型名
    model = whisper.load_model("tiny.en", device=device)  # 可替换为 "cpu" 以兼容无 GPU 环境
    transcribe_audio_files(model, audio_folder, transcript_folder, history_folder)
    print("\n🎉 所有音频文件转换并归档完成！")