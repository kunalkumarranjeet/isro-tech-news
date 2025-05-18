import feedparser
from datetime import datetime
from email.utils import parsedate_to_datetime, format_datetime
import pytz  # install via pip

FEED_URL = "https://www.thehindu.com/sci-tech/technology/feeder/default.rss"
KEYWORDS = ["ISRO", "space", "tech", "technology"]
MAX_ITEMS = 5

IST = pytz.timezone("Asia/Kolkata")

def contains_keywords(text, keywords):
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in keywords)

def is_today_ist(pub_dt):
    ist_now = datetime.now(IST)
    return pub_dt.astimezone(IST).date() == ist_now.date()

def generate_rss(items):
    now = format_datetime(datetime.utcnow())
    rss_items = ""

    for entry in items[:MAX_ITEMS]:
        pub_date = parsedate_to_datetime(entry.published)
        pub_date_formatted = format_datetime(pub_date)
        rss_items += (
            f"<item>\n"
            f"<title>{entry.title}</title>\n"
            f"<link>{entry.link}</link>\n"
            f"<description>{entry.summary}</description>\n"
            f"<pubDate>{pub_date_formatted}</pubDate>\n"
            f"<guid>{entry.link}</guid>\n"
            f"</item>\n"
        )

    rss_feed = (
        '<?xml version="1.0" encoding="UTF-8" ?>\n'
        '<rss version="2.0">\n'
        '<channel>\n'
        '<title>ISRO & Tech News - The Hindu</title>\n'
        '<link>https://kunalkumarranjeet.github.io/isro-tech-news/</link>\n'
        '<description>Auto-updated news feed about ISRO and tech from The Hindu</description>\n'
        f'<lastBuildDate>{now}</lastBuildDate>\n'
        f'{rss_items}'
        '</channel>\n'
        '</rss>'
    )

    return rss_feed

def main():
    feed = feedparser.parse(FEED_URL)
    filtered_entries = []

    for entry in feed.entries:
        pub_dt = parsedate_to_datetime(entry.published)
        if is_today_ist(pub_dt) and contains_keywords(entry.title + " " + entry.summary, KEYWORDS):
            filtered_entries.append(entry)

    rss_xml = generate_rss(filtered_entries)

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

if __name__ == "__main__":
    main()
