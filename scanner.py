import requests  # To send HTTP requests and get webpage content
import re        # To use regular expressions for extracting links
import urllib.parse as urlparse  # To handle relative and absolute URLs

class Scanner:
    def __init__(self, url):
        self.target_url = url  # Base URL provided by the user
        self.target_links = []  # List to store unique links found during crawl

    def extract_links_from(self, url):
        try:
            response = requests.get(url)  # Fetch HTML content of the page
            return re.findall('(?:href=")(.*?)"', response.text)  # Extract all href links using regex
        except requests.exceptions.RequestException:
            return []  # If the request fails, return an empty list

    def crawl(self, url):
        href_links = self.extract_links_from(url)  # Get all links from the current page
        for link in href_links:
            link = urlparse.urljoin(url, link)  # Convert relative links to full URLs

            if "#" in link:
                link = link.split("#")[0]  # Remove fragment identifiers (e.g., #section)

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)  # Add only new, internal links
                print(link)
                self.crawl(link)  # Recursively crawl the new link

# User input section
if __name__ == "__main__":
    user_url = input("Enter the URL to scan: ")  # Example: https://example.com
    scanner = Scanner(user_url)
    scanner.crawl(user_url)
