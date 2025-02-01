import requests
from bs4 import BeautifulSoup
from googlesearch import search
import os


# Define a function to perform a Google search and filter PDF links
def search_pdfs(topic, author=None, keywords=None):
    # Construct the search query
    query = f"{topic} filetype:pdf"
    if author:
        query += f" {author}"
    if keywords:
        query += f" {' '.join(keywords)}"

    # Perform Google search
    print(f"Searching for PDFs with query: {query}")
    results = search(query, num=2)  # Use 'num' instead of 'num_results'

    # Filter and store only the PDF links
    pdf_links = [result for result in results if result.endswith(".pdf")]
    
    return pdf_links


# Function to download PDFs
def download_pdf(url, download_folder="pdf_downloads"):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(download_folder, exist_ok=True)  # Create directory if not exists
            filename = os.path.join(download_folder, url.split("/")[-1])
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Main function to handle user input and perform search
def main():
    topic = input("Enter the name of the topic: ")
    author = input("Enter any author recommendations (optional): ")
    keywords = input("Enter any relevant keywords separated by commas (optional): ")
    keywords_list = [kw.strip() for kw in keywords.split(",")] if keywords else None
    
    # Search for PDFs
    pdf_links = search_pdfs(topic, author, keywords_list)
    
    # Display and download PDFs
    if pdf_links:
        print(f"Found {len(pdf_links)} PDFs:")
        for idx, link in enumerate(pdf_links):
            print(f"{idx + 1}: {link}")
            download_pdf(link)
    else:
        print("No PDF links found.")

if __name__ == "__main__":
    main()
