# **LectureSlice**

## **项目介绍**
LectureSlice 是一个分阶段文本处理管道，旨在将视频讲座内容自动转录、语义切片、智能翻译并最终整理为高质量的 Markdown 文档。

本项目的目标是：

- 支持将视频自动转为结构化的讲义笔记；
- 结合 Whisper 和大语言模型提升内容理解与生成质量；
- 全流程自动归档每一步中间产物，便于复现与迭代；
- 最终输出结构清晰、便于查阅和发布的 Markdown 文件。

## **项目结构**
```bash
project-root/
│── data/                        # 统一数据目录
│   ├── 0_videos/                # 原始视频
│   │   └── history/             # 归档已处理视频
│   ├── 1_raw_audio/            # 提取的音频
│   │   └── history/
│   ├── 2_transcripts/          # Whisper转录的文本
│   │   └── history/
│   ├── 3_slices/               # 切分后的文本片段
│   │   └── history/
│   ├── 4_outputs/              # LLM处理后的输出片段
│   │   └── history/
│   ├── 5_markdowns/            # 合并后的最终 Markdown 结果
│
│── scripts/                    # 核心脚本目录
│   ├── 0_video_to_audio.py     # 提取音频
│   ├── 1_audio_to_text.py      # Whisper 语音转文字
│   ├── 2_text_slicer.py        # 文本切片
│   ├── 3_LLM_processor.py      # 调用大模型处理切片
│   ├── 4_markdown_generator.py # 合并输出 Markdown
│
│── models/                     # 预训练模型目录
│   ├── sentence_transformer/
│   ├── whisper/
│
│── requirements.txt            # Python 依赖
│── README.md                   # 本文件
```

## **如何运行完整流程**


### 🧩 分步骤执行（调试或替换阶段组件）
```bash
python scripts/0_video_to_audio.py        # 视频提取音频
python scripts/1_audio_to_text.py         # 音频转文字（Whisper）
python scripts/2_text_slicer.py           # 文本切句/分片
python scripts/3_LLM_processor.py         # 使用大模型理解片段
python scripts/4_markdown_generator.py    # 合并为完整 Markdown
```

### 📂 输出结构说明
最终结果将保存在：
```
data/5_markdowns/
```
每个合并文件对应一个处理子目录的完整讲义 Markdown 结果。