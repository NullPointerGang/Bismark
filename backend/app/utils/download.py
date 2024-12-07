from yt_dlp import YoutubeDL


class DownloadYouTube:
    def __init__(self) -> None:
        pass

    
    def download(self, url: str, format_type: str):
        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        elif format_type == 'mp4':
            ydl_opts = {
                'format': 'bestvideo/best',
            }
        else:
            return None

        with YoutubeDL(ydl_opts) as ydl:
            info_dict: dict | None = ydl.extract_info(url, download=False)
            if info_dict:
                stream_url: dict = info_dict['url']
                return stream_url
            else:
                return None