from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils import timezone as tz

# COUNTRY_CHOICES = [
#     ("all", "All"),
#     ("ae", "United Arab Emirates"),
#     ("ar", "Argentina"),
#     ("at", "Austria"),
#     ("au", "Australia"),
#     ("be", "Belgium"),
#     ("bg", "Bulgaria"),
#     ("br", "Brazil"),
#     ("ca", "Canada"),
#     ("ch", "Switzerland"),
#     ("cn", "China"),
#     ("co", "Colombia"),
#     ("cu", "Cuba"),
#     ("cz", "Czech Republic"),
#     ("de", "Germany"),
#     ("eg", "Egypt"),
#     ("fr", "France"),
#     ("gb", "United Kingdom"),
#     ("gr", "Greece"),
#     ("hk", "Hong Kong"),
#     ("hu", "Hungary"),
#     ("id", "Indonesia"),
#     ("ie", "Ireland"),
#     ("il", "Israel"),
#     ("in", "India"),
#     ("it", "Italy"),
#     ("jp", "Japan"),
#     ("kr", "South Korea"),
#     ("lt", "Lithuania"),
#     ("lv", "Latvia"),
#     ("ma", "Morocco"),
#     ("mx", "Mexico"),
#     ("my", "Malaysia"),
#     ("ng", "Nigeria"),
#     ("nl", "Netherlands"),
#     ("no", "Norway"),
#     ("nz", "New Zealand"),
#     ("ph", "Philippines"),
#     ("pl", "Poland"),
#     ("pt", "Portugal"),
#     ("ro", "Romania"),
#     ("rs", "Serbia"),
#     ("ru", "Russia"),
#     ("sa", "Saudi Arabia"),
#     ("se", "Sweden"),
#     ("sg", "Singapore"),
#     ("si", "Slovenia"),
#     ("sk", "Slovakia"),
#     ("th", "Thailand"),
#     ("tr", "Turkey"),
#     ("tw", "Taiwan"),
#     ("ua", "Ukraine"),
#     ("us", "United States"),
#     ("ve", "Venezuela"),
#     ("za", "South Africa"),
# ]

# SOURCE_CHOICES = [
#     ("all", "All"),
#     ("abc-news", "ABC News"),
#     ("abc-news-au", "ABC News (AU)"),
#     ("aftenposten", "Aftenposten"),
#     ("al-jazeera-english", "Al Jazeera English"),
#     ("ansa", "ANSA.it"),
#     ("argaam", "Argaam"),
#     ("ars-technica", "Ars Technica"),
#     ("ary-news", "Ary News"),
#     ("associated-press", "Associated Press"),
#     ("australian-financial-review", "Australian Financial Review"),
#     ("axios", "Axios"),
#     ("bbc-news", "BBC News"),
#     ("bbc-sport", "BBC Sport"),
#     ("bild", "Bild"),
#     ("blasting-news-br", "Blasting News (BR)"),
#     ("bleacher-report", "Bleacher Report"),
#     ("bloomberg", "Bloomberg"),
#     ("breitbart-news", "Breitbart News"),
#     ("business-insider", "Business Insider"),
#     ("business-insider-uk", "Business Insider (UK)"),
#     ("buzzfeed", "Buzzfeed"),
#     ("cbc-news", "CBC News"),
#     ("cbs-news", "CBS News"),
#     ("cnn", "CNN"),
#     ("cnn-es", "CNN Spanish"),
#     ("crypto-coins-news", "Crypto Coins News"),
#     ("der-tagesspiegel", "Der Tagesspiegel"),
#     ("die-zeit", "Die Zeit"),
#     ("el-mundo", "El Mundo"),
#     ("engadget", "Engadget"),
#     ("entertainment-weekly", "Entertainment Weekly"),
#     ("espn", "ESPN"),
#     ("espn-cric-info", "ESPN Cric Info"),
#     ("financial-post", "Financial Post"),
#     ("focus", "Focus"),
#     ("football-italia", "Football Italia"),
#     ("fortune", "Fortune"),
#     ("four-four-two", "FourFourTwo"),
#     ("fox-news", "Fox News"),
#     ("fox-sports", "Fox Sports"),
#     ("globo", "Globo"),
#     ("google-news", "Google News"),
#     ("google-news-ar", "Google News (Argentina)"),
#     ("google-news-au", "Google News (Australia)"),
#     ("google-news-br", "Google News (Brasil)"),
#     ("google-news-ca", "Google News (Canada)"),
#     ("google-news-fr", "Google News (France)"),
#     ("google-news-in", "Google News (India)"),
#     ("google-news-is", "Google News (Israel)"),
#     ("google-news-it", "Google News (Italy)"),
#     ("google-news-ru", "Google News (Russia)"),
#     ("google-news-sa", "Google News (Saudi Arabia)"),
#     ("google-news-uk", "Google News (UK)"),
#     ("goteborgs-posten", "Göteborgs-Posten"),
#     ("gruenderszene", "Gruenderszene"),
#     ("hacker-news", "Hacker News"),
#     ("handelsblatt", "Handelsblatt"),
#     ("ign", "IGN"),
#     ("il-sole-24-ore", "Il Sole 24 Ore"),
#     ("independent", "Independent"),
#     ("infobae", "Infobae"),
#     ("info-money", "InfoMoney"),
#     ("la-gaceta", "La Gaceta"),
#     ("la-nacion", "La Nacion"),
#     ("la-repubblica", "La Repubblica"),
#     ("le-monde", "Le Monde"),
#     ("lenta", "Lenta"),
#     ("lequipe", "L equipe"),
#     ("les-echos", "Les Echos"),
#     ("liberation", "Libération"),
#     ("marca", "Marca"),
#     ("mashable", "Mashable"),
#     ("medical-news-today", "Medical News Today"),
#     ("msnbc", "MSNBC"),
#     ("mtv-news", "MTV News"),
#     ("mtv-news-uk", "MTV News (UK)"),
#     ("national-geographic", "National Geographic"),
#     ("national-review", "National Review"),
#     ("nbc-news", "NBC News"),
#     ("news24", "News24"),
#     ("new-scientist", "New Scientist"),
#     ("news-com-au", "News.com.au"),
#     ("newsweek", "Newsweek"),
#     ("new-york-magazine", "New York Magazine"),
#     ("next-big-future", "Next Big Future"),
#     ("nfl-news", "NFL News"),
#     ("nhl-news", "NHL News"),
#     ("nrk", "NRK"),
#     ("politico", "Politico"),
#     ("polygon", "Polygon"),
#     ("rbc", "RBC"),
#     ("recode", "Recode"),
#     ("reddit-r-all", "Reddit /r/all"),
#     ("reuters", "Reuters"),
#     ("rt", "RT"),
#     ("rte", "RTE"),
#     ("rtl-nieuws", "RTL Nieuws"),
#     ("sabq", "SABQ"),
#     ("spiegel-online", "Spiegel Online"),
#     ("svenska-dagbladet", "Svenska Dagbladet"),
#     ("t3n", "T3n"),
#     ("talksport", "TalkSport"),
#     ("techcrunch", "TechCrunch"),
#     ("techcrunch-cn", "TechCrunch (CN)"),
#     ("techradar", "TechRadar"),
#     ("the-american-conservative", "The American Conservative"),
#     ("the-globe-and-mail", "The Globe And Mail"),
#     ("the-hill", "The Hill"),
#     ("the-hindu", "The Hindu"),
#     ("the-huffington-post", "The Huffington Post"),
#     ("the-irish-times", "The Irish Times"),
#     ("the-jerusalem-post", "The Jerusalem Post"),
#     ("the-lad-bible", "The Lad Bible"),
#     ("the-next-web", "The Next Web"),
#     ("the-sport-bible", "The Sport Bible"),
#     ("the-times-of-india", "The Times of India"),
#     ("the-verge", "The Verge"),
#     ("the-wall-street-journal", "The Wall Street Journal"),
#     ("the-washington-post", "The Washington Post"),
#     ("the-washington-times", "The Washington Times"),
#     ("time", "Time"),
#     ("usa-today", "USA Today"),
#     ("vice-news", "Vice News"),
#     ("wired", "Wired"),
#     ("wired-de", "Wired.de"),
#     ("wirtschafts-woche", "Wirtschafts Woche"),
#     ("xinhua-net", "Xinhua Net"),
#     ("ynet", "Ynet"),
# ]


class User(AbstractUser):
    subscribe = models.BooleanField(
        default=False,
        help_text="This will enlist you to newsletter feature. You will get newsletter emails on latest news updates(within every 15 minutes). To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class NewsReader(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.headline)


class NewsBody(models.Model):
    news = models.ForeignKey(NewsReader, on_delete=models.CASCADE)
    thumbnail = models.URLField()
    source_of_news = models.CharField(max_length=100, null=True, blank=True)
    country_of_news = models.CharField(max_length=100, null=True, blank=True)
    original_news_source_link = models.URLField()

    published_at = models.DateTimeField(default=tz.now)


# class Country(models.Model):
#     country_name = models.CharField(max_length=50)  # , choices=COUNTRY_CHOICES)

#     def __str__(self):
#         return self.country_name


# class Source(models.Model):
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     source_name = models.CharField(max_length=50)  # , choices=SOURCE_CHOICES)

#     def __str__(self):
#         return self.source_name


class ReadList(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    country = models.CharField(
        max_length=50, null=True, blank=True
    )  # ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    source = models.CharField(
        max_length=50, null=True, blank=True
    )  # ForeignKey(Source, on_delete=models.SET_NULL, null=True)

    top_headlines_url = models.URLField()
    full_stories_url = models.URLField()

    newsletter = models.BooleanField(
        default=False,
        help_text="Checking this box will send you newsletters to your email id about the latest news updates(within every 15 minutes) based on this readlist. To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(default=tz.now)

    slug = models.SlugField(max_length=40)

    def __str__(self):
        return str(self.keyword)

    def slug(self):
        return slugify(self.id)

    class Meta:
        verbose_name = "ReadList"
        verbose_name_plural = "ReadLists"
