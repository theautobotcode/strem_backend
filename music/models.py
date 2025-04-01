from django.db import models


class Music(models.Model):
    """
    Music class to refer music table that will contains 
    music files details
    """
    
    title = models.CharField(max_length=256)
    artist = models.CharField(max_length=256, null=True, blank=True)
    tags = models.CharField(max_length=256, null=True, blank=True)
    file = models.FileField(upload_to="assets/songs/")
    hls_playlist = models.CharField(max_length=500, blank=True)
    album_thumbnail = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "music"
