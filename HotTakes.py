import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from colorama import init, Fore

init(autoreset=True)

print(Fore.LIGHTBLACK_EX + "  _    _       _       _______    _                   ")
print(Fore.LIGHTBLACK_EX + " | |  | |     | |     |__   __|  | |                  ")
print(Fore.LIGHTBLACK_EX + " | |__| | ___ | |_ ______| | __ _| | ____ _  ___  ___ ")
print(Fore.LIGHTBLACK_EX + " |  __  |/ _ \\| __|______| |/ _` | |/ / _` |/ _ \\/ __|")
print(Fore.LIGHTBLACK_EX + " | |  | | (_) | |_       | | (_| |   < (_| |  __/\\__ \\")
print(Fore.LIGHTBLACK_EX + " |_|  |_|\\___/ \\__|      |_|\\__,_|_|\\_\\__,_|\\___||___/")
print(Fore.LIGHTBLACK_EX + "Author: github.com/poefsa\n")

print("Available continents:")
print("1. Asia")
print("2. Middle East")
print("3. Europe")
print("4. Africa")
print("5. Latin America\n")

continent_input = input("Type one of the above continents: ").strip().lower().replace(" ", "-")
url = f"https://www.npr.org/sections/{continent_input}"
headers = { "User-Agent": "Mozilla/5.0" }
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
top_headline = soup.select_one("h2.title a")
if top_headline:
    headline_text = top_headline.get_text(strip=True)
    article_url = top_headline.get("href")

    print("\nTop Headline:")
    print("- " + headline_text)
    print("Article URL:", article_url)
else:
    print("Couldn't find a headline. Try another continent.")
    exit()

def summarize_text_simple(text, max_sentences=5):
    clean_text = BeautifulSoup(text, "html.parser").get_text()
    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    if len(sentences) <= max_sentences:
        return clean_text
    word_counts = defaultdict(int)
    for sentence in sentences:
        words = re.findall(r'\w+', sentence.lower())
        for word in words:
            word_counts[word] += 1
    sentence_scores = {}
    for index, sentence in enumerate(sentences):
        words = re.findall(r'\w+', sentence.lower())
        score = sum(word_counts[word] for word in words)
        sentence_scores[index] = score
    top_indexes = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    top_indexes.sort()
    summary = ' '.join([sentences[i] for i in top_indexes])
    return summary

choice = input("\nWould you like a short summary of this article? (Y/N): ").strip().lower()
if choice == "y":
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")
    article_div = article_soup.find("div", id="storytext")
    if article_div:
        paragraphs = article_div.find_all("p")
        full_text = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        first_half = full_text[:len(full_text)//2]
        half_text = "\n".join(first_half)
        summary = summarize_text_simple(half_text)
        print("\n--- Summary ---")
        print(summary)
    else:
        print("Couldn't find article text.")
elif choice == "n":
    print("Okay, no summary shown.")
else:
    print("Invalid option entered.")