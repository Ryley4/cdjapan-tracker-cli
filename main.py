import requests
from bs4 import BeautifulSoup
import time

def fetch_vinyls(artist_name, known_vinyls):
    search_query = "+".join(artist_name.split())

    url = f"https://www.cdjapan.co.jp/searchuni?term.media_format=&q={search_query}&fq.media=LP"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        vinyl_listings = soup.find_all('a', class_='item-wrap')

        new_vinyls = []
        for listing in vinyl_listings:
            if "No longer available" in listing.get_text():
                continue

            title_element = listing.find('div', class_='title')
            title = title_element.get_text(strip=True) if title_element else "Unknown Title"
            link = listing['href']

            if title not in known_vinyls:
                known_vinyls.add(title)
                new_vinyls.append({
                    'title': title,
                    'link': f"https://www.cdjapan.co.jp{link}"
                })

        return new_vinyls

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching vinyls: {e}")
        return []

if __name__ == "__main__":
    artist_name = input("Enter the artist's name: ").strip()
    known_vinyls = set()

    print(f"Fetching initial list of vinyls for {artist_name}...")
    initial_vinyls = fetch_vinyls(artist_name, known_vinyls)
    if initial_vinyls:
        print("\nInitial Vinyls Found:")
        for vinyl in initial_vinyls:
            print(f"Title: {vinyl['title']}")
            print(f"\033[94mLink: {vinyl['link']}\033[0m\n")  
    else:
        print("No vinyls found.")

    print(f"\nTracking vinyls for {artist_name}. Press Ctrl+C to stop.")
    try:
        while True:
            new_vinyls = fetch_vinyls(artist_name, known_vinyls)
            if new_vinyls:
                print("\nNew Vinyls Found:")
                for vinyl in new_vinyls:
                    print(f"Title: {vinyl['title']}")
                    print(f"\033[94mLink: {vinyl['link']}\033[0m\n")  

            else:
                print("No new vinyls found.")

            time.sleep(300) 

    except KeyboardInterrupt:
        print("\nStopped tracking vinyls.")
