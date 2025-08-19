# Spotify backup

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A simple command line tool to back up your Spotify playlists.

```text
usage: backup.py [-h] [--client_id CLIENT_ID] [--client_secret CLIENT_SECRET] [--filename FILENAME] playlist

Dumps your spotify playlist into a CSV file.
You may get related credentials here:
https://developer.spotify.com/dashboard/applications

positional arguments:
  playlist              Spotify link or ID of the playlist.

options:
  -h, --help            show this help message and exit
  --client_id CLIENT_ID
                        Specify client id from Spotify. If not specified, looks
                        for 'SPOTIFY_CLIENT_ID' environment variable.
  --client_secret CLIENT_SECRET
                        Specify client secret from Spotify. If not specified,
                        looks for 'SPOTIFY_CLIENT_SECRET' environment variable.
  --filename FILENAME   Specify a filename for the backup. Defaults to playlist
                        name with UTC timestamp.
```

``backup.py`` is [PEP 723](https://peps.python.org/pep-0723/) compliant, so you
can use [uv](https://github.com/astral-sh/uv) to run it without needing to
manage a virtual environment:

```
uv run backup.py
```
