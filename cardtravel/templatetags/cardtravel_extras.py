from django import template

from cardtravel.models import Card


register = template.Library()

@register.filter
def encode_url(cooked_url):
    return cooked_url.replace(' ', '_')

def card_sidebar():
        cards = Card.objects.all()
        countries = []
        series = []
        years = []
        for card in cards:
            if card.country not in countries:
                countries.append(card.country)
            if card.series not in series:
                series.append(card.series)
            if card.issued_on not in years:
                years.append(card.issued_on)
        countries.sort()
        series.sort()
        years.sort()
        args = {}
        args["countries"] = countries
        args["series"] = series
        args["years"] = years
        return args

register.inclusion_tag('cardtravel/preview/card_sidebar.html')(card_sidebar)


def paginate(paginate_objects):
    args = {}
    args["paginate_objects"] = paginate_objects
    return args



register.inclusion_tag('cardtravel/preview/pagination.html')(paginate)    