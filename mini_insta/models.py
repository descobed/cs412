from django.db import models
from django.urls import reverse
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

    def get_absolute_url(self):
        '''returns the profile detail url'''
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_followers(self):
        '''NEW returns a list of all followers of this profile'''
        followers = Follow.objects.filter(profile=self)
        return followers
    
    def get_num_followers(self):
        '''NEW returns number of followers'''
        num = Follow.objects.filter(profile=self).count()
        return num

    def get_following(self):
        '''NEW returns a list of all profiles this profile is following'''
        following = Follow.objects.filter(follower_profile=self)
        return following
    
    def get_num_following(self):
        '''NEW returns number of profiles this profile is following'''
        num = Follow.objects.filter(follower_profile=self).count()
        return num

    def get_post_feed(self):
        '''NEW Feed showing all posts by followed profiles'''
        following_profiles = Follow.objects.filter(
            follower_profile=self
        ).values_list('profile', flat=True)
        post_feed = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return post_feed

class Post(models.Model):
    '''Model for a mini_insta post'''
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the post'''
        return f'Post by {self.caption}'
    
    def get_all_photos(self):
        '''returns all photos, for single post pages'''
        photos = Photo.objects.filter(post=self)
        return photos

    def get_first_photo(self):
        '''NEW returns the first photo for this post, if any'''
        return Photo.objects.filter(post=self).first()

    def get_all_comments(self):
        '''NEW returns all comments for this post'''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_all_likes(self):
        '''NEW returns all likes for this post'''
        likes = Like.objects.filter(post=self)
        return likes
    
    def get_num_likes(self):
        '''NEW returns the number of likes for this post'''
        num = Like.objects.filter(post=self).count()
        return num

class Photo(models.Model):
    '''Model for a mini_insta photo'''

    #If the parent post is deleted, delete this also
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #the url
    image_url = models.URLField(blank=True)
    #image file
    image_file = models.ImageField(blank=True)
    #timestamp!
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the photo'''
        return f'Photo url: {self.image_url}'
    
    def get_image_url(self):
        '''returns the url of the photo'''
        if self.image_file:
            return self.image_file.url
        if self.image_url:
            return self.image_url
        return None
            

class Follow(models.Model):
    '''NEW relationship between following and being followed'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the follow relationship'''
        return f'{self.follower_profile} follows {self.profile}'
    
class Comment(models.Model):
    '''NEW comments relating a profile to a post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''returns a string of the comment'''
        return f'commenter: {self.profile} post: {self.post}'
    

class Like(models.Model):
    '''NEW Likes on posts!'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''returns a string of the like'''
        return f'{self.profile} likes {self.post}'