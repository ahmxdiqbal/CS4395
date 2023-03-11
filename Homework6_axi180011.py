import pickle                                       # importing packages
import re
import requests
from urllib import request
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter


def extract_terms(pages):
    stop_words = set(stopwords.words('english'))        # declaring stopwords
    all_tokens = []

                                                        # creating a list of all the words in all the files
    for page in pages:                                  # going through each file(page)
        tokens = []
        for sents in pages:
            for sent in sents:
                sent = sent.split()
                for word in sent:
                    tokens.append(word)

                                                        # processing those words
        tokens = [t for t in tokens if t not in stop_words and t.isalpha()]
        tokens = [t.lower() for t in tokens]
        all_tokens.extend(tokens)                       # adding words of each page to the total list

                                                        # counting and sorting terms, then picking 33 most common terms
    token_counts = Counter(all_tokens)
    sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
    top_terms = []
    for i in range(33):
        top_terms.append(sorted_tokens[i][0])
        print(top_terms[i])

    return top_terms


def clean(text, counter):
                                                        # cleaning the raw text
    text = "".join(text)
    text = re.sub(r'\t', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'^\s.*\n?', '', text, flags=re.MULTILINE)
    text = text.lower()

    sents = sent_tokenize(text)                         # senctence tokenizing the cleaned text

                                                        # writing the cleaned text to a file
    filename = "file" + str(counter) + ".txt"
    with open(filename, 'w') as f:
        for sent in sents:
            try:
                f.write(sent + "\n")
            except:
                pass

    return sents


def scrape_text(urls):
    counter = 0
    pages = []

    for url in urls:
        req = request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'})

        try:                                            # getting the full html of the page
            html = request.urlopen(req)
        except:
            continue

                                                        # creating a soup object
        soup = BeautifulSoup(html, features="html.parser")

        for script in soup(["script", "style"]):        # kill all script and style elements
            script.extract()

        text = soup.get_text()                          # extracting raw text

        pages.append(clean(text, counter))              # calling clean function on raw text, and appending file contents to list of pages

        counter += 1

    return pages


def web_crawler(url):
                                                        # getting contents of webpage
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")

    urls = []
    counter = 0
                                                        # write urls to a file
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):                 # finding all links on page
            if len(urls) >= 15:
                break
            href = link.get('href')
                                                        # completing all relative link
            if href.startswith("/") or href.startswith("#"):
                href = url + href
                                                        # filtering out wikipedia links
            if 'wiki' not in href:
                urls.append(href)
                f.write(str(href) + '\n\n')
                counter += 1

    return urls


if __name__ == '__main__':
    starter_url = "https://en.wikipedia.org/wiki/Football"
    urls = web_crawler(starter_url)
    pages = scrape_text(urls)
    extract_terms(pages)

                                                        # picked 10 relevant terms
    top_10 = ["ball", "soccer", "england", "world", "cup", "football", "game", "players", "fifa", "nations"]

                                                        # built knowledge base
    knowledge_base = {
        "ball": "a hollow sphere that is kicked by the players in a football game",
        "soccer": "a game played by two teams of eleven players with a round ball that may not be touched with the hands or arms during play except by the "
                  "goalkeepers. The object of the game is to score goals by kicking or heading the ball into the opponents' goal",
        "england": "an island country in northwestern europe in which modern football was invented",
        "world": "the earth, together with all of its countries, peoples, and natural features",
        "cup": "an ornamental trophy in the form of a cup, usually made of gold or silver and having a stem and two handles, awarded as a prize in a competition",
        "football": "the term used to refer to soccer outside the united states of america",
        "game": "a period of play of soccer between two teams, ending in a definite result",
        "players": "the people taking part in a soccer game",
        "fifa": "a federation that is the governing body for many international soccer tournaments",
        "nations": "refers to the organized political entities within a set of recognized borders, many of which play soccer with teams consisting of their "
                   "citizens against each other"
    }

                                                        # pickling knowledge base
    with open('knowledge_base.pickle', 'wb') as file:
        pickle.dump(knowledge_base, file)




