from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import MyMentionableArticle
from mentions.models.webmention import Webmention

class WebmentionInline(GenericTabularInline):
    model = Webmention
    readonly_fields = ['target_url', 'source_url', 'quote', 'hcard', 'sent_by', ]
    can_delete = False

@admin.register(MyMentionableArticle)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        WebmentionInline,
    ]
