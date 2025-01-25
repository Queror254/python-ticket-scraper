import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Base URL for constructing full links
BASE_URL = "https://gametime.co"
CONCERT_URL = "https://gametime.co/c/concert"

# File paths for CSVs
ARTIST_CSV = "top_artists.csv"
TICKET_CSV = "artist_tickets.csv"

def scrape_top_artists():
    """
    Scrape the top artists from the concert page and save them to a CSV file.
    """
    response = requests.get(CONCERT_URL)
    # check if the request is OK   
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Locate the Top Artists section
        top_artists_section = soup.select("#content > div > div > div.app-main-content__wrapper > main > div.pages-CategoryPerformers-NonSportsPerformers-module__non-sports-performers-container > div.components-ReactSlickCarousel-ReactSlickCarousel-module__main-container > div.components-ReactSlickCarousel-ReactSlickCarousel-module__slider > div > div > div > div ")

        artists = []

        if top_artists_section:
          # Extract artist names and links
            for artist_div  in top_artists_section:
                 # Look for each specific artist link using the "slick-slide" class
                artist_link = artist_div.select_one("div > div > div > a")

                if artist_link:
                    try:
                       artist_name = artist_link.text.strip()
                       artist_url = BASE_URL + artist_link["href"]
                       
                       # Add to list of artist
                       artists.append({"name": artist_name, "link": artist_url})
                    except Exception as e:
                        print(f"Error processing artist: {e}")
            
                    #except AttributeError:
                       # Skip any incomplete data
                    #   continue
            
            # Save to CSV
            with open(ARTIST_CSV, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "link"])
                writer.writeheader()
                writer.writerows(artists)
            
            print(f"Saved {len(artists)} artists to {ARTIST_CSV}.")
        else:
            print("Could not find the Top Artists section.")
    else:
        print(f"Failed to load the concert page: {response.status_code}")

def scrape_tickets():
    """
    Read artist links from the CSV and scrape ticket details for each artist.
    Save the results in another CSV file with additional fields.
    """
    try:
        # Load artist data from CSV
        with open(ARTIST_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            artists = list(reader)
        
        tickets = []

        for artist in artists:
            artist_name = artist["name"]
            artist_link = artist["link"]
            print(f"Scraping tickets for {artist_name}...")

            response = requests.get(artist_link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Extract ticket details 
                # #content > div > div > div.app-main-content__wrapper > main > div.pages-Performer-Performer-module__body-container > section:nth-child(3) > a:nth-child(2) > div > div > div.components-TableViewCell-TableViewCell-module__main > div > div > span:nth-child(3)
                # # #content > div > div > div.app-main-content__wrapper > main > div.pages-Performer-Performer-module__body-container > section:nth-child(3) > a >
                ticket_elements = soup.select("#content > div > div > div.app-main-content__wrapper > main > div.pages-Performer-Performer-module__body-container > section:nth-child(3) > a")  # Replace with actual ticket selector

                for ticket in ticket_elements:
                    # Replace with actual extraction logic based on HTML structure
                    try:
                        date = ticket.select_one("div > div > div.components-TableViewCell-TableViewCell-module__left > span").text.strip()
                        day = ticket.select_one("div > div > div.components-TableViewCell-TableViewCell-module__left > p").text.strip()
                        event_name = ticket.select_one("div > div > div.components-TableViewCell-TableViewCell-module__main > span").text.strip()
                        time = ticket.select_one("div > div > div.components-TableViewCell-TableViewCell-module__main > div > div > span:nth-child(1)").text.strip()
                        location = ticket.select_one(" div > div > div.components-TableViewCell-TableViewCell-module__main > div > div > span:nth-child(3)").text.strip()
                        city = ticket.select_one("div > div > div.components-TableViewCell-TableViewCell-module__main > div > div > span:nth-child(4)").text.strip()
                        # #content > div > div > div.app-main-content__wrapper > main > div.pages-Performer-Performer-module__body-container > section:nth-child(3) > a:nth-child(2) > div > div > span > div > span
                        raw_price = ticket.select_one("div > div > span > div > span.components-TableViewCell-TableViewCell-module__price-button").text.strip()
                        price = raw_price.replace("FROM", "").strip()  

                        # Save ticket details with artist name
                        tickets.append({
                            "artist": artist_name,
                            "ticket": ticket.text.strip(),
                            "Date": date,
                            "Day": day,
                            "Event Name": event_name,
                            "Time": time,
                            "Location": location,
                            "City": city,
                            "Price": price
                        })
                    except AttributeError:
                        continue  # Skip tickets with missing or incomplete data
            
            else:
                print(f"Failed to load tickets for {artist_name} (status code {response.status_code}).")
        
        # Save tickets to CSV
        with open(TICKET_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["artist", "ticket", "Date", "Day", "Event Name", "Time", "Location", "City", "Price"])
            writer.writeheader()
            writer.writerows(tickets)
        
        print(f"Saved {len(tickets)} tickets to {TICKET_CSV}.")
    
    except FileNotFoundError:
        print(f"{ARTIST_CSV} not found. Please scrape artists first.")

if __name__ == "__main__":
    # Step 1: Scrape Top Artists and Save to CSV
    scrape_top_artists()
    
    # Step 2: Read Artist Links from CSV and Scrape Tickets
    scrape_tickets()
