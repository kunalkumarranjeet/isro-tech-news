import feedparser
from datetime import datetime
from email.utils import format_datetime

FEED_URL = "https://www.thehindu.com/sci-tech/technology/feeder/default.rss"
KEYWORDS = ["ISRO", "space", "tech", "technology"]
MAX_ITEMS = 5

def contains_keywords(text, keywords):
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in keywords)

def generate_rss(items):
    now = format_datetime(datetime.utcnow())
    rss_items = ""
    
    for entry in items[:MAX_ITEMS]:
        pub_date = format_datetime(datetime(*entry.published_parsed[:6]))
        rss_items += f"""
        <item>
            <title>{entry.title}</title>
            <link>{entry.link}</link>
            <description>{entry.summary}</description>
            <pubDate>{pub_date}</pubDate>
            <guid>{entry.link}</guid>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>ISRO & Tech News - The Hindu</title>
    <link>https://kunalkumarranjeet.github.io/isro-tech-news/</link>
    <description>Auto-updated news feed about ISRO and tech from The Hindu</description>
    <lastBuildDate>{now}</lastBuildDate>
    {rss_items}
  </channel>
</rss>"""
    return rss_feed

def main():
    feed = feedparser.parse(FEED_URL)
    filtered_entries = [entry for entry in feed.entries if contains_keywords(entry.title + " " + entry.summary, KEYWORDS)]
    
    rss_xml = generate_rss(filtered_entries)

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

if __name__ == "__main__":
    main()
