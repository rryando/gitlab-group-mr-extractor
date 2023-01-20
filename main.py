import requests
import pandas as pd

# Replace with your GitLab API token
API_TOKEN = 'your-gitlab-api-token'

# Replace with the URL of your GitLab instance
GITLAB_URL = 'https://gitlab.com'

# Replace with the ID of the group you want to search in
GROUP_ID = 'target-group-id'

# Replace with the list of usernames you want to search for
USERNAMES = ['ryan.rynaldo1']

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

# Initialize an empty list to store the filtered merge requests
filtered_merge_requests = []

# Loop through the list of merge requests
for merge_request in merge_requests:
    # Extract the relevant information from the merge request
    filtered_merge_request = {
        'username': merge_request['author']['username'],
        'state': merge_request['state'],
        'title': merge_request['title'],
        'source_branch': merge_request['source_branch'],
        'references': merge_request['references']['full'],
        'created_at': merge_request['created_at']
    }

    # Append the filtered merge request to the list
    filtered_merge_requests.append(filtered_merge_request)

# Convert the list of merge requests to a pandas dataframe
df = pd.DataFrame(filtered_merge_requests)

# Output the dataframe to an excel file
df.to_excel('merge_requests.xlsx')