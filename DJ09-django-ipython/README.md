# Django 使用 ipython 命令行

## 添加步骤

    # 第一步：下载 django 扩展
    pip install django-extensions
     
    # 第二步：下载 ipython
    pip install ipython
     

    # 第三步：在django setting中设置 shell 默认环境
    SHELL_PLUS = 'ipython'  # 建议跟其他全局配置放置在一起
     
    # 最后，可以愉快的使用了
    python manage.py shell
