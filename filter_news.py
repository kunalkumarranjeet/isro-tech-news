import feedparser

# The Hindu Tech RSS feed URL
RSS_URL = "https://www.thehindu.com/sci-tech/technology/feeder/default.rss"

# Keywords to filter news about ISRO and tech
KEYWORDS = ['ISRO', 'space', 'technology', 'satellite', 'rocket']

def fetch_and_filter_news():
    feed = feedparser.parse(RSS_URL)
    filtered_news = []

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary if 'summary' in entry else ""
        link = entry.link

        # Check if any keyword is in title or summary (case-insensitive)
        if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in KEYWORDS):
            filtered_news.append({
                'title': title,
                'link': link
            })

    return filtered_news

if __name__ == "__main__":
    news = fetch_and_filter_news()
    if news:
        print(f"Found {len(news)} relevant news articles:")
        for article in news:
            print(f"- {article['title']}\n  Link: {article['link']}")
    else:
        print("No relevant news found.")
