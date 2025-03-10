# **LectureSlice**

## **项目结构**
```bash
project-root/
│── data/                  # 统一数据存储目录
│   ├── raw_audio/         # 原始音频文件
│   │   ├── history/       # 存储历史音频
│   ├── videos/            # 原始视频文件
│   │   ├── history/       # 存储历史视频
│   ├── transcripts/       # 语音转文本结果
│   │   ├── history/       # 存储历史文本
│   ├── sentences/         # 按句分割的文本
│   │   ├── history/       # 存储历史分句
│   ├── similarities/      # 相邻语句相似度数据
│   │   ├── history/       # 存储历史相似度计算
│   ├── cut_points/        # 语义切割点
│   │   ├── history/       # 存储历史切割点
│   ├── segments/          # 最终切割后的段落
│   │   ├── history/       # 存储历史分段
│   ├── output/            # 结构化输出（JSON / Markdown）
│   │   ├── history/       # 存储历史输出
│
│── scripts/               # 核心处理脚本
│   ├── 0_extract_audio.py  # 视频提取音轨
│   ├── 1_transcribe.py    # 音频转文本
│   ├── 2_split_sentences.py # 分句处理
│   ├── 3_compute_similarity.py # 计算相邻语句相似度
│   ├── 4_detect_cut.py    # 生成切割点
│   ├── 5_segment_text.py  # 按切割点分段
│   ├── run_pipeline.sh     # 一键运行完整流程的脚本
│   ├── utils.py           # 公共工具函数
│
│── models/                # 机器学习模型（BERT 句向量等）
│   ├── sentence_transformer/  # 预训练模型文件
│   ├── whisper/           # Whisper 语音识别模型（可选）
│
│── web/                   # 可选的 Web 端
│   ├── api.py             # FastAPI 端点
│   ├── app.py             # Streamlit 界面
│
│── requirements.txt       # 依赖库
│── README.md              # 项目说明

## **如何运行完整流程**
### **一键运行所有步骤**
你可以使用 `run_pipeline.sh` 来自动执行所有处理步骤：
```bash
bash run_pipeline.sh
```

### **逐步执行**
如果你希望逐步执行每个阶段，可以按照以下顺序运行：
```bash
python scripts/0_extract_audio.py  # 提取音频
python scripts/1_transcribe.py      # 音频转文本
python scripts/2_split_sentences.py # 分句处理
python scripts/3_compute_similarity.py # 计算相邻语句相似度
python scripts/4_detect_cut.py      # 生成切割点
python scripts/5_segment_text.py    # 按切割点分段
```

### **示例**
```bash
bash run_pipeline.sh data/videos/sample.mp4
```

这样会处理 `sample.mp4`，提取音频并转换为结构化文本。