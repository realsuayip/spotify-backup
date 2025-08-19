# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///

import argparse
import base64
import csv
import os
import time
from urllib.parse import urlparse

import requests

BASE_URL = "https://api.spotify.com/v1/"
PLAYLIST_URL = BASE_URL + "playlists/%(id)s/"
TRACKS_URL = PLAYLIST_URL + (
    "tracks?fields="
    "next,items(added_at,track(name,duration_ms,artists.name,album.name)"
)


def _get_authenticated_session(client_id, client_secret):
    token = client_id + ":" + client_secret
    token = base64.b64encode(token.encode("utf-8"))
    token = "Basic %s" % token.decode("utf-8")

    session = requests.Session()
    session.headers = {"Authorization": token}

    response = session.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
    )
    assert response.status_code == 200, "Check your credentials"
    content = response.json()
    authorization = "%s %s" % (
        content["token_type"],
        content["access_token"],
    )
    session.headers = {"Authorization": authorization}
    return session


def _parse_item(item):
    track = item["track"]
    name = track["name"]
    added_at = item["added_at"]
    album = track["album"]["name"]
    artists = ", ".join(artist["name"] for artist in track["artists"]).strip()
    duration = track["duration_ms"]
    return name, artists, album, duration, added_at


def _parse_playlist(playlist):
    if "spotify" not in playlist:
        return playlist
    return urlparse(playlist).path.split("/")[-1]


def pull(client_id, client_secret, playlist_id, filename=None):
    session = _get_authenticated_session(client_id, client_secret)
    response = session.get(PLAYLIST_URL % {"id": playlist_id})
    assert response.status_code == 200, "Invalid playlist specified"

    playlist = response.json()
    filename = filename or "%s_%d" % (playlist["name"], time.time())
    csvfile = open("%s.csv" % filename, "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(("name", "artists", "album", "duration", "added_at"))

    tracks = session.get(TRACKS_URL % {"id": playlist_id}).json()

    while True:
        for item in tracks["items"]:
            writer.writerow(_parse_item(item))

        if not tracks["next"]:
            break

        tracks = session.get(tracks["next"]).json()

    csvfile.close()
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dumps your spotify playlist into a CSV file."
        " You may get related credentials here:"
        " https://developer.spotify.com/dashboard/applications"
    )
    parser.add_argument(
        "playlist",
        type=str,
        help="Spotify link or ID of the playlist.",
    )
    parser.add_argument(
        "--client_id",
        type=str,
        help="Specify client id from Spotify."
        " If not specified, looks for 'SPOTIFY_CLIENT_ID'"
        " environment variable.",
    )
    parser.add_argument(
        "--client_secret",
        type=str,
        help="Specify client secret from Spotify."
        " If not specified, looks for 'SPOTIFY_CLIENT_SECRET'"
        " environment variable.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Specify a filename for the backup."
        " Defaults to playlist name with UTC timestamp.",
    )
    args = parser.parse_args()

    _client_id = args.client_id or os.environ["SPOTIFY_CLIENT_ID"]
    _client_secret = args.client_secret or os.environ["SPOTIFY_CLIENT_SECRET"]
    _playlist_id = _parse_playlist(args.playlist)
    pull(_client_id, _client_secret, _playlist_id, args.filename)
