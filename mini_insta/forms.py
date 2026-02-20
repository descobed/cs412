# Diego Escobeod Ruiz / task 2 for mini_insta  

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''Creates a new post for'''
    
    image_url = forms.URLField(required=False, label='Image URL')

    class Meta:
        model = Post
        #should inherit the user/pk
        fields = ['caption']