from django.urls import path, include
# 登录后就直接创建帐号
# from .apis.wechatlogin import WeChatLoginAPIView
from .apis.wechatupdateinfo import WeChatUpdateInfoAPIView
# 需要先绑定再登录
from .apis.wechatbind import WeChatBindAPIView, WeChatLoginAPIView

urlpatterns = [
    path('login/', WeChatLoginAPIView.as_view(), name='wechat_login'),
    path('bind/', WeChatBindAPIView.as_view(), name='wechat_bind'),
    path('updateUserInfo/', WeChatUpdateInfoAPIView.as_view(), name="wechat_update_userinfo"),
]
