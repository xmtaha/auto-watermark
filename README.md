# Auto Watermark Tool (Python + FFmpeg)

This small but effective Python tool allows you to add a transparent PNG watermark to your videos. The watermark is placed in the center of the video, automatically rescaled to the size of the video and appears at 15% opacity.

## Features

- Video file and PNG watermark selection (GUI)
- The watermark is placed in the center of the video
- Proportional sizing for all videos, vertical or horizontal
- Watermark visible with 15% opacity
- Fast and high quality processing with FFmpeg
- New file generation as MP4
- Windows compatible (with ffmpeg.exe)

## Requirements

- Python 3.7+
- `ffmpeg.exe` and `ffprobe.exe` must be in the **same folder** as this script (for Windows)
- No extra Python libraries are needed (`tkinter` and `subprocess` are sufficient)

