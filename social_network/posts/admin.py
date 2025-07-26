from django.contrib import admin
from .models import Post, Like, Comment


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    raw_id_fields = ('user',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    raw_id_fields = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text_short', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')
    raw_id_fields = ('author',)
    inlines = [LikeInline, CommentInline]

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Text'

    def likes_count(self, obj):
        return obj.likes_count

    likes_count.short_description = 'Likes'

    def comments_count(self, obj):
        return obj.comments_count

    comments_count.short_description = 'Comments'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_short', 'text_short', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text', 'user__username')
    raw_id_fields = ('user', 'post')

    def post_short(self, obj):
        return obj.post.text[:30] + '...' if len(obj.post.text) > 30 else obj.post.text

    post_short.short_description = 'Post'

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Text'


