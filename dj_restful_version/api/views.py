from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from django.urls import reverse


# class ParamVersion(object):
#
#     def determine_version(self, request, *args, **kwargs):
#         version = request.query_params.get('version')
#         return version
#
#
# class UsersView(APIView):
#
#     versioning_class = ParamVersion
#
#     def get(self, request, *args, **kwargs):
#         print(request.version)
#         return HttpResponse('用户列表')


# class UsersView(APIView):
#
#     versioning_class = QueryParameterVersioning
#
#     def get(self, request, *args, **kwargs):
#         print(request.version)
#         return HttpResponse('用户列表')

class UsersView(APIView):

    def get(self, request, *args, **kwargs):
        # 获取版本
        print(request.version)

        # 获取处理版本的对象
        print(request.versioning_scheme)

        # 反向生成 URL （基于 rest framework）
        url = request.versioning_scheme.reverse(viewname='xxx', request=request)
        print(url)

        # 反向生成 URL （基于 Django）
        url2 = reverse(viewname='xxx', kwargs={'version': 2})
        print(url2)

        return HttpResponse('用户列表')
