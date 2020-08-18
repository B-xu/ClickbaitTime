import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')




def findVideo(id):
    ydl_opts = {
    'format': 'worst',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp4',
        'preferredquality': '160',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    }   

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info('https://www.youtube.com/watch?v='+id, download=False)
        video_url = info_dict.get("url", None)
        return video_url