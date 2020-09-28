from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': "Type your comment",
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content',)



