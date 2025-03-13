import os
import subprocess

def convert_videos_in_folder(folder_path, output_folder=None):
    # 如果不指定输出文件夹，默认输出在原文件夹
    if output_folder is None:
        output_folder = folder_path

    # 创建输出文件夹如果不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 找到所有.mp4文件
    mp4_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
    print(f"找到 {len(mp4_files)} 个 MP4 文件：{mp4_files}")

    # 遍历所有文件
    for file_name in mp4_files:
        input_path = os.path.join(folder_path, file_name)
        output_name = os.path.splitext(file_name)[0] + "_converted.mp4"
        output_path = os.path.join(output_folder, output_name)

        # ffmpeg 命令
        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-vf", "scale=1280:720,fps=30",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path
        ]

        # 执行命令
        print(f"正在转换: {file_name} -> {output_name}")
        try:
            subprocess.run(command, check=True)
            print(f"✅ 成功转换: {output_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 转换失败: {file_name}")
            print(e)

    print("全部转换完成！")

# 示例调用方式
if __name__ == "__main__":
    folder = "comparison"  # 这里替换为你的文件夹路径
    output_folder = "converted_videos"  # 转换后保存的位置，默认可以为 None
    convert_videos_in_folder(folder, output_folder)