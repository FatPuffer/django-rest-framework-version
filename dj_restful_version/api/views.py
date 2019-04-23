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
        # viewname：url中name属性
        # kwargs：字典形式传参给url正则匹配内容
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
# HyperlinkedIdentityField 实现关联表的url生成
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
        # 1.实例化，一般是将数据封装到对象：__new__ , __init__
        # many=True，接下来执行ListSerializer对象的构造方法
        # many=False，接下来执行GroupSerializer对象的构造方法
        ser = GroupSerializer(instance=obj, many=False)
        # 2.调用对象的data属性
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)


# ----------------------------------------------------------
# 验证数据

# class CheckValidator:
#     """自定义验证规则"""
#
#     def __init__(self, base):
#         self.base = base
#
#     def __call__(self, value):
#         if not value.startswith(self.base):
#             message = "标题必须以{}开头".format(self.base)
#             raise serializers.ValidationError(message)
#
#     def set_context(self, serializer_field):
#         # 执行之前调用，serializer_field是当前字段对象
#         pass
#
#
# class UserGroupSerializer(serializers.Serializer):
#     title = serializers.CharField(error_messages={"required": "标题不能为空"}, validators=[CheckValidator('Fatpuffer'),])
#
#
# class UserGroupView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserGroupSerializer(data=request.data)
#         if serializer.is_valid():
#             print(serializer.validated_data['title'])
#         else:
#             print(serializer.errors)
#
#         return HttpResponse('提交数据')


# ----------------------------------------------------------
# 使用钩子方法验证单个数据


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={"required": "标题不能为空"})

    def validate_title(self, value):
        from rest_framework import exceptions
        if not value.startswith('Fat'):
            message = "标题必须以{}开头".format('Fat')
            raise exceptions.ValidationError(message)
            # return message
        return value


    """
    # 对多个字段进行验证
    def validate(self, attrs):
        # arrrs是数据组成的字典
    
        # 判断linux的数是否在linux分类
        if "linux" in attrs.get('title') and attrs['category_post'] == 2:
            return attrs
        else:
            raise serializers.ValidationError("图书与分类不一致")
    """


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['title'])
        else:
            print(serializer.errors)

        return HttpResponse('提交数据')


# ----------------------------------------------------------
# 分页
# 1.分页，看第n页，每页显示n条数据


from api.utils.serializers.pager import PagerSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# class MyPageNumberPagination(PageNumberPagination):
#     """
#         继承PageNumberPagination并扩展分页
#         http://127.0.0.1:8000/api/v1/pageer1/?page=2&size=3
#     """
#     page_size = 2  # 每页显示多少个
#     max_page_size = 5  # 每页显示最大值，防止一次性获取数据过大，导致数据库崩溃
#
#     ?page=1&size=3
#     page_query_param = 'page'  # 查询参数 page=1
#     page_size_query_param = 'size'  # 查询参数 size=3
#
#
# class Pager1View(APIView):
#     """
#         http://127.0.0.1:8000/api/v1/pageer1/?page=4
#     """
#     def get(self, request, *args, **kwargs):
#
#         # 获取所有数据
#         roles = Role.objects.all()
#
#         # 创建分页对象
#         pg = PageNumberPagination()
#         # pg = MyPageNumberPagination()
#
#         # 在数据库中获取分页数据
#         page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
#
#         # 对分页数据进行序列化
#         ser = PagerSerializer(instance=page_roles, many=True)
#
#         # 提供上一页下一页连接，以及数据总数量
#         # page = pg.get_paginated_response(ser.data)
#         # return Response(page.data)
#
#         return Response(ser.data)


# ----------------------------------------------------------
# 分页
# 2.分页，在n个位置，向后查看n条数据
#
# from rest_framework.pagination import LimitOffsetPagination
#
#
# class MyPageNumberPagination(LimitOffsetPagination):
#     """
#         继承LimitOffsetPagination并扩展分页
#         http://127.0.0.1:8000/api/v1/pageer1/?offset=0&limit=3
#     """
#     default_limit = 2  # 默认每页显示数量
#     max_limit = 5  # 每页显示最大值，防止一次性获取数据过大，导致数据库崩溃
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#
#
# class Pager1View(APIView):
#     """
#         http://127.0.0.1:8000/api/v1/pageer1/?offset=0
#     """
#     def get(self, request, *args, **kwargs):
#
#         # 获取所有数据
#         roles = Role.objects.all()
#
#         # 创建分页对象
#         pg = LimitOffsetPagination()
#
#         # 在数据库中获取分页数据
#         page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
#
#         # 对分页数据进行序列化
#         ser = PagerSerializer(instance=page_roles, many=True)
#
#         # 提供上一页下一页连接，以及数据总数量
#         # page = pg.get_paginated_response(ser.data)
#         # return Response(page.data)
#
#         return Response(ser.data)


# ----------------------------------------------------------
# 分页
# 3.加密分页，上一页和下一页：在分页时记录最大页码和最小页码，实现跳转时查询，避免随着页码越大查询数据越多从而导致加载数据缓慢问题

from rest_framework.pagination import CursorPagination


class MyPageNumberPagination(CursorPagination):
    """
        继承CursorPagination并扩展分页
        http://127.0.0.1:8000/api/v1/pageer1/?cursor=cD0y
    """
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'  # 排序规则

    page_size_query_param = 3  # 每页显示个数

    max_page_size = 5  # 一页最多显示多少个


class Pager1View(APIView):
    """
        加密分页，不能直接输入页码
    """
    def get(self, request, *args, **kwargs):

        # 获取所有数据
        roles = Role.objects.all()

        # 创建分页对象
        # pg = CursorPagination()
        pg = MyPageNumberPagination()

        # 在数据库中获取分页数据
        page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对分页数据进行序列化
        ser = PagerSerializer(instance=page_roles, many=True)

        # 提供上一页下一页连接，以及数据总数量
        page = pg.get_paginated_response(ser.data)
        return Response(page.data)
