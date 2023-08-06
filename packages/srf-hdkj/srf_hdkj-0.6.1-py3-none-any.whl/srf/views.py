# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Callable, Any

from sanic.log import logger
from sanic.response import json, HTTPResponse
from sanic.views import HTTPMethodView
from ujson import dumps
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from srf.exceptions import APIException, ValidationException
from srf.permissions import BasePermission
from srf.status import RuleStatus, HttpStatus
from srf.utils import run_awaitable

__all__ = ('BaseView', 'APIView')


class BaseView:
    """只实现路由分发的基础视图
    在使用时应当开放全部路由 ALL_METHOD
    app.add_route('/test', BaseView.as_view(), 'test', ALL_METHOD)
    如需限制路由则在其他地方注明
    app.add_route('/test', BaseView.as_view(), 'test', ALL_METHOD)
    注意以上方法的报错是不可控的
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def as_view(cls, **initkwargs):
        # 返回的响应方法闭包
        async def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            self.app = request.app
            return await self.dispatch(request, *args, **kwargs)

        view.view_class = cls
        # view.API_DOC_CONFIG = class_kwargs.get('API_DOC_CONFIG')  # 未来的API文档配置属性+
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__name__ = cls.__name__
        return view

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs

    async def dispatch(self, request, *args, **kwargs):
        """分发路由"""
        request.user = None
        method = request.method.lower()

        if not hasattr(self, method):
            return HTTPResponse('405请求方法错误', status=405)
        handler = getattr(self, method, None)
        return await run_awaitable(handler, request, *args, **kwargs)


class APIView(BaseView):
    """通用视图，可以基于其实现增删改查，提供权限套件"""
    authentication_classes = ()
    permission_classes = ()
    is_transaction = True

    async def dispatch(self, request, *args, **kwargs):
        """分发路由"""
        method = request.method.lower()

        if not hasattr(self, method):
            return self.json_response(msg='发生错误：未找到%s方法' % method, errcode=400)
        handler = getattr(self, method, None)
        try:
            is_success = await self.initial(request, *args, **kwargs)
            if is_success is False:
                return self.json_response(msg='缺少token或token失效', errcode=4002)
            if self.is_transaction:
                async with in_transaction():
                    response = await run_awaitable(handler, request=request, *args, **kwargs)
            else:
                response = await run_awaitable(handler, request=request, *args, **kwargs)
        except Exception as exc:
            # logger.error(f'--捕获未知错误--{exc}')
            response = self.handle_exception(exc)
        return response

    def get_exception_handler(self):
        """
        Returns the exception handler that this view uses.
        """
        return getattr(self.app.ctx, "srf_exception_handler", None)

    def handle_exception(self, exc: APIException):
        exception_handler = self.get_exception_handler()
        if exception_handler is None:
            self.raise_uncaught_exception(exc)
        else:
            response = exception_handler(exc)
            response.exception = True
            return response

    def raise_uncaught_exception(self, exc):
        # if self.app.config.DEBUG:
        #     request = self.request
        #     renderer_format = getattr(request.accepted_renderer, 'format')
        #     use_plaintext_traceback = renderer_format not in ('html', 'api', 'admin')
        #     request.force_plaintext_errors(use_plaintext_traceback)
        raise exc

    def json_response(self, data=None, msg="请求成功", errcode=200,
                      http_status=HttpStatus.HTTP_200_OK):
        """
        Json 相应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :param status: 前台约定状态，供前台判断是否成功
        :param http_status: Http响应数据
        :return:
        """
        if data is None:
            data = {}
        response_body = {
            'data': data,
            'code': errcode,
            'errcode': errcode,
            'errmsg': msg
        }
        return json(body=response_body, status=http_status, dumps=dumps)

    def success_json_response(self, data=None, msg="Success", **kwargs):
        """
        快捷的成功的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        return self.json_response(data=data, msg=msg, errcode=200)

    def error_json_response(self, data=None, msg="Fail", **kwargs):
        """
        快捷的失败的json响应体
        :param data: 返回的数据主题
        :param msg: 前台提示字符串
        :return: json
        """
        return self.json_response(data=data, msg=msg, errcode=400)

    def get_authenticators(self):
        """
        实例化并返回此视图可以使用的身份验证器列表
        """
        from srf.authentication import BaseAuthenticate
        authentications = []
        for auth in self.authentication_classes:
            if isinstance(auth, BaseAuthenticate):
                authentications.append(auth)
            else:
                authentications.append(auth())
        return authentications

    async def check_authentication(self, request):
        """
        检查权限 查看是否拥有权限，并在此处为Request.User 赋值
        :param request: 请求
        :return:
        """
        result = True
        for authenticators in self.get_authenticators():
            is_success = await authenticators.authenticate(request, self)
            if is_success is False:
                result = False
        return result

    def get_permissions(self):
        """
        实例化并返回此视图所需的权限列表
        """
        permissions = []
        for permission in self.permission_classes:
            if isinstance(permission, BasePermission):
                permissions.append(permission)
            else:
                permissions.append(permissions)
        return permissions

    async def check_permissions(self, request):
        """
        检查是否应允许该请求，如果不允许该请求，
        则在 has_permission 中引发一个适当的异常。
        :param request: 当前请求
        :return:
        """
        for permission in self.get_permissions():
            await permission.has_permission(request, self)

    async def check_object_permissions(self, request, obj):
        """
        检查是否应允许给定对象的请求, 如果不允许该请求，
        则在 has_object_permission 中引发一个适当的异常。
            常用于 get_object() 方法
        :param request: 当前请求
        :param obj: 需要鉴权的模型对象
        :return:
        """
        for permission in self.get_permissions():
            await permission.has_object_permission(request, self, obj)

    async def check_throttles(self, request):
        """
        检查范围频率。
        则引发一个 APIException 异常。
        :param request:
        :return:
        """
        pass

    async def initial(self, request, *args, **kwargs):
        """
        在请求分发之前执行初始化操作，用于检查权限及检查基础内容
        """
        is_success = await self.check_authentication(request)

        await self.check_permissions(request)
        await self.check_throttles(request)
        return is_success
