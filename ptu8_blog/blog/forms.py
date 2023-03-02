from django import forms
from . import models


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('post', 'commenter', 'text')
        widgets = {'post': forms.HiddenInput(), 'commenter': forms.HiddenInput(), 'text':forms.Textarea(attrs={'rows':5})}