import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import time

def google_search(query, num_results=10):
   
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    params = {
        "q": query,
        "num": num_results
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print("Failed to retrieve results")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select('.tF2Cxc'):
        title_element = result.select_one('h3')
        link_element = result.select_one('a')
        description_element = result.select_one('.VwiC3b')

        if title_element and link_element and description_element:
            results.append({
                "title": title_element.get_text(),
                "link": link_element['href'],
                "description": description_element.get_text()
            })

    if not results:
        print("No results found. The HTML structure might have changed.")
    
    return results

def save_to_csv(data, filename="search_results.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

query = input("Enter your search query: ") 
num_results = int(input("Enter the number of results to fetch: ")) 

results = google_search(query, num_results)

for idx, result in enumerate(results, start=1):
    print(f"\nResult {idx}:")
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Description: {result['description']}")

save = input("Would you like to save the results to a CSV file? (y/n)").strip().lower()
if save in ["yes", "y"]:
    filename = input("Enter the filename (e.g., search_results.csv): ").strip()
    save_to_csv(results, filename)
else:
    print("Results were not saved.")