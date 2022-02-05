from functools import reduce

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

from mentions.models.webmention import (
    Webmention,
    OutgoingWebmentionStatus,
)
from mentions.tasks.outgoing_webmentions import process_outgoing_webmentions
from .models import MentionableExample, TemporaryMention


class MentionableExampleView(View):
    """
    Example of a mentionable page.
    For the purposes of this example we are just returning the mentions with the main request.
    You might prefer to do this via javascript to help the original page load as quickly as
    possible. To do that, make a call to /webmention/get
    """

    def dispatch(self, request, *args, **kwargs):
        article = MentionableExample.objects.get(slug=kwargs.get('slug'))
        mentions_pending_approval = Webmention.objects.filter(approved=False)

        temps = TemporaryMention.objects.all().order_by("url", "submission_time")
        temps = [x for x in temps if x.alive]
        temporary_mentions = []
        if temps:
            temporary_mentions = reduce(
                lambda x, y: x + [y] if x == [] or x[-1].url != y.url else x, temps, []
            )
            temporary_mentions.sort(key=lambda x: x.submission_time)

        return render(
            request,
            "mentionable_example_tester.html",
            {
                'article': article,
                "mentions_pending_approval": mentions_pending_approval,
                "temporary_mentions": temporary_mentions,
            },
        )


class SubmitView(View):
    """
    Allow developers to submit their own URLs.
    These will appear on the main page for a short time to help them
    test their implementation.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, "submit_temporary_mention.html")

        elif request.method == "POST":
            url = request.POST.get("url")
            try:
                URLValidator()(url)
            except ValidationError:
                return HttpResponseBadRequest()

            if url:
                temp = TemporaryMention.objects.create(url=url)
                temp.save()
                process_outgoing_webmentions(
                    "/", f'<html><body><a href="{url}">{url}</a></body></html>'
                )
                status = (
                    OutgoingWebmentionStatus.objects.filter(target_url=url)
                    .order_by("created_at")
                    .first()
                )
                temp.outgoing_status = status
                temp.save()

                return redirect("/")

        return HttpResponseBadRequest()
