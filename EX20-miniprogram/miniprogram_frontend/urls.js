const config = require('./config.js');

module.exports = {
    login: config.loginUrl,
    // 绑定用户
    bindUser: config.serverUrl + "/miniprogram/bind/",
    // 更新信息
	updateUserInfo: config.serverUrl + "/miniprogram/updateUserInfo/"
};