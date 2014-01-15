from math import sqrt

from django.db.models.query import QuerySet
from django.db import models

from model_utils import Choices
from model_utils.managers import PassThroughManager

from thedevlabsweb.users.models import User

from .stats import wilson_ci_lower_bound

class RankedQuerySet(QuerySet):
    def ranked_for(self, user):
        seen = Score.objects.filter(user=user).values_list('website__pk', flat=True)
        qs = self.exclude(pk__in=seen)
        return sorted(qs, key=lambda w: w.score)


class Website(models.Model):
    url = models.URLField(unique=True)
    objects = PassThroughManager.for_queryset_class(RankedQuerySet)()

    def __unicode__(self):
        return self.url

    @property
    def score(self):
        """Score this website. Only takes into account upvote/downvote"""
        pos = self.scores.filter(value=1).count()
        n = self.scores.count()
        return wilson_ci_lower_bound(n, pos)


class Score(models.Model):
    VALUES = Choices(
        (-1, 'downvote'),
        (1, 'upvote'),
    )

    user = models.ForeignKey(User, related_name='scores')
    website = models.ForeignKey(Website, related_name='scores')
    value = models.SmallIntegerField(choices=VALUES)

    class Meta:
        unique_together = ('user', 'website')
