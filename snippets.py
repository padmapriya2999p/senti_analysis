from collections import defaultdict
from textblob import TextBlob

# Define aspects to analyze
aspects = ['gameplay', 'graphics', 'user interface']

# Provided dataset of customer reviews
reviews = [
    "This is a pretty good version of the game for being free. There are LOTS of different levels to play. My kids enjoy it a lot too.,1",
    "This is a really cool game. there are a bunch of levels and you can find golden eggs. super fun.,1",
    "This is a silly game and can be frustrating, but lots of fun and definitely recommend just as a fun time.,1",
    "This is a terrific game on any pad. Hrs of fun.  My grandkids love it. Great entertainment when waiting in long lines,1",
    "This is super fun though a little frustrating at times!!!!!!!!! I loved it before I got my kindle I would beg my brother and dad to play. But when I get it I play it all the time!!!!!!,1",
    "This seems to be popular when my kindle fire is out of my hands.  Lots of fun and free time for me plus the graphics are very, very nice.,1",
    "This was a very entertaining and challenging game with several levels to seek improvement. The ads did not overrun it and, for free, this was an excellent program.,1",
    "This keeps me busy all the time. I am really happy about this app, I have never ever had any problems.,1",
    "Very fun and challenges you, I always try and get three stars, nice graphics and gameplay, always a good way to kill time.,1",
    "Very high quality for a game. Fast, and crystal clear. Amazing that a game so popular, would be FREE! All levels to accomplish to become an Angry Birds Pro.~ Jessie,1",
    "This is the best game ever!!!!!  it is so fun and addicting. there is so many different episodes that are amazing. love it!,1",
    "This is the one of the best apps because it is a good time consuming game wherever you go because you do not need wifi.,1",
    "This is the original Angry Birds game but it only works on the original Kindle Fire and not on the new HD version.,1",
    "What can I say?  Ya Can't improve on perfection.  Great for traveling or times when you just need to relax.,1"
]

# Initialize dictionary to store sentiment scores for each aspect
aspect_sentiments = defaultdict(list)

# Iterate through reviews and calculate sentiment scores for each aspect
for review in reviews:
    review_text, sentiment = review.rsplit(',', 1)
    sentiment = int(sentiment)
    for aspect in aspects:
        if aspect in review_text.lower():
            # Calculate sentiment polarity using TextBlob
            polarity_score = TextBlob(review_text).sentiment.polarity
            aspect_sentiments[aspect].append(polarity_score)

# Calculate average sentiment score for each aspect
average_aspect_sentiments = {aspect: sum(scores) / len(scores) for aspect, scores in aspect_sentiments.items()}

# Print average sentiment scores for each aspect
for aspect, score in average_aspect_sentiments.items():
    print(f"Average sentiment score for {aspect}: {score:.2f}")
