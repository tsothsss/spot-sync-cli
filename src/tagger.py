from pathlib import Path
import urllib.request
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from src.spotify import TrackMetadata


class MetadataTagger:
    @staticmethod
    def apply_metadata(file_path: str, metadata: TrackMetadata):
        """
        Ενσωματώνει ID3 tags και εξώφυλλο στο .mp3 αρχείο.
        """
        path = Path(file_path)
        if not path.exists() or path.suffix.lower() != ".mp3":
            print(f"[Tagger Skip] Το αρχείο δεν είναι mp3: {file_path}")
            return

        # 1. Κειμενικά tags (Title, Artist, Album κτλ.)
        try:
            audio = EasyID3(file_path)
        except Exception:
            audio = MP3(file_path)
            audio.add_tags()
            audio = EasyID3(file_path)

        audio["title"] = metadata.title
        audio["artist"] = metadata.artist
        audio["album"] = metadata.album
        audio["tracknumber"] = str(metadata.track_number)
        audio["date"] = metadata.release_date
        audio.save()

        # 2. Ενσωμάτωση εξωφύλλου (Cover Art)
        if metadata.cover_art_url:
            try:
                req = urllib.request.Request(
                    metadata.cover_art_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                cover_data = urllib.request.urlopen(req).read()

                audio_id3 = ID3(file_path)
                audio_id3.add(
                    APIC(
                        encoding=3,       # UTF-8
                        mime="image/jpeg",
                        type=3,           # Front cover
                        desc="Cover",
                        data=cover_data
                    )
                )
                audio_id3.save(v2_version=3)
                print(f"[Tagger] Προστέθηκαν ID3 tags & Album Cover στο {path.name}")
            except Exception as e:
                print(f"[Tagger Warning] Δεν ήταν δυνατή η προσθήκη εξωφύλλου: {e}")