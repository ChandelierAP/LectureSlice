import os

# 定义项目结构
project_structure = {
    "data": ["raw_audio", "transcripts", "sentences", "similarities", "cut_points", "segments", "output"],
    "scripts": [
        "1_transcribe.py",
        "2_split_sentences.py",
        "3_compute_similarity.py",
        "4_detect_cut.py",
        "5_segment_text.py",
        "utils.py"
    ],
    "models": ["sentence_transformer", "whisper"],
    "web": ["api.py", "app.py"],
    "root_files": ["requirements.txt", "README.md"]
}

def create_project_structure(base_path="project-root"):
    os.makedirs(base_path, exist_ok=True)
    
    # 创建数据文件夹
    for folder in project_structure["data"]:
        os.makedirs(os.path.join(base_path, "data", folder), exist_ok=True)

    # 创建脚本文件
    scripts_path = os.path.join(base_path, "scripts")
    os.makedirs(scripts_path, exist_ok=True)
    for script in project_structure["scripts"]:
        script_path = os.path.join(scripts_path, script)
        open(script_path, "w").close()  # 创建空白文件

    # 创建模型文件夹
    for folder in project_structure["models"]:
        os.makedirs(os.path.join(base_path, "models", folder), exist_ok=True)

    # 创建 Web 目录
    web_path = os.path.join(base_path, "web")
    os.makedirs(web_path, exist_ok=True)
    for web_file in project_structure["web"]:
        web_file_path = os.path.join(web_path, web_file)
        open(web_file_path, "w").close()

    # 创建根目录的文件
    for root_file in project_structure["root_files"]:
        open(os.path.join(base_path, root_file), "w").close()

    print(f"项目结构已创建在 {base_path} 目录下")

# 运行脚本
create_project_structure()