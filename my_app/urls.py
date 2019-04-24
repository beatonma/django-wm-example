"""

"""

import logging

from django.urls import path

from .views import MentionableExampleView, SubmitView

log = logging.getLogger(__name__)

urlpatterns = [
    # REQUIRED: Add `model_name` with `appname.modelname` to path kwargs!
    path(
        '',
        MentionableExampleView.as_view(),
        kwargs={
            'slug': 'webmention-tester',
            'model_name': 'my_app.MentionableExample',
        },
        name='main'),
    path(
        'submit',
        SubmitView.as_view(),
        name='submit'),
    path(
        'mentionable/<str:slug>',
        MentionableExampleView.as_view(),
        kwargs={
            'model_name': 'my_app.MentionableExample',
        },
        name='mentionable_example'),
]
