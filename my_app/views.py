from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from .models import MyMentionableArticle


class MyMentionableArticleView(View):
    def dispatch(self, request, *args, **kwargs):
        article = MyMentionableArticle.objects.get(slug=kwargs.get('slug'))
        return render(
            request,
            'my_mentionable_article.html',
            {
                'article': article,
            })
