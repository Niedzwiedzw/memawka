from django.contrib import admin
from meme_feed.models import Author, GroupPost

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupPost)
class AuthorAdmin(admin.ModelAdmin):
    pass
