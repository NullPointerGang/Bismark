import logging
import os
import yt_dlp
from yt_dlp.utils import sanitize_filename


class YouTubeDownloader:
    def __init__(self, output_path: str = "downloads"):
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)
        self.yt_dlp_video_options = {
                "format": "bv*[filesize < 50M][ext=mp4][vcodec^=avc1] + ba[ext=m4a]",
                "outtmpl": f"{self.output_path}/{sanitize_filename('%(title)s').replace(' ', '')}",
                'noplaylist': True,
            }
        
        self.yt_dlp_audio_options = {
                "format": "m4a/bestaudio/best",
                "outtmpl": f"{self.output_path}/{sanitize_filename('%(title)s').replace(' ', '')}",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                    }
                ],
                'noplaylist': True,
            }

    def download(self, url: str, format: str):
        try:
            if format == "mp4":
                return self._download_video(url)
            elif format == "mp3":
                return self._download_audio(url)
            else:
                logging.error(f"Unsupported format: {format}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None

    def _download_video(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_video_options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    filename = ydl.prepare_filename(info_dict) + ".mp4"
                    title = info_dict.get("title", "Unknown Title")
                    thumbnail = info_dict.get("thumbnail", None)

                    ydl.download(url)
                    return os.path.abspath(filename), title, thumbnail
                else:
                    logging.error("Failed to extract video information.")
                    return None
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            return None
        
    def _download_audio(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_audio_options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    filename = ydl.prepare_filename(info_dict) + ".mp3"
                    title = info_dict.get("title", "Unknown Title")
                    thumbnail = info_dict.get("thumbnail", None)

                    ydl.download(url)
                    return os.path.abspath(filename), title, thumbnail
                else:
                    logging.error("Failed to extract video information.")
                    return None, None, None
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            return None