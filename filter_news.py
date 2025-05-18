import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime, format_datetime

import pytz  # Needs to be installed via pip

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
        rss_items += f"""
        <item>
            <title>{entry.title}</title>
            <link>{entry.link}</link>
            <description>{entry.summary}</description>
            <pubDate>{pub_date_formatted}</pubDate>
            <guid>{entry.link}</guid>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version=
