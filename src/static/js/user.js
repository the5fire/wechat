/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var _ = require('underscore');

    var User = Backbone.Model.extend({
        urlRoot: '/user',
    });

    var LoginView = Backbone.View.extend({
        el: "#login",
        wrapper: $('#wrapper'),

        initialize: function(appRouter) {
            this.appRouter = appRouter;
        },
        
        events: {
            'keypress #login_pwd': 'loginEvent',
            'click .login_submit': 'login',
            'keypress #reg_pwd_repeat': 'registeEvent',
            'click .registe_submit': 'registe',
        },

        hide: function() {
            this.wrapper.hide();
        },

        show: function() {
            this.wrapper.show();
        },

        loginEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.login(evt);
            }
        },

        login: function(evt){
            var username_input = $('#login_username');
            var pwd_input = $('#login_pwd');
            var u = new User({
                username: username_input.val(),
                password: pwd_input.val(),
            });
            var self = this;
            u.save(null, {
                url: '/login',
                success: function(model, resp, options){
                    self.appRouter.g_user = resp;
                    // 跳转到index
                    self.appRouter.navigate('index', {trigger: true});
                },
                error: function(model, resp, options){
                    alert(resp.responseText);
                }
            });
        },

        registeEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.registe(evt);
            }
        },

        registe: function(evt){
            var reg_username_input = $('#reg_username');
            var reg_pwd_input = $('#reg_pwd');
            var reg_pwd_repeat_input = $('#reg_pwd_repeat');
            var u = new User({
                username: reg_username_input.val(),
                password: reg_pwd_input.val(),
                password_repeat: reg_pwd_repeat_input.val(),
            });
            var self = this;
            u.save(null, {
                success: function(model, resp, options){
                    self.appRouter.g_user = resp;
                    // 跳转到index
                    self.appRouter.navigate('index', {trigger: true});
                },
                error: function(model, resp, options){
                    alert(resp.responseText);
                }
            });
        },
    });

    var UserView = Backbone.View.extend({
        el: "#user_info",
        username: $('#username'),

        show: function(username) {
            this.username.html(username);
            this.$el.show();
        },
    });

    module.exports = {
        "User": User,
        "UserView": UserView,
        "LoginView": LoginView,
    };
});
