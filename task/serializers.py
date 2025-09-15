from rest_framework import serializers
from .models import Languages

class LanguageSerializer(serializers.Serializer):
    language = serializers.CharField()
    count = serializers.IntegerField()

class YearLanguagesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    top_languages = LanguageSerializer(many=True)
