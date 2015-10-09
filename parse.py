import json

data_file_path = "data/sample_conversations.json"
with open(data_file_path) as data_file:
    data = json.load(data_file)

messages = [message['Text']
            for datum in data['Issues'] 
            for message in datum['Messages']]
