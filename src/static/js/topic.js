/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var _ = require('underscore');

    var Topic = Backbone.Model.extend({
        urlRoot: '/topic',
    });

    var Topics = Backbone.Collection.extend({
        url: '/topic',
        model: Topic,
    });

    var TopicView = Backbone.View.extend({
        tagName:  "div class='column'",
        templ: _.template($('#topic-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });

    module.exports = {
        "Topic": Topic,
        "Topics": Topics,
        "TopicView": TopicView,
    }
});
