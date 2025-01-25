# PythonTicketScraper

## Overview

PythonTicketScraper is a web scraping project designed to extract information about concerts and artists from the Gametime website. The project aims to provide a simple and efficient way to gather data about upcoming concerts and artist tickets.

## Features

- Scrapes concert information from the Gametime website
- Extracts data about top artists and stores it in a CSV file
- Extracts data about artist tickets and stores it in a CSV file
- Easy to use and customize

## Requirements

- Python 3.x
- `requests` library for sending HTTP requests
- `beautifulsoup4` library for parsing HTML content
- `csv` library for storing data in CSV files. Comes pre-installed with Python.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Queror254/python-ticket-scraper.git
   ```
2. Change to scraper directory
   ```bash
   cd python-ticket-scraper
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the scraper:
   ```bash
   python scraper.py
   ```

## Usage

- Run the `scrape_top_artists()` function to extract data about top artists
- Run the `scrape_artist_tickets()` function to extract data about artist tickets
- Customize the scraper by modifying the `BASE_URL` and `CONCERT_URL` constants

## Data Output

The scraper stores the extracted data in two CSV files:

- `top_artists.csv`: contains information about top artists
- `artist_tickets.csv`: contains information about artist tickets

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This project is for educational purposes only. The Gametime website may have terms of service that prohibit web scraping. Use this project at your own risk.

## Author

techmystic

## Acknowledgments

- Gametime website for providing the data
- `requests`, `beautifulsoup4`, and `csv` libraries for making the project possible
