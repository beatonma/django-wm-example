from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import MentionableExample, TemporaryMention
from mentions.models.webmention import Webmention


class WebmentionInline(GenericTabularInline):
    model = Webmention
    readonly_fields = ['target_url', 'source_url', 'quote', 'hcard', 'sent_by', ]
    can_delete = False


@admin.register(MentionableExample)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        WebmentionInline,
    ]

@admin.register(TemporaryMention)
class TemporaryMentionAdmin(admin.ModelAdmin):
    list_display = ['url', 'submission_time', 'alive']
