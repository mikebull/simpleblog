from django import forms
from blog.models import Post, Comment, Category, Author
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'categories', 'author')
        widgets = {
           'body': TinyMCE(attrs={
                'cols': 80,
                'rows': 20
            },
            mce_attrs={
               'language': 'en',
               'theme': 'advanced'
           })}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description')

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username', 'full_name')