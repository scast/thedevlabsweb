from django.shortcuts import render
from django.conf import settings

from vanilla import FormView
from braces.views import LoginRequiredMixin
from twython import Twython

from .forms import TwitterSearchForm


class TwitterSearchView(FormView, LoginRequiredMixin):
    form_class = TwitterSearchForm
    template_name = 'search.html'
    def form_valid(self, form):
        query = form.cleaned_data['q']
        twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
        results = twitter.search(q=query)
        context = self.get_context_data(results=results['statuses'], form=form)
        return self.render_to_response(context)
