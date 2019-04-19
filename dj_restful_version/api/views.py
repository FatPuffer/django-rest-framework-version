from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from django.urls import reverse

from .models import Role, UserInfo


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


from rest_framework.parsers import FileUploadParser


class ParserView(APIView):
    # parser_classes = [FileUploadParser,]  # 该视图支持上传文件
    """
    JSONParser:表示只能解析content-type:application/json头
    {'name': 'fatpuffer', 'age': 18}
    
    FormParser:表示只能解析content-type:application/x-www-form-urlencoded头
    <QueryDict: {'name': ['fatpuffer'], 'age': ['22']}>
    """

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON格式数据
            a. content-type: application/json
            b. {"name":"fatpuffer", age:18}
        """
        print(request.data)
        print(request.data['name'])
        print(request.data['age'])
        return HttpResponse('用户信息')


import json


class RoleView(APIView):
    """自己实现序列化JSON"""
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all().values('id', 'title')
        roles = list(roles)
        # ensure_ascii=False：关闭自动编码，使其可以直接呈现中文汉字
        ret = json.dumps(roles, ensure_ascii=False)

        return HttpResponse()


from rest_framework import serializers


class UserInfoSerializer(serializers.Serializer):
    """继承序列化对象实现序列化"""
    # 获取choice选项中的编号
    aaa = serializers.CharField(source='user_type')
    # 获取choice选项中的值 get_字段名_display
    bbb = serializers.CharField(source='get_user_type_display')
    username = serializers.CharField()
    password = serializers.CharField()
    # 显示外键group表中的id和title字段
    gp = serializers.CharField(source="group.title")
    # SerializerMethodField：自定义显示，实现嵌套序列化
    rls = serializers.SerializerMethodField()

    # 自定义显示
    def get_rls(self, row):
        role_obj_list = row.roles.all()
        ret = []
        for item in role_obj_list:
            ret.append({"id": item.id, "title": item.title})
        return ret


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        user = UserInfo.objects.all()
        ser = UserInfoSerializer(instance=user, many=True)

        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

