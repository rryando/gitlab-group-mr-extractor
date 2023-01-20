import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import requests

# Replace with your GitLab API token
API_TOKEN = 'your-gitlab-api-token'

# Replace with the URL of your GitLab instance
GITLAB_URL = 'https://gitlab.com'

# Replace with the ID of the group you want to search in
GROUP_ID = 'target-group-id'

# Replace with the list of usernames you want to search for
USERNAMES = ['ryan.rynaldo1', 'mikqi']

# Replace with number of MR to fetch
NUM_OF_MR = 100

# Initialize an empty list to store the merge requests
merge_requests = []


for username in USERNAMES:
    # Construct the API URL to search for merge requests in the group by the current username
    api_url = f'{GITLAB_URL}/api/v4/groups/{GROUP_ID}/merge_requests?state=all&author_username={username}&per_page={NUM_OF_MR}'

    # Send a GET request to the API URL
    response = requests.get(api_url, headers={'PRIVATE-TOKEN': API_TOKEN})

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Error: {response.content}')
    else:
        # Parse the JSON response

        merge_requests.extend(response.json())


def train_classifier(sample_data):
    sample_text = [f'{data["title"]} {data["source_branch"]}' for data in sample_data]
    labels = [data['classification'] for data in sample_data]
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(sample_text)
    classifier = MultinomialNB()
    classifier.fit(features, labels)
    return classifier, vectorizer

def classify_merge_requests(merge_requests, classifier, vectorizer):
    filtered_merge_requests = []
    for merge_request in merge_requests:
        title = merge_request['title']
        source_branch = merge_request['source_branch']
        text = f'{title} {source_branch}'
        features = vectorizer.transform([text])
        classification = classifier.predict(features)[0]
        filtered_merge_request = {
            'username': merge_request['author']['username'],
            'state': merge_request['state'],
            'title': merge_request['title'],
            'source_branch': merge_request['source_branch'],
            'references': merge_request['references']['full'],
            'created_at': merge_request['created_at'],
            'classification': classification
        }
        filtered_merge_requests.append(filtered_merge_request)
    return filtered_merge_requests

# Load sample data from a JSON file
with open('sample_role_classification.json', 'r') as file:
    sample_data = json.load(file)

# Train the classifier using the sample data
classifier, vectorizer = train_classifier(sample_data)

# Classify the merge requests using the trained classifier
filtered_merge_requests = classify_merge_requests(merge_requests, classifier, vectorizer)

df = pd.DataFrame(filtered_merge_requests)

# Output the dataframe to an excel file
df.to_excel('merge_requests.xlsx')