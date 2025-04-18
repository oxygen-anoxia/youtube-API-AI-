import subprocess
import re


def extract_playlist_id(url):
    """
    从 YouTube 视频 URL 中提取播放列表 ID。
    """
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        return None


def save_playlist_urls(video_url, output_file='urls.txt'):
    """
    使用 yt-dlp 提取播放列表中的所有视频链接并保存到文件。
    """
    playlist_id = extract_playlist_id(video_url)
    if not playlist_id:
        print("未找到播放列表 ID。请确保输入的 URL 包含 'list=' 参数。")
        return

    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

    command = [
        "python", "-m", "yt_dlp",
        "--flat-playlist",
        "-i",
        "--print-to-file", "url", output_file,
        playlist_url
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ 播放列表中的视频链接已保存到 {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 提取视频链接时出错：{e}")


# 示例用法
if __name__ == "__main__":
    input_url = input("请输入包含播放列表的 YouTube 视频链接：\n")
    save_playlist_urls(input_url)
