
from django.contrib import admin

# Register your models here.
from .models import Follow, Photo, Post, Profile, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)