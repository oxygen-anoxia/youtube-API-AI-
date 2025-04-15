import os
import subprocess
from openai import OpenAI


url_txt = "urls.txt"           # 包含 YouTube 链接的 txt 文件
save_dir = "downloads"         # 下载与输出目录
api_key = ""  # 替换为你的 OpenAI API Key
base_url = "https://openrouter.ai/api/v1"
max_tokens = 5000


def download_video_and_subtitles(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", "-m", "yt_dlp",
        "--write-auto-sub", "--sub-lang", "en",
        "--skip-download",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    subprocess.run(command, shell=True)


def extract_unique_lines_from_vtt(vtt_path):
    output_lines = []
    previous_line = ""

    with open(vtt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()
        if "start position:0%" in line and i + 1 < len(lines):
            content = lines[i + 1].strip()
            if content and content != previous_line:
                output_lines.append(content)
                previous_line = content

    return ' '.join(output_lines)


def process_all_urls(url_file, output_dir):
    with open(url_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        print(f"\n🎬 正在处理: {url}")
        download_video_and_subtitles(url, output_dir)

    processed_txt_files = []

    for file in os.listdir(output_dir):
        if file.endswith(".vtt"):
            vtt_path = os.path.join(output_dir, file)
            clean_text = extract_unique_lines_from_vtt(vtt_path)

            txt_path = vtt_path.replace(".vtt", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
            print(f"✅ 已生成字幕文本: {txt_path}")

            processed_txt_files.append(txt_path)

    return processed_txt_files


def summarize_txts_with_context(txt_paths):
    """
    批量对多个字幕 txt 文件进行上下文总结，输出为 *_summary.txt 文件。
    """
    client = OpenAI(api_key=api_key, base_url=base_url,
                    default_headers={  # 关键修改点
                        "HTTP-Referer": "http://localhost",  # 本地开发专用标识
                        "X-Title": "Youtube Summary Tool"    # 应用名称（可自定义）
                    })

    for txt_path in txt_paths:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 分段文本
        chunk_size = 3000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        messages = [
            {"role": "system", "content": "你是一个字幕总结专家，帮助用户准确理解视频内容，特别关注各种软件和平台的使用流程。"}
        ]

        for i, chunk in enumerate(chunks):
            messages.append({
                "role": "user",
                "content": f"这是视频字幕的第 {i+1} 段，请阅读并记住内容，稍后我会让你总结：\n{chunk}"
            })

        messages.append({
            "role": "user",
            "content": "现在请你对前面所有提供的字幕内容进行整体总结。请细致说明字幕中提到的软件和平台是如何被使用的，尤其要保留操作步骤和关键细节。"
        })

        print(f"🧠 正在进行上下文总结：{txt_path}")
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.5
        )

        summary = response.choices[0].message.content

        output_path = txt_path.replace(".txt", "_summary.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"✅ 总结完成，保存于：{output_path}")


if __name__ == "__main__":

    # Step 1: 下载视频字幕 + 提取 txt
    txt_files = process_all_urls(url_txt, save_dir)

    # Step 2: 使用 OpenAI API 总结
    summarize_txts_with_context(txt_files)
