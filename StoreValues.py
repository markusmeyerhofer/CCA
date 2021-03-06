import mariadb
import sys
import requests
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ssh -L 3306:localhost:3306 pi@cca1.hopto.org

# Note
# Nach min. 15 Minuten Pause "WHERE"-Klausel aus select-Statement entfernen, starten, wieder einsetzen

url = "https://api.nomics.com/v1/currencies/ticker?key=7447a1d2a3e1e93b18d9bbf0006ed748"
request = requests.get(url)
data = request.json()
request.close()

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="phpmyadmin",
        password="F1xKCrC7ydVr",
        host="localhost",
        port=3306,
        database="CCA"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# Get last CRYPTO_DATA-tuple
cur.execute("SELECT price, circulating_supply, market_cap, num_exchanges, volume FROM CRYPTO_DATA WHERE timestamp > "
            "now() - interval 15 minute ORDER BY timestamp ASC LIMIT 1;")
row = cur.fetchone()
price_past, circulating_supply_past, market_cap_past, num_exchanges, volume_past = row

# Calculating changes
price_change_rel = str(price_past / float(data[0]["price"]) * 100)
circulating_supply_change_rel = str(circulating_supply_past / int(data[0]["circulating_supply"]) * 100)
market_cap_change_rel = str(market_cap_past / int(data[0]["market_cap"]) * 100)
num_exchanges_change_rel = str(num_exchanges / int(data[0]["num_exchanges"]) * 100)
volume_change_rel = str(volume_past / float(data[0]["1d"]["volume"]) * 100)

# Insert into CRYPTO_DATA
cur.execute("INSERT INTO CRYPTO_DATA(id,name,price,circulating_supply,market_cap,num_exchanges,num_pairs,volume,"
            "price_change_rel,circulating_supply_change_rel,market_cap_change_rel,num_exchanges_change_rel,"
            "volume_change_rel,timestamp) VALUES('" + data[0]["id"] + "','" + data[0]["name"] + "'," + data[0]["price"]
            + "," + data[0]["circulating_supply"] + "," + data[0]["market_cap"] + "," + data[0]["num_exchanges"]
            + "," + data[0]["num_pairs"] + "," + data[0]["1d"]["volume"] + "," + price_change_rel + "," +
            circulating_supply_change_rel + "," + market_cap_change_rel + "," + num_exchanges_change_rel +
            "," + volume_change_rel + ",'" + timestamp + "')")

# Get data from second API
url2 = "https://api.lunarcrush.com/v2?data=assets&key=bpt6yli7l2vr2ez7ymafo&symbol=BTC"
request2 = requests.get(url2)
data2 = request2.json()["data"][0]
request2.close()

# Insert into SOCIALMEDIA_24H
cur.execute("INSERT INTO SOCIALMEDIA_24H(id, rank_calc_24h, contributors_calc_24h, url_shares_calc_24h,"
            "tweet_spam_calc_24h, news_calc_24h, social_score_calc_24h, social_volume_calc_24h,"
            "average_sentiment_calc_24h, timestamp) VALUES('" + data2["symbol"] + "'," +
            str(data2["alt_rank_calc_24h_previous"]) + "," + str(data2["social_contributors_calc_24h"]) + "," +
            str(data2["url_shares_calc_24h"]) + "," + str(data2["tweet_spam_calc_24h"]) + "," +
            str(data2["news_calc_24h"]) + "," + str(data2["social_score_calc_24h"]) + "," +
            str(data2["social_volume_calc_24h"]) + "," + str(data2["average_sentiment"]) + ",'" + timestamp + "')")

# Insert into SOCIALMEDIA_DATA
cur.execute("INSERT INTO SOCIALMEDIA_DATA(id, url_shares, unique_url_shares, reddit_posts, reddit_posts_score,"
            " reddit_comments, reddit_comments_score, tweets, tweet_spam, tweet_followers, tweet_retweets,"
            " tweet_replies, tweet_favorites, correlation_rank, galaxy_score, social_contributors, social_volume,"
            " social_volume_global, social_dominance, timestamp) VALUES('" + data2["symbol"] + "',"
            + str(data2["url_shares"]) + "," + str(data2["unique_url_shares"]) + "," + str(data2["reddit_posts"]) + ","
            + str(data2["reddit_posts_score"]) + "," + str(data2["reddit_comments"]) + ","
            + str(data2["reddit_comments_score"]) + "," + str(data2["tweets"]) + "," + str(data2["tweet_spam"]) + ","
            + str(data2["tweet_followers"]) + "," + str(data2["tweet_retweets"]) + "," + str(data2["tweet_replies"]) +
            "," + str(data2["tweet_favorites"]) + "," + str(data2["correlation_rank"]) + "," +
            str(data2["galaxy_score"]) + "," + str(data2["social_contributors"]) + "," + str(data2["social_volume"]) +
            "," + str(data2["social_volume_global"]) + "," + str(data2["social_dominance"]) + ",'" + timestamp + "')")

# Get last SOCIALMEDIA_DATA-tuple
cur.execute("SELECT url_shares, unique_url_shares, reddit_posts, reddit_posts_score, reddit_comments,"
            " reddit_comments_score, tweets, tweet_spam, tweet_retweets, galaxy_score, social_volume_global,"
            " social_contributors FROM SOCIALMEDIA_DATA WHERE timestamp > now() - interval 15 minute ORDER BY timestamp"
            " ASC LIMIT 1;")

row = cur.fetchone()
url_shares_past, unique_url_shares_past, reddit_posts_past, reddit_posts_score_past, reddit_comments_past, \
reddit_comments_score_past, tweets_past, tweet_spam_past, tweet_retweets_past, galaxy_score_past, \
social_volume_global_past, social_contributors_past = row

# Calculating changes
url_shares_change_rel = url_shares_past / data2["url_shares"] * 100
unique_url_shares_change_rel = unique_url_shares_past / data2["unique_url_shares"] * 100
reddit_posts_change_rel = reddit_posts_past / data2["reddit_posts"] * 100
reddit_posts_score_change_rel = reddit_posts_score_past / data2["reddit_posts_score"] * 100
reddit_comments_change_rel = reddit_comments_past / data2["reddit_comments"] * 100
reddit_comments_score_change_rel = reddit_comments_score_past / data2["reddit_comments_score"] * 100
tweets_change_rel = tweets_past / data2["tweets"] * 100
tweet_spam_change_rel = tweet_spam_past / data2["tweet_spam"] * 100
tweet_retweets_change_rel = tweet_retweets_past / data2["tweet_retweets"] * 100
galaxy_score_change_rel = galaxy_score_past / data2["galaxy_score"] * 100
social_volume_global_change_rel = social_volume_global_past / data2["social_volume"] * 100
social_contributors_change_rel = social_contributors_past / data2["social_volume_global"] * 100

# Insert into SOCIALMEDIA_DATA_RELATIVE
cur.execute("INSERT INTO SOCIALMEDIA_DATA_RELATIV(id, url_shares_change_rel, unique_url_shares_change_rel,"
            " reddit_posts_change_rel, reddit_posts_score_change_rel, reddit_comments_change_rel,"
            " reddit_comments_score_change_rel, tweets_change_rel, tweet_spam_change_rel, tweet_retweets_change_rel,"
            " galaxy_score_change_rel, social_volume_global_change_rel, social_contributors_change_rel, timestamp)"
            " VALUES('" + data2["symbol"] + "'," + str(url_shares_change_rel) + "," +
            str(unique_url_shares_change_rel) + "," + str(reddit_posts_change_rel) + "," +
            str(reddit_posts_score_change_rel) + "," + str(reddit_comments_change_rel) + "," +
            str(reddit_comments_score_change_rel) + "," + str(tweets_change_rel) + "," +
            str(tweet_spam_change_rel) + "," + str(tweet_retweets_change_rel) + "," +
            str(galaxy_score_change_rel) + "," + str(social_volume_global_change_rel) + "," +
            str(social_contributors_change_rel) + ",'" + str(timestamp) + "')")

# Insert into SOCIALMEDIA_SENTIMENTS
cur.execute("INSERT INTO SOCIALMEDIA_SENTIMENTS(id, tweet_sentiment1, tweet_sentiment2, tweet_sentiment3,"
            " tweet_sentiment4, tweet_sentiment5, tweet_sentiment_impact1, tweet_sentiment_impact2,"
            " tweet_sentiment_impact3, tweet_sentiment_impact4, tweet_sentiment_impact5, average_sentiment,"
            " sentiment_relativ, social_impact_score, timestamp) VALUES('" + data2["symbol"] + "'," +
            str(data2["tweet_sentiment1"]) + "," + str(data2["tweet_sentiment2"]) + "," +
            str(data2["tweet_sentiment3"]) + "," + str(data2["tweet_sentiment4"]) + "," +
            str(data2["tweet_sentiment5"]) + "," + str(data2["tweet_sentiment_impact1"]) + "," +
            str(data2["tweet_sentiment_impact2"]) + "," + str(data2["tweet_sentiment_impact3"]) + "," +
            str(data2["tweet_sentiment_impact4"]) + "," + str(data2["tweet_sentiment_impact5"]) + "," +
            str(data2["average_sentiment"]) + "," + str(data2["sentiment_relative"]) + "," +
            str(data2["social_impact_score"]) + ",'" + timestamp + "')")

conn.commit()
cur.close()
