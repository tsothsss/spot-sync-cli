from src.spotify import SpotifyHandler
from src.youtube import YouTubeAudioEngine
from src.tagger import MetadataTagger

def main():
    # 1. Spotify Metadata
    spotify = SpotifyHandler()
    test_url = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
    
    print("Fetching track metadata from Spotify...")
    track = spotify.get_track_metadata(test_url)
    
    print("-" * 30)
    print(f"Τίτλος:      {track.title}")
    print(f"Καλλιτέχνης: {track.artist}")
    print(f"Άλμπουμ:     {track.album}")
    print(f"Query:       {track.query}")
    print("-" * 30)

    # 2. YouTube Audio Download
    yt_engine = YouTubeAudioEngine(download_dir="downloads")
    file_path = yt_engine.download_audio(track.query)

    # 3. ID3 Metadata & Album Art Injection
    if file_path:
        MetadataTagger.apply_metadata(file_path, track)
        print(f"\n Ολοκληρώθηκε πλήρως: {file_path}")
    else:
        print("\n Η λήψη απέτυχε.")

if __name__ == "__main__":
    main()