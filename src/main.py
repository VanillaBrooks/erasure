import tweepy
import time
from api import consumer_key, consumer_secret, access_token, access_token_secret

# get api credentials
def authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# cycle through followers: block them then unblock them
def followers(api):
    count = 0
    for fol in tweepy.Cursor(api.followers).items():
        api.create_block(fol.id)
        api.destroy_block(fol.id)
        count += 1
    return count

# cycle through likes and remove all of them
def favorites(api):
    count = 0
    for fav in tweepy.Cursor(api.favorites).items():
        api.destroy_favorite(fav.id)
        count += 1
    return count

# unfollow everyone you are following
def follows(api):
    count = 0 
    for fol_id in tweepy.Cursor(api.friends_ids).items():
        api.destroy_friendship(fol_id)
        count += 1
    return count

# remove all your tweets
def tweets(api):
    count = 0
    for twt in tweepy.Cursor(api.user_timeline).items():
        api.destroy_status(twt.id)
        count +=1
    return count

if __name__ == "__main__":
    # start timer
    start = time.time()

    # get api 
    try:
        api = authenticate()
    except Exception as e:
        print(f"there was an exception when authenticating with twitter:\n{e}")
        
    # purge everything
    fol = followers(api)
    fav = favorites(api)
    fol_me = follows(api)
    twt =tweets(api)
    
    # end time
    end = time.time()
    diff = str(end-start)[:10]
    
    print(f"deleted {twt} tweets, {fol} followers, {fol_me} follows, {fav} favorites in {diff} seconds")