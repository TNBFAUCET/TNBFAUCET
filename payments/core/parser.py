import re
import os
import configparser
import requests

from urllib.parse import urlparse
from .model import PostModel


def validate_hashtag(tags, to='TNBFaucet'):
    for tag in tags:
        if tag.lower() == to.lower():
            return True
    return False


def find_account_number(text):
    match = re.search(r'[0-9a-fA-F]{64}', text)
    if match:
        return match.group()


def process(tweet_url, amount):
    access_token = os.getenv('ACCESS_TOKEN_TWITTER')
    url = urlparse(tweet_url)
    path = url.path
    if path and path[-1] == '/':
        path = path[:-1]
    endpoint = path.split('/')[-1]
    if not endpoint.isnumeric():
        '''
        logger.error(f'Cannot determine tweet id for <{tweet_url}>')
        '''
        return

    tweet_id = int(endpoint)

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(
        f'https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=entities,author_id', headers=headers)

    if response.status_code != 200:
        '''
        logger.debug((
            'Cannot find tweet of id '
            f'<{tweet_id}> <Error:{response.text}>'))
        logger.error((
            f'Cannot find tweet of id for <{tweet_url}>'))
        '''
        return

    data = response.json()
    user_id = data['data']['author_id']
    post = PostModel(tweet_id, amount)
    account_number = find_account_number(data['data']['text'])
    
    if not account_number:
        '''
        logger.debug(('Invalid account number for '
                      f'<User:{user_id}> via <Twitter:{tweet_id}>'))
        logger.error(f'Invalid account number for <{tweet_url}>')
        '''
        return

    post.set_account_number(account_number)
    post.set_user(user_id)

    hashtags = []
    for tag in data['data']['entities']['hashtags']:
        hashtags.append(tag['tag'])
    if validate_hashtag(hashtags):
        '''
        logger.debug(str(post))
        logger.info(f'Seeking <{str(amount)}> via <{tweet_url}>')
        '''
        return post

if __name__ == '__main__':
    pass

print(process('https://twitter.com/oshioki4/status/1372101447794368512', 50))
