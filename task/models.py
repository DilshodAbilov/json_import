from django.db import models
# Create your models here.

class Repository(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stars = models.BigIntegerField()
    forks = models.BigIntegerField()
    watchers = models.BigIntegerField()
    is_fork = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    primary_languages = models.CharField(max_length=150,null=True,blank=True)
    description = models.TextField(null = True, blank=True)
    created_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    lisense = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"

class Languages(models.Model):
    repository =    models.ForeignKey(Repository,on_delete=models.CASCADE,related_name="languages")
    name = models.CharField(max_length=200)
    size = models.BigIntegerField()

    def __str__(self):
        return self.name
