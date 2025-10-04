import os
import requests

def daily_lesson_audio_dl(lesson_dir):
    """
    Download daily lesson audio files based on the last Saturday.
    """
    from datetime import datetime, timedelta

    today = datetime.today()
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)

    for i in range(7):  # 7 daily lessons
        download_date = last_saturday + timedelta(days=i)
        formatted_date = download_date.strftime('%Y-%m-%d')
        url = f"https://d7dlhz1yjc01y.cloudfront.net/audio/en/lessons/{formatted_date}.mp3"

        dest_path = os.path.join(lesson_dir, f"{formatted_date}.mp3")

        try:
            head_response = requests.head(url, timeout=10)
            if head_response.status_code == 200:
                if os.path.exists(dest_path):
                    print(f"File {dest_path} already exists. Skipping download.")
                    return

                try:
                    print(f"⬇️ Downloading {url}")
                    response = requests.get(url, stream=True, timeout=10)
                    response.raise_for_status()
                    with open(dest_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    print(f"✅ Downloaded: {dest_path}")
                except Exception as e:
                    print(f"⚠️ Error downloading {url}: {e}")
            else:
                print(f"⚠️ File not found for {formatted_date}. Skipping.")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error checking availability for {url}: {e}")
