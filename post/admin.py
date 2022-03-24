from django.contrib import admin
from post.models import *


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 5
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]

