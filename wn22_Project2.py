from xml.sax import parseString
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results():
    """
    Write a function that creates a BeautifulSoup object on "search_results.html". Parse
    through the object and return a list of tuples containing book titles, authors, and ratings 
    (ratings is the number of ratings, not the average rating) in the format given below. Make sure to strip()
    any newlines cast ratings to an int so we can sort on it later.

    [('Book title 1', 'Author 1','Ratings 1',), ('Book title 2', 'Author 2', 'Ratings 2')...]
    """
    
    # create the soup ~
    with open("search_results.html", "r") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "lxml")

    # find title
    titles = soup.find_all("a", class_="bookTitle")

    # find author
    authors = []
    miniauthors = soup.find_all("span", itemprop="author")
    for author in miniauthors:
        other = author.find("a", class_="authorName")
        authors.append(other)

    # find ratings
    ratings  = []
    miniratings = soup.find_all("span", class_="minirating")
    for rate in miniratings:
        new = (rate.text)[18:-8]
        ratings.append(int(new.replace(",", "")))

    # create tuple
    output = []
    for i in range(len(titles)):
        output.append((titles[i].text.strip(), authors[i].text, ratings[i]))

    return output


def get_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=david+sedaris&qid=". Parse through the object and return a list of
    URLs for each of the first five books in the search using the following format:

    ['https://www.goodreads.com/book/show/4137.Me_Talk_Pretty_One_Day?from_search=true&from_srp=true&qid=SXEzoop0e2&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and, and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    # create beautifulsoup object ~
    url = "https://www.goodreads.com/search?q=david+sedaris&qid="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # return the first five urls and create tuple
    links = []
    minilinks = soup.find_all('a', class_="bookTitle")[:5]
    for link in minilinks:
        href = link.get('href')
        current_url = "https://www.goodreads.com"
        absolute_url = current_url + href
        links.append(absolute_url)
    
    return links


def get_book_summary(book_html):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given an HTML file of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, number 
    of pages, book rating, and review count. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages, book rating, review count)

    When there is more than one auther listed, you want only the first author.
    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title, number of pages, and rating.
    """
    
    # create the soup ~
    with open(book_html, "r") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "lxml")
    
    # get title, author, pages, rating, and review count
    book_title = soup.find("h1", id="bookTitle")
    book_author = soup.find("a", class_="authorName")
    num_pages = soup.find("span", itemprop="numberOfPages")
    book_rating = soup.find("span", itemprop="ratingValue")
    review_count = soup.find(itemprop="ratingCount").get("content")

    # create tuple
    output = [book_title.text.strip(), book_author.text, num_pages.text, book_rating.text.strip(), review_count]
    
    return output


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2021"
    page in "best_books_2021.html". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "Beautiful World, Where Are You", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2021, then you should append 
    ("Fiction", "Beautiful World, Where Are You", "https://www.goodreads.com/choiceawards/best-fiction-books-2021") 
    to your list of tuples.

    Don't forget to be append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/choiceawards/best-fiction-books-2021". rather than "/choiceawards/best-fiction-books-2021"
    """

    # create the soup ~
    with open(filepath, "r") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "lxml")

    # category section
    category = []
    minicategory = soup.find_all("h4", class_="category__copy")
    for i in range(0, len(minicategory)):
        category.append(minicategory[i].text)

    # book titles section
    book = []
    for title in soup.find_all("img", class_="category__winnerImage"):
        book_title = title.get("alt")
        book.append(book_title)

    # url section
    url = []
    test = soup.find_all('div', class_="category clearFix")
    for link in test:
        href = link.find("a")["href"]
        current_url = "https://www.goodreads.com"
        absolute_url = current_url + href
        url.append(absolute_url)

    # create tuple
    output = []
    for i in range(len(category)):
        output.append((category[i].strip(), book[i], url[i]))

    return output



# DO LATER ------------------------------------------------------------------------------------------------------------------------->
def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), 
    sorts the tuples in ascending order by rating ratings,
    writes the data to a csv file, 
    and saves it to the passed filename.

    The first row of the csv should contain "Book Title","Author Name","Ratings"
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name,Ratings
    Book1,Author1,Ratingss1
    Book2,Author2,Ratings2
    Book3,Author3,Ratings3

    In order of least ratings to most ratings.
    ......

    This function should not return anything.
    """
    pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass


class TestCases(unittest.TestCase):

    # call get_links() and save it to a static variable: search_urls

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() and save to a local variable
        search_titles = get_titles_from_search_results()

        # check that the number of titles extracted is correct (20 titles)
        total_titles = 20
        message = "the titles are not equal"
        # self.assertEqual(search_titles, total_titles)

        # check that the variable you saved after calling the function is a list

        # check that each item in the list is a tuple
        
        # check that the first book, author, and ratings tuple is correct (open search_results.html and find it)

        # check that the last title is correct (open search_results.html and find it)
        pass
    
    def test_get_links(self):
        # check that TestCases.search_urls is a list

        # check that the length of TestCases.search_urls is correct (5 URLs)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        pass

    def test_get_book_summary(self):
        # the list of webpages you want to pass in one by one into get_book_summary
        # all of these are stores in the book_summary_html_files folder
        html_list = ['book_summary_html_files/Me Talk Pretty One Day by David Sedaris.html',
                     'book_summary_html_files/David Sedaris - 14 CD Boxed Set by David Sedaris.html',
                     'book_summary_html_files/SantaLand Diaries by David Sedaris.html',
                     'book_summary_html_files/Dress Your Family in Corduroy and Denim by David Sedaris.html',
                     'book_summary_html_files/David Sedaris_ Live For Your Listening Pleasure by David Sedaris.html']
        # create an empty list
    
        # for i in html_list:
        
        # check that the number of book summaries is correct (5)
        
            # check that each item in the list is a tuple

            # check that each tuple has 5 elements

            # check that the first two elements in the tuple are string
     
            # check that the third and fifth element in the tuple, i.e. pages and review count are ints
           
            # check that the fourth element in the tuple, i.e. rating is a float
         
        # check that the first book in the search has 272 pages

        # check that the last book has 4.35 rating

        # check that the third book as a reviw count of 539
        pass
    
    def test_summarize_best_books(self):
        # call summarize_best_books on best_books_2021.html and save it to a variable

        # check that we have the right number of best books (17)
 
            # assert each item in the list of best books is a tuple

            # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "Beautiful World, Where Are You", 'https://www.goodreads.com/choiceawards/best-fiction-books-2021'

        # check that the last tuple is made up of the following 3 strings: 'Middle Grade & Children's', 'Daughter of the Deep', 'https://www.goodreads.com/choiceawards/best-childrens-books-2021'

        pass
    
    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable

        # call write csv on the variable you saved
        
        # read in the csv that you wrote

        # check that there are 21 lines in the csv

        # check that the header row is correct

        # check that the next row is Harry Potter: A History of Magic,British Library,13153

        # check that the last row is "Harry Potter and the Sorcerer's Stone (Harry Potter, #1)",J.K. Rowling,7003900
        pass


if __name__ == '__main__':
    # extra_credit("extra_credit.html")
    unittest.main(verbosity=2)



