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


class WeChatLoginAPIView(views.APIView):
    permission_classes = []

    def post(self, request):
        code = request.data.get('code', None)
        if not code:
            return Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        url = get_wechat_login_code_url(code)
        resp = requests.get(url)

        openid = ''
        session_key = ''
        if resp.status_code != 200:
            return Response({"error": "WeChat server return error, please try again later"})
        json = resp.json()
        # print(json)
        if "errcode" in json:
            return Response({"error": json["errmsg"]})
        openid = json['openid']
        session_key = json['session_key']

        if not session_key:
            return Response({"error": "WeChat server doesn't return session key"})
        if not openid:
            return Response({"error": "WeChat server doesn't return openid"})

        # v1
        # user, _ = User.objects.get_or_create(username=openid)
        # wechataccount, _ = WeChatAccount.objects.get_or_create(openId=openid, user=user)
        # wechataccount.openId = openid
        # wechataccount.session_key = session_key
        # wechataccount.unionId = json.get('unionid', '')
        # wechataccount.save()

        # v2
        wechataccount, _ = WeChatAccount.objects.get_or_create(openId=openid)
        if not wechataccount.user:
            user, _ = User.objects.get_or_create(username=openid)
            wechataccount.user = user
        else:
            user = wechataccount.user
        wechataccount.session_key = session_key
        wechataccount.unionId = json.get('unionid', '')
        wechataccount.save()

        token, created = Token.objects.get_or_create(user=user)
        if created:
            return Response({'token': token.key, 'user_id': user.id})
        Token.objects.get(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id
        })
