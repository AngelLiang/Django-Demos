# django 语言本地化（未完成）

## 准备工作

Windows下需要下载安装两个文件

- gettext-runtime-X.zip
- gettext-tools-X.zip

> X 是版本号，需要高于 0.15

http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies

## 添加步骤

一、中间件增加`django.middleware.locale.LocaleMiddleware`，并且它的顺序要靠前。

二、在`settings.py`中增加`LANGUAGES`和`LOCALE_PATHS`。


三、生成翻译文件，并且翻译
