import logging
import os
import yt_dlp
from yt_dlp.utils import sanitize_filename


class YouTubeDownloader:
    """
    A class to handle downloading YouTube videos and extracting video information.

    Attributes:
        output_path (str): The directory where downloaded videos will be saved.
    """

    def __init__(self, output_path: str = "downloads"):
        """
        Initializes the YouTubeDownloader with a specified output path.

        Args:
            output_path (str): The directory where videos will be saved. Defaults to "downloads".
        """
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def download(self, url: str, format_id: str):
        """
        Downloads a YouTube video from the provided URL and format.

        Args:
            url (str): The URL of the YouTube video to download.
            format_id (str): The format ID to specify which video quality and file type to download.

        Returns:
            str: The filename of the downloaded video, or None if the download failed.

        Raises:
            Exception: If there is an error during the download process.
        """
        format_sanitized = format_id.replace('+', '_')
        try:
            yt_dlp_options = {
                "format": str(format_id),
                "outtmpl": f"{self.output_path}/{sanitize_filename(f'f_{format_sanitized}_%(title)s.%(ext)s').replace('+', '_')}",
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    filename = ydl.prepare_filename(info_dict)
                    sanitized_filename = filename.replace('+', '_')

                    ydl.download(url)

                    if sanitized_filename != filename:
                        os.rename(filename, sanitized_filename)

                    return sanitized_filename
                else:
                    logging.error("Failed to extract video information.")
                    return None
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            return None


    def get_info(self, url: str):
        """
        Extracts information about a YouTube video without downloading it.

        Args:
            url (str): The URL of the YouTube video to extract information from.

        Returns:
            tuple: A tuple containing the title, thumbnail URL, a list of unique video formats, and a list of audio formats.
                If extraction fails, returns four None values.

        Raises:
            Exception: If there is an error extracting video information.
        """
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
