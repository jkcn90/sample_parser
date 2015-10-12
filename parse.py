import os
import sys
import json
import numpy as np

from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

import sample_parser
from sample_parser.ternary_search_tree import TernarySearchTree as SearchTree

data_file_path = "data/sample_conversations.json"
data_file_path = os.path.join(sample_parser.__path__[0], data_file_path)
with open(data_file_path) as data_file:
    data = json.load(data_file)

messages = [message['Text']
            for datum in data['Issues'] 
            for message in datum['Messages']]

words = [message.split() for message in messages]
words = [word for word_list in words for word in word_list]
words = list(set(words))

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                             stop_words='english',
                             max_df=0.01, min_df=0.001)
X = vectorizer.fit_transform(messages)

n_components = 500
svd = TruncatedSVD(n_components)
lsa = make_pipeline(svd, Normalizer(copy=False))

X = lsa.fit_transform(X)

n_clusters = 30

km = MiniBatchKMeans(n_clusters=n_clusters, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000)
km.fit(X)
message_predictions = km.predict(X)

word_tree = SearchTree()
for word in words:
    word_tree.add(word)
