import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.db import transaction
from task.models import Repository, Language, Topic, LanguagesSize, TopicsStars


class Command(BaseCommand):
    help = 'Imports JSON file with repositories, languages, and topics'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file')

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

        for repo_data in data:
            try:
                repository = Repository(
                    owner=repo_data['owner'],
                    name=repo_data['name'],
                    stars=repo_data.get('stars', 0),
                    forks=repo_data.get('forks', 0),
                    watchers=repo_data.get('watchers', 0),
                    isFork=repo_data.get('isFork', False),
                    isArchived=repo_data.get('isArchived', False),
                    description=repo_data.get('description', ''),
                    createdAt=parse_datetime(repo_data['createdAt']),
                    pushedAt=parse_datetime(repo_data['pushedAt']),
                    license=repo_data.get('license'),
                )

                primary_lang_name = repo_data.get('primaryLanguage')
                if primary_lang_name:
                    primary_lang_obj, _ = Language.objects.get_or_create(name=primary_lang_name)
                    repository.primaryLanguage = primary_lang_obj

                repositories.append(repository)
            except KeyError as e:
                self.stderr.write(self.style.ERROR(f'Missing key in repository: {e}'))

        with transaction.atomic():
            Repository.objects.bulk_create(repositories, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"{len(repositories)} repositories saved."))

        languages_size_objs = []
        seen_pairs = set()

        for repo_index, repo_data in enumerate(data):
            repository = repositories[repo_index]
            for lang in repo_data.get('languages', []):
                lang_name = lang.get('name')
                lang_size = lang.get('size', 0)
                if not lang_name:
                    continue
                pair_key = (repository.name, lang_name)
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                lang_obj, _ = Language.objects.get_or_create(name=lang_name)
                languages_size_objs.append(LanguagesSize(
                    repo=repository,
                    language=lang_obj,
                    size=lang_size
                ))

        with transaction.atomic():
            LanguagesSize.objects.bulk_create(languages_size_objs, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"{len(languages_size_objs)} language-size records saved."))

        topics_stars_objs = []
        for repo_index, repo_data in enumerate(data):
            repository = repositories[repo_index]
            for topic in repo_data.get('topics', []):
                topic_name = topic.get('name')
                topic_stars = topic.get('stars', 0)
                if not topic_name:
                    continue
                topic_obj, _ = Topic.objects.get_or_create(name=topic_name)
                topics_stars_objs.append(TopicsStars(
                    repo=repository,
                    topic=topic_obj,
                    stars=topic_stars
                ))

        with transaction.atomic():
            TopicsStars.objects.bulk_create(topics_stars_objs, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"{len(topics_stars_objs)} topics-stars records saved."))

        self.stdout.write(self.style.SUCCESS("Import completed successfully!"))
