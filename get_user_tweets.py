

import tweepy
import time
import send_msg as tele
consumer_key = "fie98c2LclARc8lH2XdhANREw"
consumer_secret = "zZkNseihPjGPkqR1PUWvlh65tZujhuIDIlj77IyR7zGBAbNO5n"
access_token = "158798447-S3TetLOSzw5FlGbO2DuC2S7l1vaTeC9WGK5MWecj"
access_token_secret = "eJSiJwMkG5wg39sEPmOcmnKZlxkfdSO0y1IgvsOyppVbD"
liste_id=['0']
def signal():

    time.sleep(60)
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    username='TheCoinMonitor_'
    tweets_list= api.user_timeline(screen_name=username, count=2)
    print (liste_id[0])
    tweet_last=tweets_list[0]
    tweet= tweets_list[1]
    if liste_id[-1]==tweet_last.id:
        print ("yeni tweet yok")

    else:
        liste_id.append(tweet_last.id)
        print(liste_id)


        print(tweet.created_at)
        x=tweet.text
        m = x.split("$")
        z =m[2]
        quto = z[0:3]
        quto2 = z[4:8]
        print (quto)
        print (quto2)
        print (m)
        tele.telegram_bot(quto)
        tele.telegram_bot(quto2)
        if m[2] =='BTC SHORTED @':
            print ("xyx")
        else:
            print ("mdj")
        print(tweet.text)
        print(tweet.id)
        print(tweet.in_reply_to_screen_name)

while True:
    signal()












