from django import forms
from .models import Profile, Review


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text']


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'tags']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i}/10') for i in range(1, 11)]),
        }
