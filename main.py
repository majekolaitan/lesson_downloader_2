from utils import get_sabbath_school_info, cleanup_old_lessons, get_lesson_folder
from search_yt_and_dl import search_yt_and_dl
from daily_lesson_audio_dl import daily_lesson_audio_dl

channels = {
        "https://www.youtube.com/@hopeSabbathSchool/videos": {
            "template": "Lesson {lesson}:",
            "match": "exact",
        },
        "https://www.youtube.com/@3ABNSabbathSchoolPanelOfficial/videos": {
            "template": "Lesson {lesson} Q{quarter} {year}",
            "match": "exact",
        },
        "https://www.youtube.com/c/Cl%C3%A1udioCarneiro/videos": {
            "template": "{year} Q{quarter} Lesson {lesson} –",
            "match": "exact",
        },
        "https://www.youtube.com/@itiswritten/videos": {
            "template": "{year} Q{quarter} Lesson {lesson}: ",
            "match": "exact",
        },
        "https://www.youtube.com/@SecretsUnsealedMinistry/videos": {
            "template": "Lesson {lesson}: ",
            "match": "exact",
        },
    }

year, quarter, lesson = get_sabbath_school_info()
lesson_dir = get_lesson_folder(lesson)
format_code = "bv[vcodec^=avc1][height<=720]+ba[acodec^=mp4a]"

if __name__ == "__main__":

    # cleanup_old_lessons(lesson)
    search_yt_and_dl(channels, lesson_dir, year, quarter, lesson, format_code)
    daily_lesson_audio_dl(lesson_dir)