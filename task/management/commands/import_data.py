import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.db import transaction
from task.models import Repository, Languages

class Command(BaseCommand):
    help = 'Imports JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file ')

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f'Invalid JSON format in: {json_file_path}'))
            return

        self.stdout.write(self.style.WARNING(f"Import started from {json_file_path}"))

        repositories = []
        languages = []

        for repo in data:
            try:
                repository = Repository(
                    owner=repo['owner'],
                    name=repo['name'],
                    stars=repo['stars'],
                    forks=repo['forks'],
                    watchers=repo['watchers'],
                    is_fork=repo['isFork'],
                    is_archived=repo['isArchived'],
                    primary_languages=repo.get('primaryLanguage'),
                    description=repo.get('description', ''),
                    created_at=parse_datetime(repo['createdAt']),
                    pushed_at=parse_datetime(repo['pushedAt']),
                    lisense=repo.get('license')
                )
                repositories.append(repository)
            except KeyError as e:
                self.stderr.write(self.style.ERROR(f'Missing key in repository: {e} in {repo}'))

        with transaction.atomic():
            Repository.objects.bulk_create(repositories, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"{len(repositories)} repositories saved."))

        for repo_index, repo in enumerate(data):
            repository = repositories[repo_index]
            for lang in repo.get('languages', []):
                try:
                    languages.append(Languages(
                        repository=repository,
                        name=lang['name'],
                        size=lang['size']
                    ))
                except KeyError as e:
                    self.stderr.write(self.style.ERROR(f'Missing key in language: {e} in {lang}'))

        with transaction.atomic():
            Languages.objects.bulk_create(languages, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"{len(languages)} languages saved."))

        self.stdout.write(self.style.SUCCESS("Import completed successfully!"))
