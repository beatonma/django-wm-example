from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from mentions.models.webmention import Webmention
from .models import MentionableExample, TemporaryMention


class MentionableExampleView(View):
    def dispatch(self, request, *args, **kwargs):
        article = MentionableExample.objects.get(slug=kwargs.get('slug'))
        mentions_pending_approval = Webmention.objects.filter(approved=False)
        temporary_mentions = [x for x in TemporaryMention.objects.all() if x.alive]

        return render(
            request,
            'mentionable_example_tester.html',
            {
                'article': article,
                'mentions_pending_approval': mentions_pending_approval,
                'temporary_mentions': temporary_mentions,
            })


class SubmitView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(
                request,
                'submit_temporary_mention.html')

        elif request.method == 'POST':
            url = request.POST.get('url')
            try:
                URLValidator()(url)
            except ValidationError:
                return HttpResponseBadRequest()

            if url:
                TemporaryMention.objects.create(url=url).save()
                return redirect('/')

        return HttpResponseBadRequest()