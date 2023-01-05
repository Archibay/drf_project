from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'published')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('username', 'text')


class ContactUsForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
