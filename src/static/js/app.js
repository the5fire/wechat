/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require) {
    var $ = require('jquery');
    var _ = require('underscore');
    var Backbone = require('backbone');
    var AppRouter = require('approuter');
    var UserModule = require('user');

    var User = UserModule.User;

    var g_user = new User();
    var appRouter = new AppRouter(g_user);
    g_user.fetch({
        success: function(model, resp, options){
            g_user = resp;
            Backbone.history.start({pustState: true});

            if(g_user === null || g_user.id === undefined) {
                // 跳转到登录页面
                appRouter.navigate('login', {trigger: true});
            } else if (appRouter.indexFlag == false){
                // 跳转到首页
                appRouter.navigate('index', {trigger: true});
            }
        },
    }); // 获取当前用户
});
