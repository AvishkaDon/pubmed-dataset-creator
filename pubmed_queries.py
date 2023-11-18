import os
import logging
from datetime import datetime
import argparse

from Bio import Entrez
import pandas as pd

# Global constants
CHUNK_SIZE = 2000
CREDENTIALS_FILE = "credentials.txt"
LOGS_DIR = "logs"
RESULTS_DIR = "data"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def read_credentials(filename):
    """Read Entrez credentials from a file."""
    with open(filename, "r") as file:
        email, api_key = [line.split(":")[1].strip() for line in file]
    return email, api_key

def setup_logging():
    """Set up logging configuration."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    log_filename = os.path.join(LOGS_DIR, f"log_{datetime.now():%Y%m%d_%H%M%S}.log")
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        handlers=[logging.FileHandler(log_filename),
                                  logging.StreamHandler()])

def set_entrez_credentials(email, api_key):
    """Set Entrez email and API key."""
    Entrez.email = email
    Entrez.api_key = api_key

def search(query, retmax=CHUNK_SIZE, retstart=0):
    """Send search query to Entrez."""
    logging.info("Sending search query: %s, retmax: %s, starting at %s", query, retmax, retstart)
    handle = Entrez.esearch(db="pubmed", sort="relevance", retmax=retmax, retstart=retstart, retmode="xml", term=query)
    results = Entrez.read(handle)
    logging.info("Received %s results", len(results["IdList"]))
    return results

def search_all(query):
    """Search all results for a query."""
    all_ids = []
    initial_results = search(query, retmax=1)
    total_count = int(initial_results["Count"])

    for start in range(0, total_count, CHUNK_SIZE):
        results = search(query, retmax=CHUNK_SIZE, retstart=start)
        all_ids.extend(results["IdList"])
        logging.info("Fetched %s papers, range %s to %s", len(all_ids), start, start + CHUNK_SIZE)

    return all_ids

def fetch_details(id_list):
    """Fetch details for a list of IDs."""
    logging.info("Fetching details for %s papers", len(id_list))
    handle = Entrez.efetch(db="pubmed", retmode="xml", id=",".join(id_list))
    results = Entrez.read(handle)
    logging.info("Received paper details")

    papers = [{'PMID': paper['MedlineCitation']['PMID'],
               'Title': paper['MedlineCitation']['Article']['ArticleTitle'],
               'Abstract': paper.get('MedlineCitation', {}).get('Article', {}).get('Abstract', {}).get('AbstractText', ['No abstract available'])[0]}
              for paper in results['PubmedArticle']]
    return papers

def save_results(papers, dir=RESULTS_DIR):
    """Save paper details to a CSV file."""
    if not os.path.exists(dir):
        os.makedirs(dir)

    df = pd.DataFrame(papers)
    filename = os.path.join(dir, f"results_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(filename, index=False)
    logging.info("Results saved to %s", filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch paper details from Entrez.")
    parser.add_argument("--query", default="female infertility AND systematic [sb]", help="Entrez search query.")
    args = parser.parse_args()

    setup_logging()
    email, api_key = read_credentials(CREDENTIALS_FILE)
    set_entrez_credentials(email, api_key)

    start_time = datetime.now()
    all_ids = search_all(args.query)
    papers = fetch_details(all_ids)
    save_results(papers)

    logging.info(f"Run time: {datetime.now() - start_time}")
