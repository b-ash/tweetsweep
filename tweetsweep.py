import json
import urllib2
import csv
import argparse


def look_for_tweets(handles, matches, excludes, **options):
    if options['csv_to_output']:
        with open(options['csv_to_output'], 'wb') as file:
            get_tweets_for_users(handles, matches, excludes, file, options)
    else:
        get_tweets_for_users(handles, matches, excludes, None, options)


def get_tweets_for_users(handles, matches, excludes, file, options):
    for handle in handles:
        tweets = get_tweets_for_user(handle, matches, excludes, options)

        if file:
            print_tweets_to_csv(file, handle, tweets)
        else:
            print_tweets_to_console(handle, tweets)


def get_tweets_for_user(handle, matches, excludes, options):
    relevant_tweets = []
    max_id = 0
    while True:
        tweets = fetch_page_of_tweets(handle, max_id)
        if not len(tweets):
            break

        relevant_tweets.extend([tweet for tweet in tweets if is_relevant_tweet(tweet, matches, excludes, options)])
        max_id = tweets[-1]['id'] - 1

    return relevant_tweets


def fetch_page_of_tweets(handle, max_id):
    url = "http://api.twitter.com/1/statuses/user_timeline/%s.json?count=200&include_entities=true" % handle
    if max_id:
        url += "&max_id=%s" % max_id
    response = urllib2.urlopen(url)
    if response.getcode() is 429 or response.getcode() is 420:
        print "Yo dawg, you're bogging down twitter, and they're cutting you off. Take a breather, come back in 15 minutes or so."
        raise Exception()
    else:
        return json.load(response)


def is_relevant_tweet(tweet, matches, excludes, options):
    text = tweet['text']
    if options['case_insensitive']:
        text = text.lower()

    matches_cache = dict((item, False) for item in matches)
    excludes_cache = dict((item, False) for item in excludes)

    for bad in excludes:
        if bad in text:
            excludes_cache[bad] = True

    found_exclude = reduce_dict_cache(excludes_cache, options)
    if found_exclude:
        return False

    for match in matches:
        if match in text:
            matches_cache[match] = True

    found_match = reduce_dict_cache(matches_cache, options)
    return found_match


def print_tweets_to_console(handle, tweets):
    print "Handle: %s" % handle
    print "Number of tweets: %i" % len(tweets)

    for tweet in tweets:
        print "%s" % tweet['text']

    print ""


def print_tweets_to_csv(file, handle, tweets):
    tweet_row = ['Tweets']
    tweet_row.extend([tweet['text'].encode('utf8') for tweet in tweets])

    file_writer = csv.writer(file)
    file_writer.writerow(['Handle', handle])
    file_writer.writerow(['Number of tweets', len(tweets)])
    file_writer.writerow(tweet_row)
    file_writer.writerow([])


def get_arguments():
    parser = argparse.ArgumentParser(description='Get tweets for users that contain any of the given strings')
    parser.add_argument('-u', '--usernames', help='A comma-delimited string of the twitter handles to search', required=True)
    parser.add_argument('-m', '--matches', help='A comma-delimited string of the keywords that it may include', required=True)
    parser.add_argument('-e', '--excludes', help='A comma-delimited string of the keywords that it can\'t include', required=False)
    parser.add_argument('-o', '--output', help='An optional CSV file to output the results to', required=False)
    parser.add_argument('-a', '--any', help='Match any of the provided parameters', required=False, action='store_true')
    parser.add_argument('-i', '--insensitive', help='Make the search insensitive', required=False, action='store_true')
    arguments = vars(parser.parse_args())

    return {
        'handles': arguments['usernames'].split(','),
        'matches': format_list_arg('matches', arguments),
        'excludes': format_list_arg('excludes', arguments),
        'csv_to_output': arguments['output'],
        'single_match': arguments['any'],
        'case_insensitive': arguments['insensitive']
    }


def format_list_arg(key, options):
    list_string = options[key]
    if not list_string:
        return []

    list = list_string.split(',')
    if options['insensitive']:
        return [item.lower() for item in list]
    else:
        return list


def reduce_dict_cache(cache, options):
    list = cache.values()
    if not len(list):
        return False

    if options['single_match']:
        return reduce(lambda x, y: x or y, list)
    else:
        return reduce(lambda x, y: x and y, list)


if __name__ == "__main__":
    arguments = get_arguments()
    look_for_tweets(**arguments)
