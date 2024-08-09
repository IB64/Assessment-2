"""A script to process book data."""
import re
import sys

import pandas as pd

AUTHORS = pd.read_csv('data/AUTHORS.csv')

def clean_title(title: str) -> str:
    """Remove text inside brackets (and the brackets themselves)"""
    cleaned_title = re.sub(r'\[.*?\]|\(.*?\)', '', title).strip()
    return cleaned_title

def clean_rating(rating: str) -> str:
    """Replace commas with dots in rating values (e.g., "4,16" -> "4.16")"""
    return rating.replace(',', '.')

def clean_ratings(ratings: str) -> str:
    """Remove backticks from ratings values (e.g., `4501032` -> 4501032)"""
    return ratings.replace('`', '')

def process_raw_data(file_path: str) -> None:
    """Main function that processes the raw data and outputs a cleaned file."""
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)

        # Convert headings to lowercase
        data.columns = [x.lower() for x in data.columns]

        # Select only the required columns
        data = data[['book_title', 'author_id', 'year released', 'rating', 'ratings']]

        # Drop rows with missing values for 'title' or 'author_name'
        data.dropna(subset=['book_title', 'author_id'], inplace=True)

        # Merge in author names to match with author_id
        data = pd.merge(data, AUTHORS, on="author_id")

        # Drop author_id
        data = data[['book_title', 'name', 'year released', 'rating', 'ratings']]

        # Clean the titles by removing text within brackets
        data['book_title'] = data['book_title'].apply(clean_title)

        # Clean the 'rating' and 'ratings' columns
        data['rating'] = data['rating'].apply(clean_rating)
        data['ratings'] = data['ratings'].apply(clean_ratings)

        # Ensure numeric columns are correctly formatted
        data['year released'] = pd.to_numeric(data['year released'])
        data['rating'] = pd.to_numeric(data['rating'])
        data['ratings'] = pd.to_numeric(data['ratings'])

        # Sort the data by descending order of rating
        data = data.sort_values(by='rating', ascending=False)

        # Rename columns to wanted names
        data.rename(columns={'book_title': 'title',
                             'name': 'author_name',
                             'year released': 'year'}, inplace=True)

        # Write the processed data to a new CSV file
        data.to_csv('PROCESSED_DATA.csv', index=False)

        print("Data processing complete. PROCESSED_DATA.csv has been created.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_raw_data.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        process_raw_data(file_path)
