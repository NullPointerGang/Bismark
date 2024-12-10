import logging
import os
import yt_dlp
from yt_dlp.utils import sanitize_filename


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

                    formats_sorted = sorted(
                        formats,
                        key=lambda f: (f.get("height") or 0, f.get("filesize") or 0),
                        reverse=True
                    )
                    
                    max_quality = next((f for f in formats_sorted if f.get("vcodec") != "none" and f.get("acodec") != "none"), None)
                    video_only = next((f for f in formats_sorted if f.get("vcodec") != "none" and f.get("acodec") == "none"), None)
                    audio_only = next((f for f in formats_sorted if f.get("vcodec") == "none" and f.get("acodec") != "none"), None)

                    quality_list = {
                        "max_quality": max_quality,
                        "video_only": video_only,
                        "audio_only": audio_only,
                    }
                    
                    return title, thumbnail, quality_list
                else:
                    logging.error("Failed to extract video information.")
                    return None, None, None
        except Exception as e:
            logging.error(f"Error extracting YouTube video info: {str(e)}")
            return None, None, None
