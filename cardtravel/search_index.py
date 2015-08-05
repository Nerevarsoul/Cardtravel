from haystack import indexes

from .models import Card


class CardIndex(indexes.SearchIndex, indexes.Indexable):
	name = indexes.CharField(document=True, use_template=True, model_attr='name')

	content_auto = indexes.EdgeNgramField(model_attr='name')

	def get_model(self):
        return Card

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


