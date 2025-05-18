import feedparser
from datetime import datetime
from email.utils import parsedate_to_datetime, format_datetime
import pytz
import re

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
        if keyword_filter and not contains_keywords ​:contentReference[oaicite:0]{index=0}​
