"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map
from functools import reduce
from operator import mul

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in `centroids` that is closest to `location`. If two
    centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    "*** REPLACE THIS LINE ***"

    distance_array=[[location]+[each] for each in centroids]
    return min(distance_array,key=lambda x:distance(x[0],x[1]))[1]
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in `centroids`. Each item in
    `restaurants` should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
    "*** REPLACE THIS LINE ***"

    return group_by_first([[find_closest(restaurant_location(restaurant),centroids),restaurant] for restaurant in restaurants])
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the `cluster` based on the locations of the
    restaurants."""
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"

    each_location = []
    longitude = []
    latitude = []
    for restaurant in cluster:
        each_location = restaurant_location(restaurant)
        longitude += [each_location[0]]
        latitude += [each_location[1]]

    return [mean(longitude), mean(latitude)]


    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group `restaurants` by location into `k` clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]
    clusters=[]
    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        clusters=group_by_centroid(restaurants,old_centroids)
        centroids=[ find_centroid(cluster) for cluster in clusters]
        # END Question 6
        n += 1
    return centroids


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for `user` by performing least-squares linear regression using `feature_fn`
    on the items in `restaurants`. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    # a extract value for restaurants
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]
    # ratings from the user to restaurants

    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"
    b, a, r_squared = 0, 0, 0  # REPLACE THIS LINE WITH YOUR SOLUTION
    S_xx=square_sum(xs)
    S_yy=square_sum(ys)
    S_xy=square_mul(xs,ys)
    assert S_xx!=0, "ZeroDivision error!"
    b=S_xy/S_xx
    a=mean(ys)-b*mean(xs)
    r_squared=(S_xy**2)/(S_xx*S_yy)

    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def square_sum(lst):
    """return the sum of the squre difference of the lst
    >>> square_sum([1,2,3])
    2.0
    """
    mean_v=mean(lst)
    return reduce(lambda x,y :x+y,map(lambda x:(x-mean_v)**2, lst))

def square_mul(lst1,lst2):
    """ return the sum of mul difference between two lsts
    >>> square_mul([1,2,3],[1,2,3])
    2.0
    """
    zip_lst=zip(lst1,lst2)
    mean_1=mean(lst1)
    mean_2=mean(lst2)
    return reduce(lambda x,y:x+y,map(lambda x:mul(x[0]-mean_1,x[1]-mean_2), zip_lst))

if __name__ =="__main__":
  import doctest
  doctest.testmod()


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within `feature_fns` that gives the highest R^2 value
    for predicting ratings by the `user`; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    return max([ find_predictor(user,reviewed,feature) for feature in feature_fns],
               key=lambda x:x[1])[0]
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of `restaurants` by `user` using the best
    predictor based a function from `feature_fns`.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    reviewed_name=[restaurant_name(restaurant) for restaurant in reviewed]
    # BEGIN Question 9
    #restaurants being rated by user
    rates_of_all={}
    for restaurant in restaurants:
        if restaurant_name(restaurant) not in reviewed_name :
            rates_of_all[restaurant_name(restaurant)]=predictor(restaurant)
        else:
            rates_of_all[restaurant_name(restaurant)]=user_rating(user,restaurant_name(restaurant))
    return rates_of_all

    # END Question 9


def search(query, restaurants):
    """Return each restaurant in `restaurants` that has `query` as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    return [ restaurant for restaurant in restaurants if query in restaurant_categories(restaurant)]
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [restaurant_mean_rating,
            restaurant_price,
            restaurant_num_ratings,
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)
