from collections import defaultdict
from .stats import to_vector, pearson_correlation
from .models import Website, Score

def website_relevance(user, scores, users): #, k=10):
    """Calculate relevant websites for user.
    `user` is a User object
    `scores` is a set of scores by user
    `users` list of users excluding `user`
    """
    # bias = random.population(users, k)
    all_pks = Website.objects.order_by('pk').values_list('pk', flat=True)
    me_vector = to_vector(scores, all_pks)
    seen = set(score.website.pk for score in scores)
    possible = defaultdict(int)
    count = defaultdict(int)
    # this is expensive. do offline/optimize
    # - work on numpy arrays
    # - instead do matrix factorization (svd approximation, nnmf,
    #   alternating squares, ...)
    for other in users:
        other_scores = Score.objects.filter(user=other)
        correlation = pearson_correlation(u1, to_vector(other_scores, all_pks))
        if correlation < 0:
            continue
        for score in other_scores:
            if score.website.pk not in seen:
                possible[score.website.pk] += correlation*score.value
                count[score.website.pk] += 1

    for pk in possible.keys():
        possible[pk] /= float(count[pk])

    return possible
