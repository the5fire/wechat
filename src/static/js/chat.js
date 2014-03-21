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
            'click .submit_topic': 'saveTopic',
            'keypress #comment': 'saveMessageEvent',
        },

        initialize: function() {
            _.bindAll(this, 'addTopic', 'addMessage');

            topics.bind('add', this.addTopic);

            // 定义消息列表池，每个topic有自己的message collection
            // 这样保证每个主题下得消息不冲突
            this.message_pool = {};

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

        saveMessageEvent: function(evt) {
            if (evt.keyCode == 13) {
                this.saveMessage(evt);
            }
        },
        saveMessage: function(evt) {
            var comment_box = $('#comment')
            var content = comment_box.val();
            if (content == '') {
                alert('内容不能为空');
                return false;
            }
            var topic_id = comment_box.attr('topic_id');
            var message = new Message({
                content: content,
                topic_id: topic_id,
            });
            self = this;
            var messages = this.message_pool[topic_id];
            message.save(null, {
                success: function(model, response, options){
                    comment_box.val('');
                    // 重新获取，看服务器端是否有更新
                    // 比较丑陋的更新机制
                    messages.fetch({
                        data: {topic_id: topic_id},
                        success: function(){
                            self.message_list.scrollTop(self.message_list_div.scrollHeight);
                            messages.add(response);
                        },
                    });
                },
            });
        },

        saveTopic: function(evt) {
            var topic_title = $('#topic_title');
            if (topic_title.val() == '') {
                alert('主题不能为空！');
                return false
            }
            var topic = new Topic({
                title: topic_title.val(),
            });
            self = this;
            topic.save(null, {
                success: function(model, response, options){
                    topics.add(response);
                    topic_title.val('');
                },
            });
        },

        showTopic: function(){
            topics.fetch();
            this.topic_list.show();
            this.message_section.hide();
            this.message_list.html('');
        },

        initMessage: function(topic_id) {
            var messages = new Messages;
            messages.bind('add', this.addMessage);
            this.message_pool[topic_id] = messages;
        },

        showMessage: function(topic_id) {
            this.initMessage(topic_id);

            this.message_section.show();
            this.topic_list.hide();
            
            this.showMessageHead(topic_id);
            $('#comment').attr('topic_id', topic_id);

            var messages = this.message_pool[topic_id];
            messages.fetch({
                data: {topic_id: topic_id},
                success: function(resp) {
                    self.message_list.scrollTop(self.message_list_div.scrollHeight)
                }
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
        // 跳转到index
        appRouter.navigate('index', {trigger: true});
    }
});
