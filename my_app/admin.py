from django.contrib import admin

from .models import MyMentionableArticle


@admin.register(MyMentionableArticle)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
