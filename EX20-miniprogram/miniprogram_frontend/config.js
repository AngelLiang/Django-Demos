/**
描述：接口地址统一配置，本地，测试服务器，正式服务器 ，登录地址
 */

var bizlogic = {
	// 是否是本地
	isLocal: true,
	// 是否是正式
	isFormal: false, // isLocal:false 时才有效

	// 本地测试地址 
	localTest: 'http://127.0.0.1:8000',
	// 本地登录测试地址 
	localTest_login: 'http://127.0.0.1:8000/miniprogram/onLogin/',

	// 测试服务器地址 
	serverTest: '',
	// 测试服务器登录地址 
	serverTest_login: '',

	// 正式服务器接口地址
	serverFormal: '',
	// 正式服务器登录接口
	serverFormal_login: ''
};
var serverUrl = '',
	loginUrl = '';

// 判断是否是本地
if (bizlogic.isLocal == true) {
	serverUrl = bizlogic.localTest;
	loginUrl = bizlogic.localTest_login;
} else {
	serverUrl = bizlogic.isFormal ? bizlogic.serverFormal : bizlogic.serverTest;
	loginUrl = bizlogic.isFormal ? bizlogic.serverFormal_login : bizlogic.serverTest_login;
};


module.exports = {
	serverUrl: serverUrl,
	loginUrl: loginUrl
};