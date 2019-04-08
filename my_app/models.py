from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse

from mentions.models.mixins.mentionable import MentionableMixin
from mentions.models.webmention import Webmention

TEMPORARY_WEBMENTION_TIMEOUT = 60 * 15


class MyMentionableArticle(MentionableMixin, models.Model):
    title = models.CharField(max_length=48)
    slug = models.SlugField(max_length=48)

    summary = models.TextField()
    main_content = models.TextField()

    def all_text(self) -> str:
        # We want to find potential outgoing webmention URLs
        # in both `summary` and `main_content fields.
        return f'{self.main_content} {self.summary}'

    def get_absolute_url(self):
        return reverse('my_mentionable_article', args=[self.slug])

    def __str__(self):
        return f'{self.title}'


class TemporaryMention(models.Model):
    url = models.URLField()
    submission_time = models.DateTimeField(auto_now_add=True)

    @property
    def alive(self):
        return datetime.now() - timedelta(seconds=TEMPORARY_WEBMENTION_TIMEOUT)
