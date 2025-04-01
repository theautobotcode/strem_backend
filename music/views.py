import os
import subprocess
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import Music as Song
import json

def convert_to_hls(song_path, song_id):
    output_dir = os.path.join(settings.BASE_DIR, "assets/hls", str(song_id))
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "ffmpeg", "-i", song_path,
        "-hls_time", "10",  # Each segment is 10 seconds
        "-hls_playlist_type", "vod",
        f"{output_dir}/playlist.m3u8"
    ]
    subprocess.run(cmd, check=True)

    return f"assets/hls/{song_id}/playlist.m3u8"

@csrf_exempt
def upload_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        file = request.FILES.get('file')

        if not (title and artist and file):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        song_path = default_storage.save(f'assets/songs/{file.name}', file)
        full_path = os.path.join(settings.BASE_DIR, song_path)

        # Create song entry
        song = Song(title=title, artist=artist, file=song_path)
        song.save()

        # Convert to HLS
        hls_path = convert_to_hls(full_path, song.id)
        song.hls_playlist = hls_path
        song.save()

        return JsonResponse({'id': song.id, 'title': song.title, 'artist': song.artist, 'hls_playlist': song.hls_playlist}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_songs(request):
    songs = list(Song.objects.values('id', 'title', 'artist', 'hls_playlist'))
    return JsonResponse({'songs': songs})
