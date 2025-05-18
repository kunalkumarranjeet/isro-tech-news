import feedparser
from datetime import datetime
from email.utils import parsedate_to_datetime, format_datetime
import pytz

# RSS Feeds
TECH_FEED = "https://www.thehindu.com/sci-tech/technology/feeder/default.rss"
WORLD_FEED = "https://www.thehindu.com/news/international/feeder/default.rss"

TECH_KEYWORDS = ["ISRO", "space", "tech", "technology"]
MAX_ITEMS = 5
IST = pytz.timezone("Asia/Kolkata")

def escape_xml(text):
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))

def contains_keywords(text, keywords):
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in keywords)

def is_today_ist(pub_dt):
    ist_now = datetime.now(IST)
    return pub_dt.astimezone(IST).date() == ist_now.date()

def fetch_filtered_entries(feed_url, keyword_filter=False):
    entries = []
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        try:
            pub_dt = parsedate_to_datetime(entry.published)
        except Exception:
            continue

        if not is_today_ist(pub_dt):
            continue

        if keyword_filter and not contains_keywords(entry.title + " " + entry.summary, TECH_KEYWORDS):
            continue

        entries.append(entry)

    return entries

def generate_rss(entries):
    now = format_datetime(datetime.utcnow())
    rss_items = ""

    for entry in entries[:MAX_ITEMS]:
        title = escape_xml(entry.title)
        description = escape_xml(entry.summary)
        pub_date = parsedate_to_datetime(entry.published)
        pub_date_formatted = format_datetime(pub_date)
        rss_items += (
            f"<item>\n"
            f"<title>{title}</title>\n"
            f"<link>{entry.link}</link>\n"
            f"<description>{description}</description>\n"
            f"<pubDate>{pub_date_formatted}</pubDate>\n"
            f"<guid>{entry.link}</guid>\n"
            f"</item>\n"
        )

    rss_feed = (
        '<?xml version="1.0" encoding="UTF-8" ?>\n'
        '<rss version="2.0">\n'
        '<channel>\n'
        '<title>ISRO, Tech &amp; World News - The Hindu</title>\n'
        '<link>https://kunalkumarranjeet.github.io/isro-tech-news/</link>\n'
        '<description>Auto-updated feed with ISRO, tech, and world news from The Hindu</description>\n'
        f'<lastBuildDate>{now}</lastBuildDate>\n'
        f'{rss_items}'
        '</channel>\n'
        '</rss>'
    )

    return rss_feed

def main():
    tech_entries = fetch_filtered_entries(TECH_FEED, keyword_filter=True)
    world_entries = fetch_filtered_entries(WORLD_FEED, keyword_filter=False)

    combined = tech_entries + world_entries
    combined.sort(key=lambda e: parsedate_to_datetime(e.published), reverse=True)

    rss_xml = generate_rss(combined)

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

if __name__ == "__main__":
    main()
