from .models import Customer
from haystack import indexes


class CustomerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='product_title')

    def get_model(self):
        return Customer

    def index_queryset(self, using=None):
        return self.get_model().objects.all()