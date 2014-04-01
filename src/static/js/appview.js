/*
 * author: the5fire
 * blog:  the5fire.com
 * date: 2014-03-16
 * */
define(function(require, exports, module) {
    var $ = require('jquery');
    var _ = require('underscore');
    var Backbone = require('backbone');

    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    var socket = io.connect();
    socket.on('connect', function(){
        console.log('connected');
    });

    $(window).bind("beforeunload", function() {
        socket.disconnect();
    });

    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        topic_section: $("#topic_section"),
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
            this.socket = null;

            this.message_list_div = document.getElementById('message_list');
        },

        addTopic: function(topic) {
            var view = new TopicView({model: topic});
            this.topic_list.append(view.render().el);
        },

        addMessage: function(message) {
            var view = new MessageView({model: message});
            this.message_list.append(view.render().el);
            self.message_list.scrollTop(self.message_list_div.scrollHeight);
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
            var messages = this.message_pool[topic_id];
            message.save(null, {
                success: function(model, response, options){
                    comment_box.val('');
                    // 发送成功之后，通过socket再次发送
                    messages.add(response);
                    // FIXME: 最后可通过socket直接通信并保存
                    socket.emit('message', response);
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
            this.topic_section.show();
            this.message_section.hide();
            this.message_list.html('');

            this.goOut()
        },

        goOut: function(){
            // 退出房间
            socket.emit('go_out');
            socket.removeAllListeners('message');
        },

        initMessage: function(topic_id) {
            var messages = new Messages;
            messages.bind('add', this.addMessage);
            this.message_pool[topic_id] = messages;
        },

        showMessage: function(topic_id) {
            this.initMessage(topic_id);

            this.message_section.show();
            this.topic_section.hide();
            
            this.showMessageHead(topic_id);
            $('#comment').attr('topic_id', topic_id);

            var messages = this.message_pool[topic_id];
            // 进入房间
            socket.emit('topic', topic_id);
            // 监听message事件，添加对话到messages中
            socket.on('message', function(response) {
                debugger;
                var model = JSON.parse(response);
                messages.add(model);
            });
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
    return AppView;
});
