from django import forms
from .models import Post

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