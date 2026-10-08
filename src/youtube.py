import os
from pathlib import Path
from typing import Optional
import yt_dlp


class YouTubeAudioEngine:
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download_audio(self, search_query: str) -> Optional[str]:
        """
        Αναζητά το query στο YouTube, κατεβάζει το καλύτερο audio stream
        και επιστρέφει το path του αρχείου.
        """
        outtmpl_path = str(self.download_dir / "%(title)s.%(ext)s")

        ydl_opts = {
            # Ψάχνει στο YouTube και παίρνει το 1ο αποτέλεσμα
            "default_search": "ytsearch1",
            "format": "bestaudio/best",
            "outtmpl": outtmpl_path,
            "noplaylist": True,
            "quiet": False,
            "no_warnings": True,
            # Μετατροπή σε mp3/m4a αν υπάρχει ffmpeg, αλλιώς κατεβάζει το raw audio format
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"\n[YouTube] Αναζήτηση & Λήψη: {search_query}")
                info = ydl.extract_info(search_query, download=True)
                
                if "entries" in info and info["entries"]:
                    entry = info["entries"][0]
                else:
                    entry = info

                filename = ydl.prepare_filename(entry)
                # Αν μετατράπηκε σε mp3 από ffmpeg
                base, _ = os.path.splitext(filename)
                mp3_filename = f"{base}.mp3"

                return mp3_filename if os.path.exists(mp3_filename) else filename

        except Exception as e:
            # Fallback αν δεν υπάρχει ffmpeg εγκατεστημένο στο σύστημα
            if "ffmpeg" in str(e).lower():
                print("[Προειδοποίηση] Το FFmpeg δεν βρέθηκε, γίνεται λήψη στο native audio format...")
                ydl_opts.pop("postprocessors", None)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_raw:
                    info = ydl_raw.extract_info(search_query, download=True)
                    entry = info["entries"][0] if "entries" in info else info
                    return ydl_raw.prepare_filename(entry)
            else:
                print(f"[Σφάλμα YouTube]: {e}")
                return None