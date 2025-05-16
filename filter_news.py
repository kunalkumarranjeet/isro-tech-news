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
        published = entry.published if 'published' in entry else ""

        # Check if any keyword is in title or summary (case-insensitive)
        if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in KEYWORDS):
            filtered_news.append({
                'title': title,
                'link': link,
                'summary': summary,
                'published': published
            })

    return filtered_news

if __name__ == "__main__":
    filtered_news = fetch_and_filter_news()  # assign returned list here
    
    if filtered_news:
        print(f"Found {len(filtered_news)} relevant news articles:")
        for article in filtered_news:
            print(f"- {article['title']}\n  Link: {article['link']}")
    else:
        print("No relevant news found.")

    # Build RSS feed XML content
    rss_content = '''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>ISRO & Tech News</title>
  <link>https://github.com/kunalkumaranjeet/isro-feed</link>
  <description>Filtered news feed for ISRO and tech updates</description>
'''

    for news_item in filtered_news:
        rss_content += f'''
    <item>
      <title>{news_item["title"]}</title>
      <link>{news_item["link"]}</link>
      <description>{news_item["summary"]}</description>
      <pubDate>{news_item["published"]}</pubDate>
    </item>
    '''

    rss_content += '''
</channel>
</rss>
'''

    # Save RSS XML file
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(rss_content)
