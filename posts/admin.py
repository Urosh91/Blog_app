from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):

    list_display = ['title', 'created_at', 'updated']

    list_display_links = ['updated',]

    list_filter = ['created_at', 'updated']

    search_fields = ['title', 'created_at']

    list_editable = ['title']

admin.site.register(Post, PostAdmin)
