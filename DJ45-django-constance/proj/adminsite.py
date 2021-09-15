from django.contrib import admin
from django.conf import settings
from django.apps import apps
from django.utils.text import capfirst
from django.urls import NoReverseMatch, reverse
from django.contrib.admin.apps import AdminConfig

from constance import config
# from .__version__ import VERSION
# proj_name += f' {VERSION}'


class AdminSite(admin.AdminSite):
    # site_header = config.SITE_NAME
    # site_title = config.SITE_NAME
    # index_title = config.SITE_NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_header = config.SITE_NAME
        self.site_title = config.SITE_NAME
        self.index_title = config.SITE_NAME

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
                'admin_url': None,
                'add_url': None,
            }
            if perms.get('change') or perms.get('view'):
                model_dict['view_only'] = not perms.get('change')
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                    # 添加下面一句
                    'sequence': getattr(apps.get_app_config(app_label), 'sequence', 0)
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # 修改下面排序功能，让 module 先按 sequence 属性排序，再按名称排序
        # Sort the apps alphabetically.
        # app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        app_list = sorted(app_dict.values(), key=lambda x: (x['sequence'], x['name'].lower()))

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().index(request, extra_context)


class DjtoolboxAdminConfig(AdminConfig):
    default_site = 'proj.adminsite.AdminSite'
