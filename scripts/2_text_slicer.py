import os
import re
import shutil

def get_paths():
    """
    获取项目路径结构
    :return: base_dir, fragments_folder, deepseek_folder, fragments_history_folder
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 获取当前脚本所在目录
    fragments_folder = os.path.join(base_dir, "data", "2_transcripts")  # 文本片段文件夹
    deepseek_folder = os.path.join(base_dir, "data", "3_slices")  # Deepseek 输出文件夹
    fragments_history_folder = os.path.join(base_dir, "data", "2_transcripts", "history")  # 历史文件夹路径
    return base_dir, fragments_folder, deepseek_folder, fragments_history_folder

# 获取路径
base_dir, fragments_folder, deepseek_folder, fragments_history_folder = get_paths()

def split_text(text, max_length=8000):
    """
    将长英文文本按句子分割，并保证每个片段长度不超过60K字符。
    :param text: 输入的长英文文本。
    :param max_length: 每个片段的最大长度，默认为60K字符。
    :return: 返回分片后的文本列表。
    """
    # 使用正则表达式按句号和空格分割句子，并保留句号
    sentences = re.split(r'(?<=\. )', text)
    
    print(f"句子总数：{len(sentences)}")  # 输出句子总数
    
    fragments = []
    current_fragment = ""
    
    for sentence in sentences:
        # 检查当前句子是否会导致片段超长
        if len(current_fragment) + len(sentence) + 2 > max_length:  # +2 是为了包括句号和空格
            if current_fragment:  # 如果当前片段非空，先保存它
                fragments.append(current_fragment)
            # 开始一个新片段
            current_fragment = sentence
        else:
            # 将句子加到当前片段
            if current_fragment:
                current_fragment += sentence
            else:
                current_fragment = sentence

    # 添加最后一个片段
    if current_fragment:
        fragments.append(current_fragment)
    
    print(f"分割后的片段总数：{len(fragments)}")  # 输出分片的总数
    return fragments

def save_fragments(fragments, output_folder):
    """
    将分片后的英文文本保存为多个文件
    :param fragments: 分片后的文本列表
    :param output_folder: 输出文件夹路径
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, fragment in enumerate(fragments):
        output_file = os.path.join(output_folder, f"fragment_{i:02d}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(fragment)
        print(f"保存：{output_file}")

def move_original_to_history(file_path, history_folder):
    """
    将原始文本文件移动到 Fragments_history 文件夹
    :param file_path: 原始文件路径
    :param history_folder: 历史文件夹路径
    """
    if not os.path.exists(history_folder):
        os.makedirs(history_folder)

    # 获取文件名和目标路径
    file_name = os.path.basename(file_path)
    history_file_path = os.path.join(history_folder, file_name)
    
    # 移动原始文件到历史文件夹
    shutil.move(file_path, history_file_path)
    print(f"移动原始文件到 Fragments_history 文件夹：{history_file_path}")

def move_folder_to_deepseek(source_folder, deepseek_folder):
    """
    将包含片段的文件夹整体移动到 Deepseek 文件夹
    :param source_folder: 包含片段的文件夹
    :param deepseek_folder: Deepseek 文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(deepseek_folder):
        os.makedirs(deepseek_folder)

    folder_name = os.path.basename(source_folder)  # 获取源文件夹名称
    target_folder = os.path.join(deepseek_folder, folder_name)  # 设置目标路径
    
    # 移动整个文件夹到 Deepseek 文件夹
    shutil.move(source_folder, target_folder)
    print(f"移动文件夹到 Deepseek 文件夹：{target_folder}")

def process_files_in_directory(directory):
    """
    获取目录下所有的 txt 文件，对每个文件进行分割并保存到单独的文件夹中
    :param directory: 目标目录
    """
    txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    print(f"找到 {len(txt_files)} 个 txt 文件")  # 输出找到的 txt 文件数量
    
    for txt_file in txt_files:
        print(f"正在处理：{txt_file}")
        
        file_path = os.path.join(directory, txt_file)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        
        # 分割文本
        fragments = split_text(text)
        
        # 为每个文件创建独立的文件夹
        output_folder = os.path.join(directory, os.path.splitext(txt_file)[0])
        
        # 保存分割后的文本
        save_fragments(fragments, output_folder)
        
        # 将原始文件移动到 Fragments_history 文件夹
        move_original_to_history(file_path, fragments_history_folder)
        
        # 将包含片段的文件夹移动到 Deepseek 文件夹
        move_folder_to_deepseek(output_folder, deepseek_folder)

# 使用相对路径处理文件
process_files_in_directory(fragments_folder)