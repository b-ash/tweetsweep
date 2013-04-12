# TweetSweep

## What is TweetSweep?

TweetSweep is a lightweight command-line tool that lets you sweep any twitter handle for desired strings. It can optionally avoid undesirable strings or output to a .csv

## Usage

### Parameters

* `-u, --usernames` 
    * A comma-delimited string of twitter handles to search
    * `-u bryan_ash,some_other_handle`
    * Required

* `-m, --matches`
    * A comma-delimited string of the keywords that a tweet should include
    * `-i P90X,HubSpot`
    * Required

* `-e, --excludes`
    * A comma-delimited string of the keywords that shouldn't be present in a tweet
    * `-e instagram`
    * Not Required

* `-o, --output`
    * An optional CSV file to output the results to. If this isn't included, the results are printed to the console.
    * `-o tweets.csv`
    * Not required

* `-a, --any`
    * Match any of the provided keywords.
    * `-a`
    * Not required

* `-i, --insensitive`
    * Make the search case-insensitive
    * `-i`
    * Not required

## Sample Output

`python tweetsweep.py -u bryan_ash -m p90x,hubspot -i -a`

Handle: bryan_ash

Number of tweets: 147

Get ready, get set, #getatme with @hubspotdev http://t.co/WGhT8qCJBe

..........

Foam Roller acquired. Get ready @P90X2, I'm coming for ya! #bestshapeofmylife

Ohmygoshohmygosh #bringit @P90X2 http://t.co/BjUkKpcd

## Disclaimers

* Only tested on Mac OS X.

* Pull requests are welcome!

* Twitter's API only allows a given network to hit their API 150 times per hour. Check out the [docs](https://dev.twitter.com/docs/rate-limiting/1.1) for more info.

## TODO

* Handle Twitter's 400s and have friendly output.

## License
Copyright (c) 2013 Bryan (Bash) Ash
Licensed under the MIT license.
