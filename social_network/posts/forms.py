from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'maxlength': 1000}),
        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
        }