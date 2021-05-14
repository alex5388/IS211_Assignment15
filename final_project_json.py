# Scrape website
book_isbn = '9781449372620'
r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(book_isbn))
soup = BeautifulSoup(r.content, 'html.parser')


# Parse JSON data
data = json.loads(soup.text)
try:
    title = data['items'][0]['volumeInfo']['title']
    print(title)
except KeyError:
    print('***TITLE COULD NOT BE FOUND***')

try:
    author = data['items'][0]['volumeInfo']['authors'][0]
    print(author)
except KeyError:
    print('***AUTHOR COULD NOT BE FOUND***')

try:
    page_count = data['items'][0]['volumeInfo']['pageCount']
    print(page_count)
except KeyError:
    print('***PAGE COUNT COULD NOT BE FOUND***')

try:
    average_rating = data['items'][0]['volumeInfo']['averageRating']
    print(average_rating)
except KeyError:
    print('***AVERAGE RATING COULD NOT BE FOUND***')
