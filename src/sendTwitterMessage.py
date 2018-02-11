import tweepy


def send_twitter_message(consumer_key, consumer_secret, access_token, access_secret, message):
    """
    Simple wrapper for sending a Twitter message.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    api.update_status(message)
