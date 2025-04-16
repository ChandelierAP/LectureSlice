import os
import shutil

# 获取项目根路径
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 设置4_Final_Outputs文件夹路径
final_outputs_folder = os.path.join(base_dir, "data", "4_outputs")
final_outputs_history_folder = os.path.join(final_outputs_folder, "history")
final_markdown_folder = os.path.join(base_dir, "data", "5_markdowns")

# 确保4_Final_Outputs文件夹和历史文件夹存在
os.makedirs(final_outputs_folder, exist_ok=True)
os.makedirs(final_outputs_history_folder, exist_ok=True)
os.makedirs(final_markdown_folder, exist_ok=True)

# 目标文件夹路径，用于存放合并的md文件
output_folder = final_markdown_folder

# 打印处理目录，确保脚本在正确的目录中运行
print(f"处理目录: {final_markdown_folder}")

# 遍历4_Final_Outputs文件夹，查找所有子文件夹
for subfolder in os.scandir(final_outputs_folder):
    if subfolder.is_dir():
        folder_name = subfolder.name
        
        # 获取当前子文件夹中的所有.md文件
        md_files = [f for f in os.listdir(subfolder.path) if f.endswith(".md")]
        
        # 调试输出，查看当前子文件夹中的md文件
        print(f"子文件夹 {subfolder.path} 中的md文件：")
        print(md_files)

        if md_files:  # 如果文件夹内有.md文件
            print(f"正在处理文件夹: {folder_name}")
            
            # 对文件按名称进行排序，以确保顺序正确
            md_files.sort()  # 按文件名排序
            
            # 创建新的.md文件，名字为文件夹名
            merged_file_path = os.path.join(output_folder, f"{folder_name}.md")
            
            with open(merged_file_path, "w", encoding="utf-8") as merged_file:
                # 遍历该文件夹中的所有.md文件并将它们合并
                for md_file in md_files:
                    md_file_path = os.path.join(subfolder.path, md_file)
                    
                    with open(md_file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        merged_file.write(f"\n\n# {md_file}\n\n")  # 为每个文件添加标题
                        merged_file.write(content)
                        merged_file.write("\n\n")  # 每个文件之间添加空行

            print(f"合并后的文件已保存为: {merged_file_path}")

            # 将处理过的文件夹及其内容转移到 history 文件夹
            target_history_folder = os.path.join(final_outputs_history_folder, folder_name)
            shutil.move(subfolder.path, target_history_folder)  # 直接移动子文件夹到目标路径
            print(f"已将文件夹 {folder_name} 移动到 {target_history_folder}")

print("所有文件夹处理完成！")