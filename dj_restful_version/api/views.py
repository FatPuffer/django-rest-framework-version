from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from rest_framework.request import Request
from rest_framework.versioning import BaseVersioning


class ParamVersion(object):

    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version


class UsersView(APIView):

    versioning_class = ParamVersion

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('用户列表')

