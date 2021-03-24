from wordcloud import WordCloud, STOPWORDS
from scraping_Truspilot import scraping_trustpilot_category


def wordcloud_generate(list_comments: str):
    Dict_wordcloud = dict()

    comment_words = '' 

    for val in list_comments:
        # typecaste each val to string
        val = str(val) 

        # split the value 
        tokens = val.split()

        # Converts each token into lowercase 
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

            comment_words += " ".join(tokens)+" "

    worldcloud = WordCloud().process_text(comment_words)

    worldcloud_sorted = dict(sorted(worldcloud.items(), key=lambda item: item[1], reverse=True))
    worldcloud_sorted = worldcloud_sorted.items()

    wordcloud_comments = list(worldcloud_sorted)[:6]

    for w in wordcloud_comments:
        Dict_wordcloud[w[0]] = w[1]

    return Dict_wordcloud
