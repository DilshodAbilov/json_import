from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Repository(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stars = models.BigIntegerField(default=0)
    forks = models.BigIntegerField(default=0)
    watchers = models.BigIntegerField(default=0)
    isFork = models.BooleanField(default=False)
    isArchived = models.BooleanField(default=False)

    languages = models.ManyToManyField(Language, through="LanguagesSize", related_name="repositories")
    topics = models.ManyToManyField(Topic, through="TopicsStars", related_name="repositories")

    primaryLanguage = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name="primary_repos")

    description = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(null=True, blank=True)
    pushedAt = models.DateTimeField(null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class LanguagesSize(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    size = models.BigIntegerField()

    class Meta:
        unique_together = ('repo', 'language')

    def __str__(self):
        return f"{self.repo.name} - {self.language.name} ({self.size})"


class TopicsStars(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    stars = models.BigIntegerField()

    class Meta:
        unique_together = ('repo', 'topic')

    def __str__(self):
        return f"{self.repo.name} - {self.topic.name} ({self.stars} stars)"
