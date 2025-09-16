from django.contrib import admin
from .models import Repository,LanguagesSize,Language,Topic,TopicsStars
# Register your models here.
admin.site.register(Repository)
admin.site.register(Language)
admin.site.register(Topic)
admin.site.register(TopicsStars)
admin.site.register(LanguagesSize)
