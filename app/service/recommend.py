from flask import current_app
import numpy as np
from model.user import User
from model.picture import Picture


def sim_distance(prefs, p1, p2):

    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they have no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares = sum([
        pow(prefs[p1][item] - prefs[p2][item], 2) for item in prefs[p1]
        if item in prefs[p2]
    ])
    return 1 / (1 + np.sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they are no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Sum calculations
    n = len(si)
    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / n
    den = np.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r


def topMatches(
        prefs,
        person,
        n=5,
        similarity=sim_distance,
):
    scores = [(similarity(prefs, person, other), other) for other in prefs
              if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_distance):
    totals = {}
    simSums = {}
    for other in prefs:
        # Don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # Ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            # Only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                # The final score is calculated by multiplying each item by the
                #   similarity and adding these products together
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # Create the normalized list
    rankings = [(total / simSums[item], item)
                for (item, total) in totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_prefs(prefs):

    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result


def calculate_similar_items(prefs, n=10):

    result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transform_prefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print('%d / %d' % (c, len(itemPrefs)))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


def get_recommended_items(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # Loop over items rated by this user
    for (item, rating) in userRatings.items():
        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings and userRatings[item2] != 0:
                current_app.logger.info(
                    'user: %s has already rated this item: %s' % (user, item2))
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item)
                for (item, score) in scores.items()]
    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


def select_random_user_and_likes(self_user, num=5):
    users = User.objects().aggregate(*[{
        '$match': {
            'username': {
                '$ne': self_user.username
            }
        }
    }, {
        '$sample': {
            'size': num
        }
    }])

    rec_dict = {}
    for user in users:
        rec_dict[user['username']] = {}
        if user.__contains__('likes'):
            for pic_id in user['likes']:
                rec_dict[user['username']][pic_id] = 1  # TODO: right

    # self user
    rec_dict[self_user['username']] = {}
    if self_user.__contains__('likes'):
        for pic_id in self_user['likes']:
            rec_dict[self_user['username']][pic_id] = 1

    return rec_dict


def fill_dict_with_others(rec_dict):
    pid_set = {}
    # a set to count the ids
    for u in rec_dict:
        for pic_id in rec_dict[u]:
            pid_set[pic_id] = 1

    for pid in pid_set:
        for u in rec_dict:
            rec_dict[u][pid] = (1 if rec_dict[u].__contains__(pid)
                                and rec_dict[u][pid] == 1 else 0)

    return rec_dict


def recommend_likes(user, num=5):
    rec_dict = select_random_user_and_likes(user)
    rec_dict = fill_dict_with_others(rec_dict)

    item_sim = calculate_similar_items(rec_dict)

    result = get_recommended_items(rec_dict, item_sim, user.username)
    result = result[:5]

    no_0_result = []
    for (r, pid) in result:
        if r > 0:
            no_0_result.append(pid)

    pics = Picture.objects(id__in=no_0_result)

    return pics
