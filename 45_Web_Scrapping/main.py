from bs4 import BeautifulSoup

if __name__ == '__main__':
    # Leer el archivo html
    webpage = ''

    with open('website.html', 'r') as f:
        webpage = f.read()
    
    # Creamos el objeto soup con todo el HTML
    soup = BeautifulSoup(webpage, 'html.parser')
    
    anchor_tags = soup.find_all(name='a')
    
    print("Anchor Tags:\n")
    for tag in anchor_tags:
        print(f'{tag.getText():{20}} {tag.get("href")}')


