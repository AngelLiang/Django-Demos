// pages/bind.js
const urls = require('../../urls.js');

Page({

    /**
     * 页面的初始数据
     */
    data: {
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    },


    formSubmit(e) {
        console.log('form发生了submit事件，携带数据为：', e.detail.value)
        let formData = e.detail.value;

        // 登录
        wx.login({
            success: res => {
            // 发送 res.code 到后台换取 openId, sessionKey, unionId
            wx.request({
                // url: 'http://127.0.0.1:8000/miniprogram/bind/',
                url: urls.bindUser,
                method: 'post',
                data: {
                    username: e.detail.value.username,
                    password: e.detail.value.password,
                    code: res.code
                },
                success: (res) => {
                    console.log(res)
                    if (res.data.success) {
                        wx.setStorageSync('token', res.data.token);
                        wx.navigateTo({
                            url: '../bindsucc/bindsucc'
                          })
                    }
                },
                fail: res => {
                    wx.setStorageSync('token', null);
                }
            })
            }
        })

      },
    
      formReset(e) {
        console.log('form发生了reset事件，携带数据为：', e.detail.value)
        this.setData({
          chosen: ''
        })
      }

})