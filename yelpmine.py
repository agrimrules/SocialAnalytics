__author__ = 'agrimasthana'

import json
import urllib
import urllib2
import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

CONSUMER_KEY = 'EvNMmeQq4evxE_i-Ao5yaw'
CONSUMER_SECRET = 'oqEqbrHSbzSxO09IDtdJYNujVJ8'
TOKEN = 'oxfSyeec9HFkTy9qAwVBZagj22mhM8NA'
TOKEN_SECRET = 'MV_oFHP58i2yfFfGFxRZFeArWPM'


def request(host, path, url_params=None):

    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def get_business(business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path)

if __name__ == '__main__':
    response = get_business('arab-cowboy-cafe-and-hookah-lounge-austin')
    res = response['reviews']
    print response['reviews']
