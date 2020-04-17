# Project # 7
# The program works with XML-file with information about books.

import xml.etree.ElementTree as ET

# Choosing a language of program.
print('Choose language/ Выберите язык.\n1) Englishs/ Английский язык;\n2) '
      'Russian/ Русский язык.')
language = input('Input number/ Введите цифру: ')

while True:
    if language == '1':
        import eng_local as lc

        break
    elif language == '2':
        import rus_local as lc

        break
    print('Choose language/ Выберите язык.\n1) Englishs/ Английский язык;\n2) '
          'Russian/ Русский язык.')
    language = input('Input number/ Введите цифру: ')

# Сreating a dictionary with information about books.
d_books = {}
catalog_of_books = ET.parse("books.xml")
root = catalog_of_books.getroot()
for book in root:
    d_books[book.attrib['id']] = [{feature.tag: str(feature.text).replace(
        '\n', '')} for feature in book]


def id_info(id):
    """
    Function that printing full information about book using the id of it.
    :param id: id of book
    :return: None
    """
    try:
        book = d_books[id]
    except KeyError:
        print(lc.TXT_INCORRECT_DATA)
    else:
        print('ID:', id)
        for features in d_books[id]:
            for feature in features.items():
                print(feature[0], ':', feature[1])


def isbn_info(isbn):
    """
    Function that printing full information about book using the isbn of it.
    :param isbn: isbn of book
    :return: None
    """
    for book in root.findall('Book'):
        if book.find('ISBN').text == isbn:
            return id_info(book.get('id'))


def count_same_years(year):
    """
    Function that calculates amount of books with given year of publishing.
    :param year: the year of publishing of the book
    :return: amount of books with given year of publishing
    """
    count = 0
    for year_of_publish in root.iter('Year_of_publishing'):
        if year_of_publish.text == year:
            count += 1
    return count


def average_price():
    """
    Function that calculates average price of book in each publisher and
     prints it.
    :return: None
    """
    publishers = {}
    for info in d_books.values():
        for feature in info:
            if 'Publisher' in feature:
                publisher = feature['Publisher']
            if 'Price' in feature:
                price = float(feature['Price'])
        if publisher not in publishers:
            publishers[publisher] = [price]
        else:
            publishers[publisher] = publishers[publisher] + [price]
    for info in publishers:
        print(info, ':', round(sum(publishers[info]) / len(publishers[info]), 2))


def the_most_expensive(publisher, year):
    """
    Function that displays information about the most expensive book(s) for
     a given publisher and year of publication.
    :param publisher: the publisher of books
    :param year: the year of publishing of the books
    :return: None
    """
    books = {}
    for book in root.findall('Book'):
        answer = False
        if book.find('Publisher').text == publisher:
            answer = True
        if book.find('Year_of_publishing').text == year:
            answer = True
        else:
            answer = False
        if answer:
            price = book.find('Price').text
            if price not in books:
                books[float(book.find('Price').text)] = [book.get('id')]
            else:
                books[float(book.find('Price').text)] = books[float(book.find(
                    'Price').text)] + [book.get('id')]
    prices = list(books.keys())
    prices.sort()
    if prices == []:
        print(lc.TXT_ERROR)
        return
    for book_id in books[prices[-1]]:
        id_info(book_id)


def main():
    while True:
        print('-' * 100)
        print(lc.TXT_MENU)
        number = input(lc.TXT_INPUT_NUMBER)
        print('-' * 100)
        if number == '1':
            id = input(lc.TXT_INPUT_ID)
            id_info(id)
        elif number == '2':
            isbn = input(lc.TXT_INPUT_ISBN)
            isbn_info(isbn)
        elif number == '3':
            year = input(lc.TXT_INPUT_YEAR)
            print(count_same_years(year))
        elif number == '4':
            average_price()
        elif number == '5':
            year = input(lc.TXT_INPUT_YEAR)
            publisher = input(lc.TXT_PUSBLISH_TITLE)
            the_most_expensive(publisher, year)
        elif number == '6':
            exit()
        else:
            print('-' * 100)
            print(lc.TXT_NUMBER_ERROR)


if __name__ == '__main__':
    main()
