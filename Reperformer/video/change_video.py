import os
import subprocess

def find_all_mp4_files(folder_path):
    """递归查找所有子文件夹下的 MP4 文件"""
    mp4_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.mp4'):
                full_path = os.path.join(root, file)
                mp4_files.append(full_path)
    return mp4_files

def convert_mp4_file(input_path, output_path):
    """执行 ffmpeg 转换"""
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-vf", "scale=1920:1080,fps=30",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ]

    print(f"正在转换: {input_path} -> {output_path}")
    try:
        subprocess.run(command, check=True)
        print(f"✅ 成功转换: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 转换失败: {input_path}")
        print(e)

def batch_convert_videos(root_folder, output_root=None):
    """批量转换所有找到的 MP4 文件"""
    if output_root is None:
        output_root = os.path.join(root_folder, "converted_videos")
    
    if not os.path.exists(output_root):
        os.makedirs(output_root)
    
    mp4_files = find_all_mp4_files(root_folder)
    print(f"共找到 {len(mp4_files)} 个 MP4 文件。")

    for input_path in mp4_files:
        # 保持相对路径结构
        relative_path = os.path.relpath(input_path, root_folder)
        output_path = os.path.join(output_root, os.path.splitext(relative_path)[0] + "_converted.mp4")

        # 创建对应的子文件夹
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 转换视频
        convert_mp4_file(input_path, output_path)

    print("🎉 全部转换完成！")

# 示例执行方式
if __name__ == "__main__":
    root_folder = r"C:\moqiyinlun\moqiyinlun.github.io\Reperformer\video"  # 替换为你的视频根目录
    output_folder = "converted_videos"  # 输出文件夹，可自定义
    batch_convert_videos(root_folder, output_folder)