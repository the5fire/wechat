/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
$(function(){
    var User = Backbone.Model.extend({
        urlRoot: '/user',
    });

    var Topic = Backbone.Model.extend({
        urlRoot: '/topic',
    });

    var Message = Backbone.Model.extend({
        urlRoot: '/message',
    });

    var Topics = Backbone.Collection.extend({
        url: '/topic',
        model: Topic,
    });

    var Messages = Backbone.Collection.extend({
        url: '/message',
        model: Message,
    });

    var topics = new Topics;

    var TopicView = Backbone.View.extend({
        tagName:  "div class='column'",
        templ: _.template($('#topic-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });

    var messages = new Messages;

    var MessageView = Backbone.View.extend({
        tagName:  "div class='comment'",
        templ: _.template($('#message-template').html()),

        // 渲染列表页模板
        render: function() {
          $(this.el).html(this.templ(this.model.toJSON()));
          return this;
        },
    });


    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        message_section: $("#message_section"),
        message_list: $("#message_list"),
        message_head: $("#message_head"),

        events: {
            'click .submit': 'saveMessage',
        },

        initialize: function() {
          _.bindAll(this, 'addTopic', 'resetMessage', 'addMessage');

          topics.bind('add', this.addTopic);

          messages.bind('add', this.addMessage);
          messages.bind('reset', this.resetMessage);

          this.message_list_div = document.getElementById('message_list');
        },

        addTopic: function(topic) {
          var view = new TopicView({model: topic});
          this.topic_list.append(view.render().el);
        },

        addMessage: function(message) {
          var view = new MessageView({model: message});
          this.message_list.append(view.render().el);
        },

        resetMessage: function(){
            messages.each(this.addMessage);
            this.message_list.scrollTop(this.message_list_div.scrollHeight);
        },

        saveMessage: function(evt) {
            var comment_box = $('#comment')
            var content = comment_box.val();
            if (content == '') {
                alert('内容不能为空');
                return false;
            }
            var topic_id = $(evt.target).attr('topic_id');
            var message = new Message({
                content: content,
                topic_id: topic_id,
            });
            self = this;
            message.save(null, {
                success: function(model, response, options){
                    messages.add(response);
                    comment_box.val('');
                    self.message_list.scrollTop(self.message_list_div.scrollHeight)
                },
            });
        },

        showTopic: function(){
            topics.fetch();
            this.topic_list.show();
            this.message_section.hide();
            this.message_list.html('');
        },

        showMessage: function(topic_id) {
            this.message_section.show();
            this.topic_list.hide();
            
            this.showMessageHead(topic_id);
            $('#submit').attr('topic_id', topic_id);

            messages.fetch({
                url: '/message?topic_id=' + topic_id,
                reset: true,
            });
        },

        showMessageHead: function(topic_id) {
            var topic = new Topic({id: topic_id});
            self = this;
            topic.fetch({
                success: function(resp, model, options){
                    self.message_head.html(model.title);
                }
            });
        },
    });


    var AppRouter = Backbone.Router.extend({
        routes: {
            "index": "index",
            "topic/:id" : "topic",
        },

        initialize: function(){
            // 初始化项目, 显示首页
            this.appView = new AppView();
        },

        index: function(){
            this.indexFlag = true;
            this.appView.showTopic();
        },

        topic: function(topic_id) {
            this.indexFlag = true;
            this.appView.showMessage(topic_id);
        },
    });

    var appRouter = new AppRouter();
    appRouter.indexFlag = false;
    Backbone.history.start({pustState: true});
    if(appRouter.indexFlag == false) {
        appRouter.navigate('index', {trigger: true});
    }
});
