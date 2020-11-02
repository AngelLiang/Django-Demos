// @ts-nocheck
import { ApplyPluginsType, dynamic } from 'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/node_modules/@umijs/runtime';
import { plugin } from './plugin';

const routes = [
  {
    "path": "/xadmin/login",
    "component": dynamic({ loader: () => import(/* webpackChunkName: 'layouts__UserLayout' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/layouts/UserLayout'), loading: require('@/components/PageLoading/index').default}),
    "routes": [
      {
        "name": "login",
        "path": "/xadmin/login",
        "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__UserLogin' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/UserLogin'), loading: require('@/components/PageLoading/index').default}),
        "exact": true
      }
    ]
  },
  {
    "path": "/xadmin/",
    "component": dynamic({ loader: () => import(/* webpackChunkName: 'layouts__SecurityLayout' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/layouts/SecurityLayout'), loading: require('@/components/PageLoading/index').default}),
    "routes": [
      {
        "path": "/xadmin/",
        "component": dynamic({ loader: () => import(/* webpackChunkName: 'layouts__BasicLayout' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/layouts/BasicLayout'), loading: require('@/components/PageLoading/index').default}),
        "authority": [
          "admin",
          "user"
        ],
        "routes": [
          {
            "name": "首页",
            "path": "/xadmin/index",
            "icon": "dashboard",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__DashBoard' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/DashBoard'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "path": "/xadmin/",
            "redirect": "/xadmin/index",
            "exact": true
          },
          {
            "name": "首页",
            "path": "/xadmin/index",
            "icon": "dashboard",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__DashBoard' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/DashBoard'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "权限",
            "icon": "smile",
            "path": "/xadmin/permission",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__PermissionList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/PermissionList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "组",
            "icon": "smile",
            "path": "/xadmin/group",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__GroupList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/GroupList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "用户",
            "icon": "smile",
            "path": "/xadmin/user",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__UserList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/UserList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "客户",
            "icon": "smile",
            "path": "/xadmin/customer",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__CustomerList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/CustomerList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "产品",
            "icon": "smile",
            "path": "/xadmin/product",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__ProductList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/ProductList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "订单",
            "icon": "smile",
            "path": "/xadmin/order",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__OrderList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/OrderList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "订单明细",
            "icon": "smile",
            "path": "/xadmin/order_item",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__AutoGenPage__OrderItemList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/AutoGenPage/OrderItemList'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "Tyadmin内置",
            "icon": "VideoCamera",
            "path": "/xadmin/sys",
            "routes": [
              {
                "name": "TyAdmin日志",
                "icon": "smile",
                "path": "/xadmin/sys/ty_admin_sys_log",
                "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__TyAdminSysLogList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/TyAdminSysLogList'), loading: require('@/components/PageLoading/index').default}),
                "exact": true
              },
              {
                "name": "TyAdmin验证",
                "icon": "smile",
                "path": "/xadmin/sys/ty_admin_email_verify_record",
                "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__TyAdminEmailVerifyRecordList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/TyAdminEmailVerifyRecordList'), loading: require('@/components/PageLoading/index').default}),
                "exact": true
              }
            ]
          },
          {
            "path": "/xadmin/account/change_password",
            "name": "修改密码",
            "hideInMenu": true,
            "icon": "dashboard",
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__ChangePassword' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/ChangePassword'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          },
          {
            "name": "Tyadmin内置",
            "icon": "VideoCamera",
            "path": "/xadmin/sys",
            "routes": [
              {
                "name": "TyAdmin日志",
                "icon": "smile",
                "path": "/xadmin/sys/ty_admin_sys_log",
                "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__TyAdminSysLogList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/TyAdminSysLogList'), loading: require('@/components/PageLoading/index').default}),
                "exact": true
              },
              {
                "name": "TyAdmin验证",
                "icon": "smile",
                "path": "/xadmin/sys/ty_admin_email_verify_record",
                "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__TyAdminBuiltIn__TyAdminEmailVerifyRecordList' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/TyAdminBuiltIn/TyAdminEmailVerifyRecordList'), loading: require('@/components/PageLoading/index').default}),
                "exact": true
              }
            ]
          },
          {
            "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__404' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/404'), loading: require('@/components/PageLoading/index').default}),
            "exact": true
          }
        ]
      },
      {
        "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__404' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/404'), loading: require('@/components/PageLoading/index').default}),
        "exact": true
      }
    ]
  },
  {
    "component": dynamic({ loader: () => import(/* webpackChunkName: 'p__404' */'F:/github/Django-Demos/DJ28-tyadmin_api_cli-demo/tyadmin/src/pages/404'), loading: require('@/components/PageLoading/index').default}),
    "exact": true
  }
];

// allow user to extend routes
plugin.applyPlugins({
  key: 'patchRoutes',
  type: ApplyPluginsType.event,
  args: { routes },
});

export { routes };
