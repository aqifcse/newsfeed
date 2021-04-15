from django import forms
from portal.models import *
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget


class UserAuthForm(AuthenticationForm):

    error_messages = {
        "invalid_login": _("Incorrect username or password"),
        "invalid": _("Invalid user input!"),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if self.user_cache:
                    self.confirm_login_allowed(self.user_cache)
                else:
                    raise forms.ValidationError(
                        self.error_messages["invalid"],
                        code="invalid",
                    )

        return self.cleaned_data


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "subscribe"]
        widgets = {"jsonfield": JSONEditorWidget}


class EmailValidationOnForgotPassword(PasswordResetForm):

    error_messages = {
        "unregistered": _("The email is not registered. Please register"),
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(
                self.error_messages["unregistered"],
                code="unregistered",
            )

        return email


class ReadListForm(forms.ModelForm):
    COUNTRY_CHOICES = (
        ("", "All"),
        ("ae", "United Arab Emirates"),
        ("ar", "Argentina"),
        ("at", "Austria"),
        ("au", "Australia"),
        ("be", "Belgium"),
        ("bg", "Bulgaria"),
        ("br", "Brazil"),
        ("ca", "Canada"),
        ("ch", "Switzerland"),
        ("cn", "China"),
        ("co", "Colombia"),
        ("cu", "Cuba"),
        ("cz", "Czech Republic"),
        ("de", "Germany"),
        ("eg", "Egypt"),
        ("fr", "France"),
        ("gb", "United Kingdom"),
        ("gr", "Greece"),
        ("hk", "Hong Kong"),
        ("hu", "Hungary"),
        ("id", "Indonesia"),
        ("ie", "Ireland"),
        ("il", "Israel"),
        ("in", "India"),
        ("it", "Italy"),
        ("jp", "Japan"),
        ("kr", "South Korea"),
        ("lt", "Lithuania"),
        ("lv", "Latvia"),
        ("ma", "Morocco"),
        ("mx", "Mexico"),
        ("my", "Malaysia"),
        ("ng", "Nigeria"),
        ("nl", "Netherlands"),
        ("no", "Norway"),
        ("nz", "New Zealand"),
        ("ph", "Philippines"),
        ("pl", "Poland"),
        ("pt", "Portugal"),
        ("ro", "Romania"),
        ("rs", "Serbia"),
        ("ru", "Russia"),
        ("sa", "Saudi Arabia"),
        ("se", "Sweden"),
        ("sg", "Singapore"),
        ("si", "Slovenia"),
        ("sk", "Slovakia"),
        ("th", "Thailand"),
        ("tr", "Turkey"),
        ("tw", "Taiwan"),
        ("ua", "Ukraine"),
        ("us", "United States"),
        ("ve", "Venezuela"),
        ("za", "South Africa"),
    )

    SOURCE_CHOICES = (
        ("", "All"),
        ("abc-news", "ABC News"),
        ("abc-news-au", "ABC News (AU)"),
        ("aftenposten", "Aftenposten"),
        ("al-jazeera-english", "Al Jazeera English"),
        ("ansa", "ANSA.it"),
        ("argaam", "Argaam"),
        ("ars-technica", "Ars Technica"),
        ("ary-news", "Ary News"),
        ("associated-press", "Associated Press"),
        ("australian-financial-review", "Australian Financial Review"),
        ("axios", "Axios"),
        ("bbc-news", "BBC News"),
        ("bbc-sport", "BBC Sport"),
        ("bild", "Bild"),
        ("blasting-news-br", "Blasting News (BR)"),
        ("bleacher-report", "Bleacher Report"),
        ("bloomberg", "Bloomberg"),
        ("breitbart-news", "Breitbart News"),
        ("business-insider", "Business Insider"),
        ("business-insider-uk", "Business Insider (UK)"),
        ("buzzfeed", "Buzzfeed"),
        ("cbc-news", "CBC News"),
        ("cbs-news", "CBS News"),
        ("cnn", "CNN"),
        ("cnn-es", "CNN Spanish"),
        ("crypto-coins-news", "Crypto Coins News"),
        ("der-tagesspiegel", "Der Tagesspiegel"),
        ("die-zeit", "Die Zeit"),
        ("el-mundo", "El Mundo"),
        ("engadget", "Engadget"),
        ("entertainment-weekly", "Entertainment Weekly"),
        ("espn", "ESPN"),
        ("espn-cric-info", "ESPN Cric Info"),
        ("financial-post", "Financial Post"),
        ("focus", "Focus"),
        ("football-italia", "Football Italia"),
        ("fortune", "Fortune"),
        ("four-four-two", "FourFourTwo"),
        ("fox-news", "Fox News"),
        ("fox-sports", "Fox Sports"),
        ("globo", "Globo"),
        ("google-news", "Google News"),
        ("google-news-ar", "Google News (Argentina)"),
        ("google-news-au", "Google News (Australia)"),
        ("google-news-br", "Google News (Brasil)"),
        ("google-news-ca", "Google News (Canada)"),
        ("google-news-fr", "Google News (France)"),
        ("google-news-in", "Google News (India)"),
        ("google-news-is", "Google News (Israel)"),
        ("google-news-it", "Google News (Italy)"),
        ("google-news-ru", "Google News (Russia)"),
        ("google-news-sa", "Google News (Saudi Arabia)"),
        ("google-news-uk", "Google News (UK)"),
        ("goteborgs-posten", "Göteborgs-Posten"),
        ("gruenderszene", "Gruenderszene"),
        ("hacker-news", "Hacker News"),
        ("handelsblatt", "Handelsblatt"),
        ("ign", "IGN"),
        ("il-sole-24-ore", "Il Sole 24 Ore"),
        ("independent", "Independent"),
        ("infobae", "Infobae"),
        ("info-money", "InfoMoney"),
        ("la-gaceta", "La Gaceta"),
        ("la-nacion", "La Nacion"),
        ("la-repubblica", "La Repubblica"),
        ("le-monde", "Le Monde"),
        ("lenta", "Lenta"),
        ("lequipe", "L equipe"),
        ("les-echos", "Les Echos"),
        ("liberation", "Libération"),
        ("marca", "Marca"),
        ("mashable", "Mashable"),
        ("medical-news-today", "Medical News Today"),
        ("msnbc", "MSNBC"),
        ("mtv-news", "MTV News"),
        ("mtv-news-uk", "MTV News (UK)"),
        ("national-geographic", "National Geographic"),
        ("national-review", "National Review"),
        ("nbc-news", "NBC News"),
        ("news24", "News24"),
        ("new-scientist", "New Scientist"),
        ("news-com-au", "News.com.au"),
        ("newsweek", "Newsweek"),
        ("new-york-magazine", "New York Magazine"),
        ("next-big-future", "Next Big Future"),
        ("nfl-news", "NFL News"),
        ("nhl-news", "NHL News"),
        ("nrk", "NRK"),
        ("politico", "Politico"),
        ("polygon", "Polygon"),
        ("rbc", "RBC"),
        ("recode", "Recode"),
        ("reddit-r-all", "Reddit /r/all"),
        ("reuters", "Reuters"),
        ("rt", "RT"),
        ("rte", "RTE"),
        ("rtl-nieuws", "RTL Nieuws"),
        ("sabq", "SABQ"),
        ("spiegel-online", "Spiegel Online"),
        ("svenska-dagbladet", "Svenska Dagbladet"),
        ("t3n", "T3n"),
        ("talksport", "TalkSport"),
        ("techcrunch", "TechCrunch"),
        ("techcrunch-cn", "TechCrunch (CN)"),
        ("techradar", "TechRadar"),
        ("the-american-conservative", "The American Conservative"),
        ("the-globe-and-mail", "The Globe And Mail"),
        ("the-hill", "The Hill"),
        ("the-hindu", "The Hindu"),
        ("the-huffington-post", "The Huffington Post"),
        ("the-irish-times", "The Irish Times"),
        ("the-jerusalem-post", "The Jerusalem Post"),
        ("the-lad-bible", "The Lad Bible"),
        ("the-next-web", "The Next Web"),
        ("the-sport-bible", "The Sport Bible"),
        ("the-times-of-india", "The Times of India"),
        ("the-verge", "The Verge"),
        ("the-wall-street-journal", "The Wall Street Journal"),
        ("the-washington-post", "The Washington Post"),
        ("the-washington-times", "The Washington Times"),
        ("time", "Time"),
        ("usa-today", "USA Today"),
        ("vice-news", "Vice News"),
        ("wired", "Wired"),
        ("wired-de", "Wired.de"),
        ("wirtschafts-woche", "Wirtschafts Woche"),
        ("xinhua-net", "Xinhua Net"),
        ("ynet", "Ynet"),
    )
    keyword = forms.CharField(required=True)
    source = forms.ChoiceField(choices=SOURCE_CHOICES, required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=False)

    class Meta:
        model = ReadList
        fields = ["id", "keyword", "source", "country", "newsletter"]
