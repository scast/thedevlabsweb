from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST


from vanilla import FormView, GenericView
from braces.views import LoginRequiredMixin, JSONResponseMixin
from twython import Twython

from .forms import TwitterSearchForm, URLForm
from .models import Website, Score


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

class URLGetView(LoginRequiredMixin, JSONResponseMixin, GenericView):
    def post(self, request, *args, **kwargs):
        user = request.user
        possible = Website.objects.ranked_for(user)
        if possible:
            return self.render_json_response(possible[0].serialized)
        return self.render_json_response({'status': 'done'})

class VoteMixin(object):
    def vote(self, request, pk, value):
        website = Website.objects.get(pk=pk)
        score,_ = Score.objects.get_or_create(user=request.user, website=website,
                                            defaults={'value': value})
        score.score = value
        score.save()
        return {'status': 'ok', 'pk': score.pk}

class URLUpvoteView(LoginRequiredMixin, JSONResponseMixin,
                    VoteMixin, GenericView):
    def post(self, request, *args, **kwargs):
        return self.render_json_response(self.vote(request, kwargs['id'], 1))

class URLDownvoteView(LoginRequiredMixin, JSONResponseMixin,
                    VoteMixin, GenericView):
    def post(self, request, *args, **kwargs):
        return self.render_json_response(self.vote(request, kwargs['id'], -1))
