from haystack import indexes

from .models import UserProfile, Card, WishList, Collection, Trade


class CardIndex(indexes.SearchIndex, indexes.Indexable):
	name = indexes.CharField(document=True, use_template=True, model_attr='name')

	def get_model(self):
        return Card




