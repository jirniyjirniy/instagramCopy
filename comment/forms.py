from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=1500, widget=forms.Textarea(attrs={
        'class': 'textarea',
        'placeholder': 'Add a comment...',
        'rows': '3',
    }), required=True)

    class Meta:
        model = Comment
        fields = ('comment',)