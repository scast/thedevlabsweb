from django.shortcuts import render
from django.conf import settings

from vanilla import FormView
from braces.views import LoginRequiredMixin, JSONResponseMixin
from twython import Twython

from .forms import TwitterSearchForm


class TwitterSearchView(LoginRequiredMixin, JSONResponseMixin, FormView):
    form_class = TwitterSearchForm
    require_json = True
    # template_name = 'search.html'
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
