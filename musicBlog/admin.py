from django.contrib import admin

# Register your models here.

from .models import Album, Artist, Friend, Profile, Review, Song

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Friend)