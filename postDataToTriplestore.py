import requests

# URL for the POST request
url = "http://localhost:3030/ny-db/data"

# Headers for the request
headers = {
    'Content-Type': 'text/turtle'
}

# List of files to be posted
files_to_post = ['Data-Model.ttl']

# Function to post a single file
def post_file(file_name):
    with open(file_name, 'rb') as file:
        response = requests.post(url, headers=headers, data=file)
        print(f"Posted {file_name}: {response.status_code}, {response.reason}")

# Post each file
for file in files_to_post:
    post_file(file)