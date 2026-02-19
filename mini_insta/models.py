from django.db import models
#Diego Escobedo Ruiz/ mini_insta model for CS412



# Create your models here.

class Profile(models.Model):
    '''Model for a mini_insta profile'''

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True) 


    def __str__(self):
        '''returns a string of the user'''
        return f'{self.username}'
    
    def get_all_posts(self):
        '''returns a list of all posts by this user'''
        posts = Post.objects.filter(profile=self)
        return posts

class Post(models.Model):
    '''Model for a mini_insta post'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the post'''
        return f'Post by {self.caption}'
    

    def get_all_photos(self):
        '''returns a list of all photos in this post'''
        photos = Photo.objects.filter(post=self)
        return photos

class Photo(models.Model):
    '''Model for a mini_insta photo'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the photo'''
        return f'Photo url: {self.image_url}'