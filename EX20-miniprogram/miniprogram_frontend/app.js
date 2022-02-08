// app.js
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
          url: 'http://127.0.0.1:8000/miniprogram/login/',
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
