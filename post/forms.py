from django import forms
from post.models import Post


class PostForm(forms.ModelForm):
    picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        'class': 'file-input',
        'type': 'file',
        'name': 'resume'
    }))
    caption = forms.CharField(max_length=1500, widget=forms.Textarea(attrs={
        'class': 'input',
        'type': 'text',
        'placeholder': 'Caption'
    }), required=True)
    tags = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'text',
        'placeholder': 'Add tags separate by commas'
    }), required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption', 'tags')
