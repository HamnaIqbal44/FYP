# important imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm

# nltk.download('punkt') (package installed for words_tokenization)
# nltk.download('averaged_perceptron_tagger') (package installed for tokens parts of speech)
# nltk.download('maxent_ne_chunker')  # Downloads "English PropBank" model
# nltk.download('words')
# nltk.download('vader_lexicon')

# stylesheet
plt.style.use('ggplot')

# read in data
df = pd.read_csv('Instagram_dashboard.csv')
print(df.head())

# EDA (exploratory data analysis)
# print(df['Review'].value_counts())

# Basic NLTK
example = df['Review'][0]
print("\n", example)

# doing word tokenizing of reviews
tokens = nltk.word_tokenize(example)
print("\n", tokens)

# finding the part of speech for each of these tokens
pos_tokens = nltk.pos_tag(tokens)
print("\n", pos_tokens)

tagged = nltk.chunk.ne_chunk(pos_tokens)
print("\n", tagged)

# First Sentiment Analysis Model: VADER (Valence Aware Dictionary and sEntiment Reasoner) - BoW approach
# STEP 01 vader sentiment scoring
    # we will use nltk's SentimentIntensityAnalyzer to get the neg/neu/pos scores of the text
    # This uses a "bag of words" approach:
    # 1. stop words are removed (and, a, the etc)
    # 2. each word is scored and combined to a total score

sia = SentimentIntensityAnalyzer()
scores = sia.polarity_scores("I love this!")
print("\n", scores)

results = sia.polarity_scores(example)
print("\n", results)


# running the polarity score on entire dataset
score = {}
for index, row in tqdm(df.iterrows()):
    reviews = row['Review']
    dte = row['Date']
    score[dte] = sia.polarity_scores(reviews)

print("\n")
print(score)


vaders = pd.DataFrame(score).T
vaders = vaders.reset_index().rename(columns={'index': 'Date'})
vaders = vaders.merge(df, how='left')

print("\n", vaders.head())

ax = sns.barplot(data=vaders, x='Date', y='compound')
ax.set_title('compound score by reviwes')
plt.show()

ax = sns.barplot(data=vaders, x='Date', y='compound')
ax.set_title('compound score by reviwes')
plt.show()

fig, axs = plt.subplots(1, 3, figsize=(15, 5))
sns.barplot(data=vaders, x='Date', y='pos', ax=axs[0])
sns.barplot(data=vaders, x='Date', y='neu', ax=axs[1])
sns.barplot(data=vaders, x='Date', y='neg', ax=axs[2])
axs[0].set_title('Positive')
axs[2].set_title('Negative')
axs[1].set_title('Neutral')
plt.show()
