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