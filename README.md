# Entrez PubMed Query and Fetch Tool

This script allows you to search and fetch paper details from Entrez, particularly PubMed, and log the results. It also exports the results to a CSV file.


## Setup
1. Install dependencies
```
poetry install
```

2. Create a `credentials.txt` file with your Entrez email and API key, in the following format:
```
email: youremail@example.com
api_key: YOUR_API_KEY_HERE

```

## Usage

```bash
python script_name.py --query "YOUR_SEARCH_QUERY"
