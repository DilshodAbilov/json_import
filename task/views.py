from django.db.models import Count, F, Window
from django.db.models.functions import ExtractYear, RowNumber
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LanguagesSize

@api_view(['GET'])
def top_languages_year(request):
    queryset = LanguagesSize.objects.annotate(
        year=ExtractYear('repo__createdAt')
    ).values(
        'year', 'language__name'
    ).annotate(
        count=Count('repo')
    )

    queryset = queryset.annotate(
        row_number=Window(
            expression=RowNumber(),
            partition_by=[F('year')],
            order_by=F('count').desc()
        )
    ).filter(
        row_number__lte=5
    ).order_by('year', '-count')

    return Response(list(queryset))


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db.models import Count
# from django.db.models.functions import ExtractYear
# from .models import Repository, Language, LanguagesSize
#
# @api_view(['GET'])
# def top_languages_year(request):
#     queryset = (
#         LanguagesSize.objects
#         .annotate(year=ExtractYear('repo__createdAt'))
#         .values('year', 'language__name')
#         .annotate(count=Count('repo'))
#         .order_by('year', '-count')
#     )
#
#     result = {}
#     temp = {}
#     for item in queryset:
#         year = item['year']
#         lang_name = item['language__name']
#         if year not in temp:
#             temp[year] = 0
#         if temp[year] < 5:
#             if year not in result:
#                 result[year] = []
#             result[year].append({
#                 "language": lang_name,
#                 "count": item['count']
#             })
#             temp[year] += 1
#
#     return Response(result)











# from django.db import connection
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# # Create your views here.
# @api_view(['GET'])
# def top_languages_year(request):
#     query = """
#         SELECT year, name, count FROM (
#             SELECT
#                 EXTRACT(YEAR FROM r."createdAt") AS year,
#                 l.name,
#                 COUNT(ls.repo_id) AS count,
#                 ROW_NUMBER() OVER (
#                     PARTITION BY EXTRACT(YEAR FROM r."createdAt")
#                     ORDER BY COUNT(ls.repo_id) DESC
#                 ) AS rn
#             FROM task_languagessize ls
#             LEFT JOIN task_language l ON ls.language_id = l.id
#             LEFT JOIN task_repository r ON ls.repo_id = r.id
#             GROUP BY year, l.name
#         ) top_languages
#         WHERE rn <= 5
#         ORDER BY year, count DESC;
#     """
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         rows = cursor.fetchall()
#     result = {}
#     for year , name,count in rows:
#         year =int(year)
#         if year not in result:
#             result[year] = []
#         result[year].append({
#             "language":name,
#             "count":count
#         })
#     return Response(result)