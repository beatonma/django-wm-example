from django.db import models
from django.urls import reverse

from mentions.models.mixins.mentionable import MentionableMixin


class MyMentionableArticle(MentionableMixin, models.Model):
    title = models.CharField(max_length=48)
    slug = models.SlugField(max_length=48)

    main_content = models.TextField()
    summary = models.TextField()

    def all_text(self) -> str:
        # We want to find potential outgoing webmention URLs
        # in both `summary` and `main_content fields.
        return f'{self.main_content} {self.summary}'

    def get_absolute_url(self):
        return reverse('my_mentionable_article', args=[self.slug])
