import json

from ternary_search_tree import TernarySearchTree as SearchTree

data_file_path = "data/sample_conversations.json"
with open(data_file_path) as data_file:
    data = json.load(data_file)

messages = [message['Text']
            for datum in data['Issues'] 
            for message in datum['Messages']]

words = [message.split() for message in messages]
words = [word for word_list in words for word in word_list]
words = list(set(words))

tree = SearchTree()
for word in words:
    tree.add(word)
