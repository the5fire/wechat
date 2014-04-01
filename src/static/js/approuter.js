/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var _ = require('underscore');
    var Backbone = require('backbone');
    var AppView = require('appview');

    var AppRouter = Backbone.Router.extend({
        routes: {
            "login": "login",
            "index": "index",
            "topic/:id" : "topic",
        },

        initialize: function(){
            // 初始化项目, 显示首页
            this.appView = new AppView();
            this.loginView = new LoginView();
            this.userView = new UserView();
            this.indexFlag = false;
        },

        login: function(){
            this.loginView.show();
        },

        index: function(){
            if (g_user && g_user.id != undefined) {
                this.appView.showTopic();
                this.userView.show(g_user.username);
                this.loginView.hide();
                this.indexFlag = true;  // 标志已经到达主页了
            }
        },

        topic: function(topic_id) {
            if (g_user && g_user.id != undefined) {
                this.appView.showMessage(topic_id);
                this.userView.show(g_user.username);
                this.loginView.hide();
                this.indexFlag = true;  // 标志已经到达主页了
            }
        },
    });

    return AppRouter;
});
