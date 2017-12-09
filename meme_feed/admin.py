from django.contrib import admin
from meme_feed.models import Author, GroupPost

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupPost)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'author', 'created', 'message', 'reaction_count', 'date_discovered', 'date_updated')
    readonly_fields = ('image_tag', 'date_discovered', 'date_updated')
