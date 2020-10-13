from django.contrib import admin
from .models import Category, Author, Post, Comment, PostView
from .forms import PostAdmin

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostView)
