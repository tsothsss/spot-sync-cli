import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

@dataclass
class TrackMetadata:
    title: str
    artist: str
    album: str
    release_date: str
    track_number: int
    cover_art_url: Optional[str]
    isrc: Optional[str]

    @property
    def query(self) -> str:
        """Query format βελτιστοποιημένο για audio search."""
        return f"{self.artist} - {self.title} Audio"

class SpotifyHandler:
    def __init__(self):
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Λείπουν τα SPOTIPY_CLIENT_ID ή SPOTIPY_CLIENT_SECRET από το .env")

        auth_manager = SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def extract_track_id(self, url_or_id: str) -> str:
        """Εξαγωγή του καθαρού Spotify ID από URL."""
        if "spotify.com/track/" in url_or_id:
            # Χωρίζει το URL και αφαιρεί τυχόν URL queries (π.χ. ?si=...)
            clean_part = url_or_id.split("track/")[1]
            return clean_part.split("?")[0]
        return url_or_id

    def get_track_metadata(self, track_url: str) -> TrackMetadata:
        track_id = self.extract_track_id(track_url)
        data = self.sp.track(track_id)

        artists = ", ".join([a["name"] for a in data["artists"]])
        cover_url = data["album"]["images"][0]["url"] if data["album"]["images"] else None
        isrc = data.get("external_ids", {}).get("isrc")

        return TrackMetadata(
            title=data["name"],
            artist=artists,
            album=data["album"]["name"],
            release_date=data["album"]["release_date"],
            track_number=data["track_number"],
            cover_art_url=cover_url,
            isrc=isrc,
        )