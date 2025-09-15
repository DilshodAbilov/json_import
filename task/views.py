from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractYear
from .models import Repository, Languages

@api_view(['GET'])
def top_languages_year(request):
    queryset = (
        Languages.objects
        .annotate(year=ExtractYear('repository__created_at'))
        .values('year', 'name')
        .annotate(count=Count('id'))
        .order_by('year', '-count')
    )

    result = {}
    temp = {}
    for item in queryset:
        year = item['year']
        if year not in temp:
            temp[year] = 0
        if temp[year] < 5:
            if year not in result:
                result[year] = []
            result[year].append({
                "language": item['name'],
                "count": item['count']
            })
            temp[year] += 1

    return Response(result)










# from django.db import connection
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# # Create your views here.
# @api_view(['GET'])
# def top_languages_year(request):
#     query = """
#         SELECT year, name, count FROM (
#             SELECT EXTRACT(YEAR FROM r.created_at) as year,l.name,
#                  COUNT(l.id) as count,
#                  ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM r.created_at) ORDER BY COUNT(l.id) DESC) as qator FROM task_languages l
#                  LEFT JOIN task_repository r on l.repository_id = r.id
#                  GROUP BY year, l.name
#             ) top_tillar
#         WHERE qator <= 5
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