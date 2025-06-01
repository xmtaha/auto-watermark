import subprocess
import os
from tkinter import Tk, filedialog
import tempfile
import sys

def resource_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), filename)

def select_file(title, filetypes):
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return path

def get_video_resolution(video_path, ffprobe_path):
    cmd = [
        ffprobe_path, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    width, height = map(int, result.stdout.strip().split("\n"))
    return width, height

def apply_watermark(video_path, watermark_path, output_path, ffmpeg_path, ffprobe_path):
    video_w, video_h = get_video_resolution(video_path, ffprobe_path)

    max_w = int(video_w * 0.3)
    max_h = int(video_h * 0.3)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_wm:
        temp_wm_path = temp_wm.name

    resize_filter = (
        f"scale='if(gt(a,1),min(iw\\,{max_w}),-1)':'if(lte(a,1),min(ih\\,{max_h}),-1)',"
        f"format=rgba,colorchannelmixer=aa=0.15"
    )

    resize_cmd = [
        ffmpeg_path, "-y",
        "-i", watermark_path,
        "-vf", resize_filter,
        temp_wm_path
    ]
    subprocess.run(resize_cmd, check=True)

    overlay_cmd = [
        ffmpeg_path, "-y",
        "-i", video_path,
        "-i", temp_wm_path,
        "-filter_complex", "overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(overlay_cmd, check=True)

    os.remove(temp_wm_path)

def main():
    ffmpeg_path = resource_path("ffmpeg.exe")
    ffprobe_path = resource_path("ffprobe.exe")

    if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
        print("ffmpeg.exe or ffprobe.exe not found in the same directory.")
        return

    video = select_file("Select a video file", [("Video files", "*.mp4 *.mkv *.mov *.avi")])
    if not video:
        print("No video file selected.")
        return

    watermark = select_file("Select a PNG watermark file", [("PNG files", "*.png")])
    if not watermark:
        print("No watermark selected.")
        return

    output = os.path.splitext(video)[0] + "_watermarked.mp4"

    print("Processing, please wait...")
    apply_watermark(video, watermark, output, ffmpeg_path, ffprobe_path)
    print(f"Done! Saved as: {output}")

if __name__ == "__main__":
    main()
