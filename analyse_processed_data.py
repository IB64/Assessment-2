"""A script to analyse book data."""
import pandas as pd
import altair as alt

def create_decade_releases_chart(data: pd.DataFrame) -> None:
    """Create a pie chart showing the proportion of books released in each decade."""
    try:
        # Extract the decade from the year
        data['decade'] = (data['year'] // 10) * 10

        # Count the number of books released in each decade
        decade_counts = data['decade'].value_counts().reset_index()
        decade_counts.columns = ['decade', 'count']

        # Create the pie chart
        chart = alt.Chart(decade_counts).mark_arc().encode(
            theta=alt.Theta(field='count', type='quantitative'),
            color=alt.Color(field='decade', type='nominal'),
        ).properties(
            title='Proportion of Books Released in Each Decade'
        )

        # Save the chart as a PNG file
        chart.save('data/decade_releases.png')
        print('Pie chart saved as decade_releases.png')
    except Exception as e:
        print(f'Error creating decade releases chart: {e}')

def create_top_authors_chart(data: pd.DataFrame) -> None:
    """Create a bar chart showing the total number of ratings for the ten most-rated authors."""
    try:
        # Group by author and sum the ratings
        ratings = data.groupby('author_name')['ratings'].sum().reset_index()

        # Select the top 10 authors by ratings
        top_authors = ratings.nlargest(10, 'ratings').sort_values(by='ratings', ascending=True)

        # Create the bar chart
        chart = alt.Chart(top_authors).mark_bar().encode(
            x=alt.X('ratings:Q', title='Total Ratings'),
            y=alt.Y('author_name:N', sort='-x', title='Author')
        ).properties(
            title='Top 10 Authors by Total Ratings'
        )

        # Save the chart as a PNG file
        chart.save('data/top_authors.png')
        print('Bar chart saved as top_authors.png')
    except Exception as e:
        print(f'Error creating top authors chart: {e}')

if __name__ == "__main__":
    # Load the processed data
    processed_data = pd.read_csv('data/PROCESSED_DATA.csv')

    if processed_data is not None:
        # Create the charts
        create_decade_releases_chart(processed_data)
        create_top_authors_chart(processed_data)
