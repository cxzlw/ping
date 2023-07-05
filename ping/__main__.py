import os
import sys
import httpx
from bs4 import BeautifulSoup


def google():  # google
    sitemap_url = os.getenv("SITEMAP")
    resp = httpx.get(f"https://google.com/ping?sitemap={sitemap_url}")
    print(f"Google: {resp.status_code}")
    if not resp.is_success:
        print(f"Google: {resp.text}")


def index_now():  # bing, yandex
    host = os.getenv("HOST")
    sitemap_url = os.getenv("SITEMAP")
    api_key = os.getenv("INDEX_NOW_KEY")
    api_key_url = os.getenv("INDEX_NOW_KEY_URL")
    sitemap = httpx.get(sitemap_url)
    soup = BeautifulSoup(sitemap.content, "xml")
    urls = []
    for x in soup.find_all("loc"):
        urls.append(x.string)
    resp = httpx.post("https://www.bing.com/IndexNow",
                      json={
                          "host": host,
                          "key": api_key,
                          "keyLocation": api_key_url,
                          "urlList": urls
                      })
    print(f"Index Now: {resp.status_code}")
    if not resp.is_success:
        print(f"Index Now: {resp.text}")


if __name__ == '__main__':
    args = set(sys.argv)

    if "--google" in args:
        google()
    if "--index-now" in args:
        index_now()
