
from textblob import TextBlob

text_1 = "this is a really cool game. there are a bunch of levels and you can find golden eggs. super fun."
text_2 = "This is a silly game and can be frustrating, but lots of fun and definitely recommend just as a fun time."
#Determining the Polarity 
p_1 = TextBlob(text_1).sentiment.polarity
p_2 = TextBlob(text_2).sentiment.polarity

#Determining the Subjectivity
s_1 = TextBlob(text_1).sentiment.subjectivity
s_2 = TextBlob(text_2).sentiment.subjectivity

print("Polarity of Text 1 is", p_1)
print("Polarity of Text 2 is", p_2)
print("Subjectivity of Text 1 is", s_1)
print("Subjectivity of Text 2 is", s_2)