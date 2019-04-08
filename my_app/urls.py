"""

"""

import logging

from django.urls import path

from .views import MyMentionableArticleView

log = logging.getLogger(__name__)

urlpatterns = [
    # REQUIRED: Add `model_name` with `appname.modelname` to path kwargs!
    path(
        '',
        MyMentionableArticleView.as_view(),
        kwargs={
            'slug': 'webmention-tester',
            'model_name': 'my_app.MyMentionableArticle',
        },
        name='my_mentionable_article')
]
