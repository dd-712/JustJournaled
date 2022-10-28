from tkinter import Widget
from django import forms
from .models import Profile, BlogPost


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'phone_no',
            'bio',
            'facebook',
            'instagram',
            'linkedin',
            'image',
        )
        widgets = {
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image')
        widgets = {
            'title':
            forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of the Blog'
            }),
            'slug':
            forms.TextInput(
                attrs={
                    'class':
                    'form-control',
                    'placeholder':
                    'Copy the title with no space and a hyphen in between'
                }),
            'content':
            forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Content of the Blog'
            }),
        }