"""
This script queries the Censys API to retrieve X.509 certificate records, based on the specified search query.
The records are filtered to include only trusted and unexpired certificates with a name containing "censys.io".
The retrieved records are then stored in a CSV file with specified file name.

You NEED to install the pandas and censys Python libraries (pip install censys && pip install pandas)

To use this script, you must first obtain API credentials (api_id and api_secret) from censys.io.
The script can be run with the following command line arguments:
    --api_id: Your API ID for accessing censys.io
    --api_secret: Your API secret for accessing censys.io
    --max_records: The number of records to retrieve (0.4 actions per second)
    --csv_name: The name of the output CSV file.

Example usage:
    python censys_script.py --api_id=<API_ID> --api_secret=<API_SECRET> --max_records=<Number of records to pull> --csv_name=<CSV Name>
"""


# Import required libraries for querying the Censys API and storing the results in a CSV file
from censys.search import CensysCertificates
import pandas as pd
import argparse

# Define a function for querying the Censys API for trusted and unexpired X.509 certificates
def query_trusted_unexpired_x509_certificates(api_id, api_secret, max_records, csv_name):
    # Create a Censys API object using the API ID and secret
    censys_api_object = CensysCertificates(api_id=api_id, api_secret=api_secret)

    # Define the fields to be retrieved from the API
    fields = [
        "parsed.fingerprint_sha256",
        "parsed.validity.start",
        "parsed.validity.end",
    ]

    # Initialize an empty dataframe to store the retrieved records
    certificates = pd.DataFrame(columns=["parsed.validity.start", "parsed.validity.end", "parsed.fingerprint_sha256"])

    # Retrieve the records from the Censys API and store them in the dataframe
    for i in censys_api_object.search("parsed.names:censys.io and tags: trusted", fields, max_records=max_records):
        certificates = certificates.append(i, ignore_index=True)

    # Rename the columns in the dataframe for clarity
    certificates.rename(columns={'parsed.validity.start': 'Validity Start',
                                 'parsed.validity.end': 'Validity End',
                                 'parsed.fingerprint_sha256': 'SHA256 Fingerprint'}, inplace=True)
    # Reorder the columns in the dataframe
    certificates = certificates[['SHA256 Fingerprint', 'Validity Start', 'Validity End']]

    # Save the dataframe as a CSV file
    certificates.to_csv(csv_name, index=False)

# Define command line arguments to be passed to the script
parser = argparse.ArgumentParser("censys_script.py")
parser.add_argument("--api_id", help="API ID to query the Censys API", type=str)
parser.add_argument("--api_secret", help="API secret to query the Censys API", type=str)
parser.add_argument("--max_records", help="Maximum number of records to retrieve from the Censys API", type=int)
parser.add_argument("--csv_name", help="Name of the CSV file to store the retrieved records", type=str)

# Parse the command line arguments
args = parser.parse_args()

# Call the function to query the Censys API and store the results in a CSV file
query_trusted_unexpired_x509_certificates(args.api_id, args.api_secret, args.max_records, args.csv_name)
