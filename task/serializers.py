from rest_framework import serializers
from .models import Repository, Language, Topic, LanguagesSize, TopicsStars

class LanguageSerializer(serializers.ModelSerializer):
    size = serializers.IntegerField(source='languagessize_set.size', read_only=True)

    class Meta:
        model = Language
        fields = ['name', 'size']

class TopicSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(source='topicsstars_set.stars', read_only=True)

    class Meta:
        model = Topic
        fields = ['name', 'stars']

class RepositorySerializer(serializers.ModelSerializer):
    primaryLanguage = serializers.StringRelatedField()
    languages = LanguageSerializer(source='languagessize_set', many=True)
    topics = TopicSerializer(source='topicsstars_set', many=True)

    class Meta:
        model = Repository
        fields = [
            'owner', 'name', 'stars', 'forks', 'watchers',
            'isFork', 'isArchived', 'primaryLanguage',
            'description', 'createdAt', 'pushedAt', 'license',
            'languages', 'topics'
        ]

class YearLanguagesSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    top_languages = LanguageSerializer(many=True)
