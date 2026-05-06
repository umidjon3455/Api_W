from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'likes_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'likes_count')
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content_preview', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'author__email', 'post__title')
    readonly_fields = ('created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('user__email', 'post__title')
    readonly_fields = ('created_at',)
