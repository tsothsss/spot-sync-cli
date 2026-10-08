# spot-sync-cli
Spot Sync CLI — Find it. Match it. Sync it.  A fast, terminal-first music utility that takes a Spotify track, identifies the song, and seamlessly fetches a matching audio file. Built for speed, simplicity, and automation, with a clean CLI workflow that gets you from track link to local file in seconds.  One command. One track. Zero hassle.

These are the following commands:
1. BASIC USAGE (Default Output Folder: downloads/)
--------------------------------------------------
Download via standard Spotify Track URL:
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"

Download via Spotify URL containing tracking query parameters (?si=...):
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=abc123xyz"

Download directly using Spotify Track ID (without full URL):
python main.py "4cOdK2wGLETKBW3PvgPWqT"


2. CUSTOM OUTPUT DIRECTORY (Flag: -o or --output)
-------------------------------------------------
Download to a relative project subfolder:
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT" --output "my_music"

Download to a relative subfolder using the short flag -o:
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT" -o "my_music"

Download to an absolute Windows path (Desktop):
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT" --output "C:\Users\dimit\Desktop\Music"

Download to a directory path that contains spaces (always wrap in quotes):
python main.py "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT" -o "C:\My Downloaded Songs"


3. HELP & DOCUMENTATION FLAGS
-----------------------------
Display the full CLI help menu and argument specifications:
python main.py --help

Display the brief help menu:
python main.py -h


4. CLI ARGUMENTS REFERENCE TABLE
--------------------------------
Argument / Flag   | Type       | Required | Default   | Description
------------------|------------|----------|-----------|---------------------------------------------
url               | Positional | Yes      | None      | Spotify track link or 22-char Spotify ID
-o, --output      | Option     | No       | downloads | Target directory path for audio & MP3 files
-h, --help        | Option     | No       | None      | Print help information and exit
