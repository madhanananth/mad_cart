from rest_framework import serializers
from .models import SearchHistory


class SearchHistorySerializer(serializers.Serializer):

    model = SearchHistory
    fields = [ 'id','query','searched_at']