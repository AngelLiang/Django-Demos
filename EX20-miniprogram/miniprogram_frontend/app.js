// app.js
const wxApiInterceptors = require('./wxApiInterceptors');
var regeneratorRuntime = require('./runtime'); // 需要用到async的地方都要引入这个文件，同时需要打开es6转es5
const config = require('./config.js');
const urls = require('./urls.js');

App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        wx.request({
          url: urls.login,
          method: 'post',
          data: {
            code: res.code
          },
          success: (res) => {
            console.log(res)
            // 没有绑定帐号，则会跳转到绑定页面
            if(!res.data.success) {
              wx.navigateTo({
                url: '../bind/bind'
              })
            }

            wx.setStorageSync('token', res.data.token);
          },
          fail: res => {
            wx.setStorageSync('token', null);
          }
        })
      }
    })
  },
  globalData: {
    userInfo: null
  }
})


wx.newWx = wxApiInterceptors({
  request: {
    async request(params) {
      console.log(params)
      if (params.header === undefined) {
        params.header = {};
      }
      let token = wx.getStorageSync('token');
      if (!token) {
        // 登录
        wx.login({
          success: res => {
            // 发送 res.code 到后台换取 openId, sessionKey, unionId
            if (res.code) {
              console.log(res)
              //发起网络请求
              wx.request({
                url: config.loginUrl,
                method: 'post',
                data: {
                  code: res.code
                },
                success: (res) => { 
                  console.log(res)

                  // 没有绑定帐号，则会跳转到绑定页面
                  if(!res.data.success) {
                    wx.navigateTo({
                      url: '../bind/bind'
                    })
                  }

                  wx.setStorageSync('token', res.data.token);
                },
                fail: res => {
                  wx.setStorageSync('token', null);
                }
              })
            } else {
              let msg = '登录失败！'
              console.log(msg + res.errMsg)
              wx.showToast({
                title: msg,
                icon: 'error',
                duration: 2000
              })
            }
          }
        })

        wx.setStorageSync('token', token);
      }
      params.header.Authorization = `Token ${token}`
      return params;
    },
  },
}, true);
