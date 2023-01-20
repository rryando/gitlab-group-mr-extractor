# GitLab Merge Requests Extractor

This script is used to extract merge requests from a specific group in GitLab by a specific author(s) and export the result to a CSV file.

## Requirements

- Python 3
- requests library (can be installed using `pip install requests`)
- pandas library (can be installed using `pip install pandas`)

## Usage

1. Replace the placeholder values in the script with your own information:

- API_TOKEN: Your GitLab API token
- GITLAB_URL: The URL of your GitLab instance
- GROUP_ID: The ID of the group you want to search in
- USERNAMES: A list of usernames you want to search for

2. Run the script using the command `python main.py`
3. The script will output a Excel file named `merge_requests.xlsx` containing the merge requests data.

## Note

The script extracts the following information for each merge request:

- username
- state
- title
- source_branch
- references.full
- created_at

You can customize the extracted information by modifying the script accordingly.
