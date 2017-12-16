from django.contrib import admin
from meme_feed.models import Author, GroupPost, FacebookGroup, GroupPostComment

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(GroupPost)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'author', 'created', 'message', 'reaction_count', 'date_discovered', 'date_updated')
    readonly_fields = ('image_tag', 'date_discovered', 'date_updated')


@admin.register(FacebookGroup)
class FacebookGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'group_id', '_facebook_auth_key', 'deep_scanned', '_minimal_quality_factor')
    readonly_fields = ('_criteria_last_updated', '_criteria_last_value')

