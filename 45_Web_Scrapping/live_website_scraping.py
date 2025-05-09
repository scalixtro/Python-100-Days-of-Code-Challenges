import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = requests.get('https://news.ycombinator.com/newest')
    webpage = response.text

    # Creamos soup
    soup = BeautifulSoup(webpage, 'html.parser')

    # Queremos imprimir los titulos de los articulos
    article_titles = soup.select('.titleline > a')

    # Obtenemos los titulos de los articulos y los links
    titles = [tag.getText() for tag in article_titles]
    title_links = [tag.get('href') for tag in article_titles]

    # Obtenemos los upvotes
    tags_upvotes = soup.select('.score')
    upvotes = [int(tag.getText().split(' ')[0]) for tag in tags_upvotes]

    # Obtenemos la noticia mas popular en el momento
    max_upvotes = 0
    idx_most_upvoted = 0

    for i in range(len(upvotes)):
        if upvotes[i] > max_upvotes:
            max_upvotes = upvotes[i]
            idx_most_upvoted = i

    print(f'The most upvoted story is: {titles[idx_most_upvoted]:{40}}\t{upvotes[idx_most_upvoted]} votes')
