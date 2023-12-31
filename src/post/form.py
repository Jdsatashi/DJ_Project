from django import forms
from .models import PostModel


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'content', 'author']
