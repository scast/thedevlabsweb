# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

# from thedevlabsweb.recommender.math import website_relevance


# Subclass AbstractUser
class User(AbstractUser):

    def __unicode__(self):
        return self.username
