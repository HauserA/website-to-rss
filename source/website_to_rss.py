from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
from rfeed import Item, Feed, Guid
import boto3

S3_BUCKET = "website-to-rss-feed"

URL = "https://www.oth-regensburg.de/fakultaeten/informatik-und-mathematik/schwarzes-brett.html"

RSS_TITLE = "OTH Regensburg Fakultät Informatik - Schwarzes Brett"
RSS_LINK = "http://www.oth-regensburg.de"
RSS_DESCRIPTION = "RSS feed for: OTH Regensburg Fakultät Informatik - Schwarzes Brett"
RSS_AUTHOR = "Fakultät Informatik"
RSS_LANGUAGE = "de-DE"

s3_client = boto3.client("s3")


def article_to_item(article):
    return Item(
        title=article.h2.a.text.strip(),
        link=article.h2.a["href"],
        description=" ".join([x.text.strip() for x in article.find_all("p")]),
        author=RSS_AUTHOR,
        guid=Guid(article.h2.a["href"]),
        pubDate=datetime.strptime(article.h2.span.text[:-3], r"%d.%m.%Y"),
    )


def lambda_handler(event, context):

    print("Start lambda function")

    print(f"Start: Reading URL: {URL}")
    soup = BeautifulSoup(urlopen(URL).read(), "html.parser")
    print("Finished: Reading URL")

    articles = soup.find_all("div", class_="article")
    print(f"Found {len(articles)} articles")

    print("Start: Parsing articles")
    items = []
    twoWeeksAgo = datetime.now() - timedelta(days=14)
    for article in articles:
        rssItem = article_to_item(article)
        # only show articles that are less than 2 weeks old
        if rssItem.pubDate > twoWeeksAgo:
            items.append(rssItem)
    print("Finished: Parsing articles")
    print(f"There are {len(items)} RSS-Feed items which are less than 2 weeks old")

    print("Create Feed")
    feed = Feed(
        title=RSS_TITLE,
        link=RSS_LINK,
        description=RSS_DESCRIPTION,
        language=RSS_LANGUAGE,
        lastBuildDate=datetime.now(),
        items=items,
    )

    print("Write temporary file: rss.xml")
    with open("/tmp/rss.xml", mode="w", encoding="utf-8") as xml:
        xml.write(feed.rss())

    print(f"Upload file to S3: {S3_BUCKET}")
    response = s3_client.upload_file("/tmp/rss.xml", S3_BUCKET, "oth/rss.xml")
    print(f"S3 Response: {response}")

    print("End lambda function")


if __name__ == "__main__":
    lambda_handler({"job_name": "test"}, "")
