import os
import yt_dlp

def download_video(url, format_code, lesson_dir, lesson):
    """
    Download the specified YouTube video using yt-dlp.
    Saves into ~/Downloads/Lesson_{lesson_number}/
    """
    archive_file = os.path.join(lesson_dir, f'downloaded_videos_lesson_{lesson}.txt')

    ydl_opts = {
        'format': format_code,
        'outtmpl': os.path.join(lesson_dir, '%(title)s.%(ext)s'),
        'download_archive': archive_file,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"⬇️ Downloading: {url} in format: {format_code}")
            ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            print(f"⚠️ Download failed for {url}: {e}")


def search_yt_and_dl(channels, lesson_dir, year, quarter, lesson, format_code="bv[vcodec^=avc1][height<=360]+ba[acodec^=mp4a]"):
    """
    For each channel, searches the latest 10 videos for a custom key phrase.
    Each channel can specify whether to match 'exact' or 'flexible' (unordered words).
    If a video matches, it will be downloaded with `download_video(url, format_code)`.
    
    channels = {
        "channel_url": {
            "template": "string with {lesson}, {quarter}, {year}",
            "match": "exact" | "flexible"
        }
    }
    """
    # Get Sabbath School info

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'playlistend': 10,  # only latest 10 videos
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url, config in channels.items():
            template = config.get("template")
            match_mode = config.get("match", "exact")  # default to exact
            phrase = template.format(lesson=lesson, quarter=quarter, year=year)

            print(f"\n📺 Channel: {channel_url}")
            print(f"   Searching for: '{phrase}' (mode: {match_mode})")

            try:
                info = ydl.extract_info(channel_url, download=False)
                videos = info.get('entries', [])
            except Exception as e:
                print(f"   ⚠️ Error fetching channel: {e}")
                continue

            matches = []
            for video in videos:
                title = video.get("title", "")
                video_id = video.get("id")
                url = f"https://www.youtube.com/watch?v={video_id}"

                if match_mode == "exact":
                    if phrase.lower() in title.lower():
                        matches.append((title, url))
                elif match_mode == "flexible":
                    words = phrase.lower().split()
                    if all(word in title.lower() for word in words):
                        matches.append((title, url))

            if matches:
                print(f"   ✅ Found {len(matches)} matches:")
                for idx, (title, url) in enumerate(matches, 1):
                    print(f"      {idx}. {title}")
                    print(f"         {url}")

                    # Download video
                    try:
                        print(f"      ⬇️ Downloading {title} ...")
                        download_video(url, format_code, lesson_dir, lesson)
                    except Exception as e:
                        print(f"      ⚠️ Error downloading {title}: {e}")
            else:
                print("   ❌ No matches found in latest 10 videos.")
