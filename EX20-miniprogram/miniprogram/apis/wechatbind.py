from django.conf import settings

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

import requests

from django.contrib.auth import get_user_model
User = get_user_model()

from ..models.wechataccount import WeChatAccount
from .utils import get_wechat_login_code_url


def fetch_openid(code):
    url = get_wechat_login_code_url(code)
    resp = requests.get(url)

    if resp.status_code != 200:
        return None, "WeChat server return error, please try again later"
    json = resp.json()
    # print(json)
    if "errcode" in json:
        return None, json["errmsg"]
    openid = json['openid']
    session_key = json['session_key']

    if not session_key:
        return None, "WeChat server doesn't return session key"
    if not openid:
        return None, "WeChat server doesn't return openid"
    return json, None


class WeChatBindAPIView(views.APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None:
            return Response({"error": "没有填写用户名"})
        if password is None:
            return Response({"error": "没有填写密码"})

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "没有该用户名"})
        if not user.check_password(password):
            return Response({"error": "密码不正确"})

        code = request.data.get('code', None)
        if not code:
            return Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        json, errMsg = fetch_openid(code)
        if errMsg:
            return Response({"error": errMsg})

        openid = json['openid']
        session_key = json['session_key']

        wechataccount, _ = WeChatAccount.objects.get_or_create(openId=openid)
        wechataccount.user = user
        wechataccount.save()
        if wechataccount.user:
            user = wechataccount.user
            token, created = Token.objects.get_or_create(user=user)
            if created:
                return Response({'token': token.key, 'user_id': user.id})
            Token.objects.get(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'user_id': user.id
            })
        return Response({
            'success': False,
            'error': {
                'devMsg': '没有绑定帐号。',
                'userMsg': '请先绑定帐号。',
            }
        })


class WeChatLoginAPIView(views.APIView):
    permission_classes = []

    def post(self, request):
        code = request.data.get('code', None)
        if not code:
            return Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        json, errMsg = fetch_openid(code)
        if errMsg:
            return Response({"error": errMsg})
        openid = json['openid']

        wechataccount, _ = WeChatAccount.objects.get_or_create(openId=openid)
        if wechataccount.user:
            user = wechataccount.user
            token, created = Token.objects.get_or_create(user=user)
            if created:
                return Response({'token': token.key, 'user_id': user.id})
            Token.objects.get(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'user_id': user.id
            })
        return Response({
            'success': False,
            'error': {
                'devMsg': '没有绑定帐号。',
                'userMsg': '请先绑定帐号。',
            }
        })
