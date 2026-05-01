from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# Users have reveiws for albums
# Create recommendations based on friends reviews

# Artists have pages/ albums / songs / tags based on album reviews

# Think I will end up using spotify api, but also want to look at others

# artist / albums / songs 
class Artist(models.Model):
    '''Model for an artist'''

    name = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    tags = models.TextField(blank=True) # might change away from text

    def __str__(self):
        '''returns a string of the artist'''
        return f'{self.name}'

    def get_albums(self):
        '''returns a list of all albums by this artist'''
        albums = Album.objects.filter(artist=self)
        return albums
    

class Album(models.Model):
    '''Model for an album / under an artist'''

    title = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    genre = models.TextField(blank=True)
    cover_image_url = models.TextField(blank=True, null=True) # Had too much trouble getting photos from Discogs :(
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        '''returns a string of the album'''
        return f'{self.title} by {self.artist.name}'
    
    def get_artist(self):
        '''returns the artist of the album'''
        return self.artist
    
    def get_songs(self):
        '''returns a list of all songs in this album'''
        songs = Song.objects.filter(album=self)
        return songs
    
    def get_reviews(self):
        '''returns a list of all reviews of this album'''
        reviews = Review.objects.filter(album=self)
        return reviews
    

class Song(models.Model):
    '''Model for a song / under an album'''

    title = models.TextField(blank=True)
    length = models.IntegerField(blank=True, null=True) # in seconds
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        '''returns a string of the song'''
        return f'{self.title} from {self.album.title}'
    
    def get_album(self):
        '''returns the album of the song'''
        return self.album


# profile / reviews / friends / followers 

class Profile(models.Model):
    '''Model for a profile'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='musicblog_profile')
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)

    def __str__(self):
        '''returns a string of the profile'''
        return f'{self.username}'

    def get_friends(self):
        '''returns a list of all profiles this profile has friended'''
        return Friend.objects.filter(profile=self)

    def get_friend_count(self):
        '''returns the number of friend relationships for this profile'''
        return Friend.objects.filter(profile=self).count()


class Friend(models.Model):
    '''Relationship between two music blog profiles'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendships')
    friend_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friended_by')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'friend_profile'], name='unique_musicblog_friendship'),
        ]

    def __str__(self):
        '''returns a string of the friendship relationship'''
        return f'{self.profile} is friends with {self.friend_profile}'
    

class Review(models.Model):
    '''Model for a review'''

    rating = models.IntegerField(blank=True, null=True)
    review_text = models.TextField(blank=True)
    tags = models.TextField(blank=True) # might change 
    created_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        '''returns a string of the review'''
        return f'Review of {self.album.title} with rating {self.rating}'
    
    def get_album(self):
        '''returns the album of the review'''
        return self.album