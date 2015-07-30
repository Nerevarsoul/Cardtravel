from django.contrib.sitemaps import Sitemap
from .models import Card, Trade


class CardSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Card.objects.all()


class TradeSitemap(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Trade.objects.all()