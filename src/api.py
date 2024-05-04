"""
This module manages the API usage for fetching images from Unsplash and Pexels.
It contains functions for checking the API usage, resetting the API usage count, and loading the API access key from a configuration file.
The `check_api_usage` function ensures that the application does not exceed the API usage limit for the selected site.
"""

import json
import os

API_USAGE_FILE = 'api_usage.txt'
API_USAGE_LIMIT = int(os.getenv('API_USAGE_LIMIT', 500))

def check_api_usage(site):
    """
    Checks the API usage for the specified site.

    Parameters:
    - site (str): The site to check API usage for ('Unsplash' or 'Pexels').

    Returns:
    - bool: True if the API usage limit has not been reached, False otherwise.
    """
    # Implementation depends on how API usage is tracked
    if not os.path.exists(API_USAGE_FILE):
        with open(API_USAGE_FILE, 'w') as f:
            f.write(json.dumps({site: 0}))
    with open(API_USAGE_FILE, 'r') as f:
        usage = json.loads(f.read().strip())
    if usage.get(site, 0) >= API_USAGE_LIMIT:
        print(f"API usage limit reached for {site}. Please wait or reset the API usage.")
        return False
    usage[site] = usage.get(site, 0) + 1
    with open(API_USAGE_FILE, 'w') as f:
        f.write(json.dumps(usage))
    return True

def reset_api_usage_count():
    """
    Resets the API usage count for the specified site.

    Parameters:
    - site (str): The site to reset API usage count for ('Unsplash' or 'Pexels').
    """
    # Implementation depends on how API usage is managed

    with open(API_USAGE_FILE, 'w') as f:
        f.write('0')
    print("API usage count has been reset.")

def load_api_access_key(site):
    """
    Loads the API keys from a configuration file.

    Returns:
    - config (dict): A dictionary containing the API keys.
    """
    if os.path.exists('config.json'):
        with open('config.json') as f:
            data = json.load(f)
            if site == 'Unsplash':
                return data.get('unsplash_access_key')
            elif site == 'Pexels':
                return data.get('pexels_access_key')
            else:
                print(f"Error: Unsupported site '{site}'.")
                return None
    else:
        print("Configuration file not found.")
        return None
