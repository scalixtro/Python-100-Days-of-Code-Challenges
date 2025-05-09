import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # Get webpage
    response = requests.get('https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/')
    webpage = response.text

    # Create soup
    soup = BeautifulSoup(webpage, 'html.parser')

    # Get all movie titles
    tags_top_movie_titles = soup.select('.article-title-description__text .title')
    top_movies = [' '.join(tag.getText().split(' ')[1:]) for tag in tags_top_movie_titles]
    top_movies = top_movies[::-1]  # Reverse list to get movies from 1-100

    print('Top 100 movies of all time')
    for i, movie in enumerate(top_movies):
        print(f'{i+1}. {movie}')
