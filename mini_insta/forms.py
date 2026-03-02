# Diego Escobeod Ruiz / task 2 for mini_insta  

from django import forms
from .models import *

class UpdateProfileForm(forms.ModelForm):
    '''Form for updating a profile'''
    
    class Meta:
        model = Profile
        #Doesn't include the username or join date since they shouldnt be changed
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''Form for updating a post'''
    
    class Meta:
        model = Post
        fields = ['caption']

class DeletePostForm(forms.ModelForm):
    '''Form for deleting a post'''
    
    class Meta:
        model = Post
        fields = []  #nothing to update :(


class CreatePostForm(forms.ModelForm):
    '''Creates a new post for'''
    
    image_files = forms.ImageField(required=False, label='Upload Image')

    class Meta:
        model = Post
        #should inherit the user/pk
        fields = ['caption']