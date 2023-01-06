from django.contrib import admin
from .models import Post, Comments
from django.contrib.auth.models import User


class CommentsInlineModelAdmin(admin.TabularInline):
    model = Comments
    fk_name = 'post'


# class PostInlineModelAdmin(admin.TabularInline):
#     model = Post
#
#
# class UserInlineModelAdmin(admin.TabularInline):
#     model = User


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['owner', 'text', 'published']
    list_filter = ['published']
    list_per_page = 20
    fields = ['owner', 'post', 'text', 'published']
    search_fields = ['owner']
    # inlines = [PostInlineModelAdmin]
    save_as = True


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'text', 'published']
    list_filter = ['published']
    search_fields = ['owner']
    date_hierarchy = 'created_date'
    list_per_page = 20
    fieldsets = (
        ('Post info', {
            'fields': ('title', 'text', 'created_date', 'published')
        }),
        ('User', {
            'fields': ('owner',)
         }),
    )
    inlines = [CommentsInlineModelAdmin]
    save_as = True


admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
