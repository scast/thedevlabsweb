from django.shortcuts import render
from django.conf import settings

from vanilla import FormView
from braces.views import LoginRequiredMixin, JSONResponseMixin
from twython import Twython

from .forms import TwitterSearchForm, URLForm
from .models import Website


class TwitterSearchView(LoginRequiredMixin, JSONResponseMixin, FormView):
    form_class = TwitterSearchForm
    require_json = True

    def form_valid(self, form):
        query = form.cleaned_data['q']
        twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
        results = twitter.search(q=query)
        return self.render_json_response([
            {
                'screen_name': result['user']['screen_name'],
                'text': result['text']
            }
            for result in results['statuses']
        ])

class URLAddView(LoginRequiredMixin, JSONResponseMixin, FormView):
    form_class = URLForm
    require_json = True

    def form_invalid(self, *args, **kwargs):
        return self.render_jsoin_response({
            'status': 'invalid'
        })

    def form_valid(self, form):
        website, _ = Website.objects.get_or_create(url=form.cleaned_data['url'])
        return self.render_json_response(website.serialized)
