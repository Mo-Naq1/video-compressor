import os
import subprocess
import shutil




def calculate_bitrate(target_size_mb, duration_seconds):
    # Convert target size from MB to bits
    target_size_bits = target_size_mb * 8 * 1024 * 1024
    # Calculate bitrate in bits per second
    bitrate = target_size_bits / duration_seconds
    # Convert to kilobits per second
    bitrate_kbps = bitrate / 1000
    return bitrate_kbps

def get_video_duration(file_path):
    # Use FFmpeg to get the duration of the video
    result = subprocess.run(
        ["ffmpeg", "-i", file_path, "-hide_banner"], 
        stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    for line in result.stderr.split('\n'):
        if "Duration" in line:
            duration = line.split(",")[0].split("Duration:")[1].strip()
            h, m, s = duration.split(":")
            seconds = int(h) * 3600 + int(m) * 60 + float(s)
            return seconds
    return None
def compress_video(input_path, output_path, target_size_mb):
    duration = get_video_duration(input_path)
    if duration is None:
        print(f"Could not determine duration for {input_path}")
        return

    bitrate = calculate_bitrate(target_size_mb, duration)
    ffmpeg_cmd = f'ffmpeg -i "{input_path}" -b:v {bitrate:.0f}k -c:v libx264 -c:a copy "{output_path}"'
    try:
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        os.remove(input_path)
        shutil.move(output_path, r'C:\Users\mohdn\OneDrive\Desktop\compressed_videos\finished')
        print(f"Compressed: {input_path} to {output_path} with target size {target_size_mb} MB")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def compress_videos_in_folder(folder_path, target_size_mb):
    for filename in os.listdir(folder_path):
        if filename.endswith('.mov') or filename.endswith('.mp4'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"compressed_{filename}")
            compress_video(input_path, output_path, target_size_mb)
         
folder_path = r"FILE PATH" # FILE PATH to compressed_videos folder
target_size_mb = 25  # Target size in megabytes
compress_videos_in_folder(folder_path, target_size_mb)