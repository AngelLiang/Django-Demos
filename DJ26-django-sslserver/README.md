# django 使用 SSL 服务器

## 准备工作

浏览器导入 `cert/ca.p12` 证书到「受信任的根证书颁发机构」里。

双击 `cert/ca.p12` 文件，点击下一步直到下面的界面，选择「受信任的根证书颁发机构」，最后点击下一步直到完成。导入完成之后浏览器就不再显示安全警告。

![导入证书](screenshot/import.png)

## 快速开始

    pipenv install
    pipenv shell

    python manage.py runsslserver

    python manage.py runsslserver --certificate cert/ca-cert.pem --key cert/ca-key.pem

## 效果图

![登录页面](screenshot/login.png)
