import logging
import os
import yt_dlp
from yt_dlp.utils import sanitize_filename
import json


class YouTubeDownloader:
    def __init__(self, output_path: str = "downloads"):
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)


    def download(self, url: str, format_id: int):
        try:
            yt_dlp_options = {
                "format" : format_id,
                "outtmpl": f"{self.output_path}/f_{format_id}_{sanitize_filename('%(title)s.%(ext)s')}",
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    filename = ydl.prepare_filename(info_dict)
                    ydl.download(url)
                    return filename
                else:
                    logging.error("Failed to extract video information.")
                    return None
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            return None

    def get_info(self, url: str):
        try:
            yt_dlp_options = {
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    title = info_dict.get("title", "Unknown Title")
                    thumbnail = info_dict.get("thumbnail", None)
                    formats = info_dict.get("formats", [])

                    video_formats = []
                    audio_formats = []

                    allowed_resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]

                    for f in formats:
                        format_note = f.get("format_note", "")
                        vcodec = f.get("vcodec", "")
                        ext = f.get("ext", "")

                        if format_note in allowed_resolutions and "avc1" in vcodec and ext == "mp4":
                            video_formats.append({
                                "format_id": f.get("format_id"),
                                "resolution": format_note,
                                "ext": ext,
                                "filesize": f.get("filesize"),
                                "vcodec": vcodec,
                                "acodec": f.get("acodec"),
                            })

                        if f.get("vcodec") == "none" and f.get("acodec") != "none" and ext == "m4a":
                            audio_formats.append({
                                "format_id": f.get("format_id"),
                                "ext": ext,
                                "filesize": f.get("filesize"),
                                "acodec": f.get("acodec"),
                            })

                    seen_resolutions = set()
                    unique_video_formats = []
                    for video_format in video_formats:
                        if video_format["resolution"] not in seen_resolutions:
                            unique_video_formats.append(video_format)
                            seen_resolutions.add(video_format["resolution"])

                    return title, thumbnail, unique_video_formats, audio_formats
                else:
                    logging.error("Failed to extract video information.")
                    return None, None, None, None
        except Exception as e:
            logging.error(f"Error extracting YouTube video info: {str(e)}")
            return None, None, None, None
