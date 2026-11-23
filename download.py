#!/usr/bin/env python3
"""Download a YouTube video (or a section of it) with yt-dlp + ffmpeg.

Usage:
    python download.py <url>
    python download.py <url> --start 1:30 --end 2:10
    python download.py <url> --audio
    python download.py <url> --height 720 --out clips

Only download videos you own or have permission to use.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

# Antivirus HTTPS scanning (e.g. Avast) re-signs connections with its own CA.
# truststore makes Python use the Windows certificate store, which trusts it.
try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    print("note: 'truststore' not installed; SSL errors are possible "
          "(pip install truststore)", file=sys.stderr)

try:
    import yt_dlp
    from yt_dlp.utils import download_range_func
except ImportError:
    sys.exit("yt-dlp is not installed. Run: pip install -r requirements.txt")

DEFAULT_FFMPEG_DIR = Path(r"C:\Users\HP\yt-dlp\ytdlp-tools")
DEFAULT_OUT = Path(__file__).resolve().parent / "downloads"


def to_seconds(value: str) -> float:
    """Accept 90, 1:30 or 1:02:03 and return seconds."""
    if not re.fullmatch(r"\d+(:\d{1,2}){0,2}(\.\d+)?", value):
        raise argparse.ArgumentTypeError(f"bad time '{value}' (use 90, 1:30 or 1:02:03)")
    seconds = 0.0
    for part in value.split(":"):
        seconds = seconds * 60 + float(part)
    return seconds


def find_ffmpeg() -> str | None:
    if shutil.which("ffmpeg"):
        return None  # already on PATH
    if (DEFAULT_FFMPEG_DIR / "ffmpeg.exe").exists():
        return str(DEFAULT_FFMPEG_DIR)
    sys.exit("ffmpeg not found. Add it to PATH or edit DEFAULT_FFMPEG_DIR.")


def main() -> None:
    p = argparse.ArgumentParser(description="Download a YouTube video with yt-dlp.")
    p.add_argument("url", help="YouTube link")
    p.add_argument("--start", type=to_seconds, help="clip start, e.g. 1:30")
    p.add_argument("--end", type=to_seconds, help="clip end, e.g. 2:10")
    p.add_argument("--audio", action="store_true", help="audio only (mp3)")
    p.add_argument("--height", type=int, default=1080, help="max video height (default 1080)")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output folder")
    args = p.parse_args()

    if args.start is not None and args.end is not None and args.end <= args.start:
        sys.exit("--end must be after --start")

    args.out.mkdir(parents=True, exist_ok=True)

    opts = {
        "outtmpl": str(args.out / "%(title)s.%(ext)s"),
        "windowsfilenames": True,
        "noplaylist": True,
    }
    ffmpeg_dir = find_ffmpeg()
    if ffmpeg_dir:
        opts["ffmpeg_location"] = ffmpeg_dir

    if args.audio:
        opts["format"] = "ba/b"
        opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]
    else:
        opts["format"] = f"bv*[height<={args.height}]+ba/b[height<={args.height}]/b"
        opts["merge_output_format"] = "mp4"

    if args.start is not None or args.end is not None:
        opts["download_ranges"] = download_range_func(
            None, [(args.start or 0, args.end or float("inf"))]
        )
        opts["force_keyframes_at_cuts"] = True  # accurate cut points

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([args.url])

    print(f"\nDone. Saved to: {args.out}")


if __name__ == "__main__":
    main()
