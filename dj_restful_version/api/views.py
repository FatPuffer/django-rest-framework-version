from django.http import JsonResponse, HttpResponse
from rest_framework .views import APIView
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning
from django.urls import reverse

from .models import Role, UserInfo, UserGroup


# ----------------------------------------------------------
# http://127.0.0.1:8000/api/v1/userinfo/
# 自定义版本管理

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


# ----------------------------------------------------------
# 版本控制：http://127.0.0.1:8000/api/v1/userinfo/

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


# ----------------------------------------------------------
# 解析器

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


# ----------------------------------------------------------
#  自定义序列化

import json


class RoleView(APIView):
    """自己实现序列化JSON"""
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all().values('id', 'title')
        roles = list(roles)
        # ensure_ascii=False：关闭自动编码，使其可以直接呈现中文汉字
        ret = json.dumps(roles, ensure_ascii=False)

        return HttpResponse()


# ----------------------------------------------------------
#  继承 Serializer 类序列化


from rest_framework import serializers


# class UserInfoSerializer(serializers.Serializer):
#     """继承序列化对象实现序列化"""
#     # 获取choice选项中的编号
#     aaa = serializers.CharField(source='user_type')
#     # 获取choice选项中的值 get_字段名_display
#     bbb = serializers.CharField(source='get_user_type_display')
#     username = serializers.CharField()
#     password = serializers.CharField()
#     # 显示外键group表中的id和title字段
#     gp = serializers.CharField(source="group.title")
#     # SerializerMethodField：自定义显示，实现嵌套序列化
#     rls = serializers.SerializerMethodField()
#
#     # 自定义显示
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({"id": item.id, "title": item.title})
#         return ret


# ----------------------------------------------------------
#  继承 ModelSerializer 类序列化


# class UserInfoSerializer(serializers.ModelSerializer):
#     # 自定义字段
#     type_name = serializers.CharField(source='get_user_type_display')
#     # 外键字段处理
#     rls = serializers.SerializerMethodField()
#     # 获取外键对象__str__属性返回值，默认返回外键对象id
#     group = serializers.StringRelatedField()
#
#     class Meta:
#         model = UserInfo
#         # fields = "__all__"
#         fields = ["id", "user_type", "type_name", "username", "password", "group", "roles", "rls"]
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({"id": item.id, "title": item.title})
#         return ret


# class UserInfoSerializer(serializers.ModelSerializer):
#     # lookup_url_kwarg：url中的正则名
#     # lookup_field：根据哪个字段生成url
#     group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')
#
#     class Meta:
#         model = UserInfo
#         fields = "__all__"
#         depth = 1


# ----------------------------------------------------------
#  HyperlinkedIdentityField 实现关联表的url生成
# 不常用


class UserInfoSerializer(serializers.ModelSerializer):
    # lookup_url_kwarg：url中的正则名
    # lookup_field：根据哪个字段生成url
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = UserInfo
        fields = "__all__"
        depth = 1


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        user = UserInfo.objects.all()
        # 使用HyperlinkedIdentityField时序列化对象必须加context={"request": request}
        ser = UserInfoSerializer(instance=user, many=True, context={"request": request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = "__all__"


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj = UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


# ----------------------------------------------------------
# 验证数据

class CheckValidator:
    """自定义验证规则"""

    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = "标题必须以{}开头".format(self.base)
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        # 执行之前调用，serializer_field是当前字段对象
        pass


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={"required": "标题不能为空"}, validators=[CheckValidator('Fatpuffer'),])


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['title'])
        else:
            print(serializer.errors)

        return HttpResponse('提交数据')
