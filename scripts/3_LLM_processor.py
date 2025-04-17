import os
import shutil
import time
from openai import OpenAI
from tqdm import tqdm  # 用于显示进度条
from dotenv import load_dotenv
load_dotenv()

# 设置项目路径（项目根目录为 base_dir）
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
folder_directory = os.path.join(base_dir, "data", "3_slices")  # 输入文件夹路径
trans_folder = os.path.join(base_dir, "data", "4_outputs")  # 输出文件夹路径
history_folder = os.path.join(base_dir, "data", "3_slices", "history")  # 历史文件夹路径

# 多个 API Key
API_KEYS = os.getenv("DEEPSEEK_API_KEYS", "").split(",")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")

# 当前 key 索引
api_key_index = 0
client = OpenAI(api_key=API_KEYS[api_key_index], base_url=BASE_URL)

# 设置 Prompt 变量
Prompt = "Given a set of text slices from a video lecture (in English) that I have transcribed, please provide a clear, concise Chinese translation for each slice while maintaining context between slices, as the content of a single topic may be split across multiple parts. Highlight the key technical terms by marking them in both English and Chinese. Ensure that the explanations are accurate and easy to understand, especially for professional terms, while preserving the flow and continuity of the lecture."

# 创建新的文件夹路径（与原文件夹同层，名称为原文件夹名 + "_trans"）
if not os.path.exists(trans_folder):
    os.makedirs(trans_folder)

# 确保历史文件夹存在
if not os.path.exists(history_folder):
    os.makedirs(history_folder)

# 递归遍历子文件夹中的所有txt文件
def process_files_with_retry(subfolder):
    global api_key_index
    global client

    # 获取当前子文件夹中的所有txt文件
    txt_files = [f for f in os.listdir(subfolder) if f.endswith(".txt")]

    # 显示进度条
    with tqdm(total=len(txt_files), desc=f"Processing {subfolder}", unit="file") as pbar:
        for txt_file in txt_files:
            txt_file_path = os.path.join(subfolder, txt_file)

            # 读取txt文件内容
            with open(txt_file_path, "r") as f:
                file_content = f.read()

            # 设置重试机制
            retries = 5
            for attempt in range(retries):
                try:
                    # 发送API请求
                    response = client.chat.completions.create(
                        model=os.getenv("LLM_MODEL", "deepseek-chat"),
                        messages=[
                            {"role": "system", "content": Prompt},
                            {"role": "user", "content": file_content},
                        ],
                        stream=False
                    )

                    # 获取并保存模型的响应
                    model_response = response.choices[0].message.content

                    # 确保在输出文件夹中创建子文件夹结构
                    output_subfolder = os.path.join(trans_folder, os.path.basename(subfolder))
                    if not os.path.exists(output_subfolder):
                        os.makedirs(output_subfolder)

                    # 修改文件扩展名为.md，保存处理结果，保持MD格式
                    result_file_path = os.path.join(output_subfolder, os.path.splitext(txt_file)[0] + ".md")
                    with open(result_file_path, "w", encoding="utf-8") as result_f:
                        result_f.write(model_response)

                    # 确保目标历史文件夹存在
                    target_history_folder = os.path.join(history_folder, os.path.basename(subfolder))

                    # 如果目标文件夹不存在，创建它
                    if not os.path.exists(target_history_folder):
                        os.makedirs(target_history_folder)

                    # 移动原始txt文件到历史文件夹
                    shutil.move(txt_file_path, os.path.join(target_history_folder, txt_file))

                    # 更新进度条
                    pbar.update(1)

                    break  # 成功时跳出重试循环

                except Exception as e:
                    print(f"请求失败: {e}. 尝试重新连接 ({attempt + 1}/{retries})")
                    if attempt < retries - 1:
                        # 切换到下一个 key
                        api_key_index = (api_key_index + 1) % len(API_KEYS)
                        client = OpenAI(api_key=API_KEYS[api_key_index], base_url=BASE_URL)
                        time.sleep(2 ** attempt)  # 指数回退（例如，2^1, 2^2 秒等待）
                    else:
                        print("达到最大重试次数，跳过此文件。")
                        pbar.update(1)
                        break


# 调试输出，查看文件夹路径
print(f"文件夹 {folder_directory} 中的子文件夹：")
subfolders = [f.path for f in os.scandir(folder_directory) if f.is_dir()]
print(subfolders)

# 处理每个子文件夹中的文本文件
for subfolder in subfolders:
    process_files_with_retry(subfolder)

print(f"Results saved to the folder: {trans_folder}")