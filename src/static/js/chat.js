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

    var AppView = Backbone.View.extend({
        el: "#main",
        topic_list: $("#topic_list"),
        loader: $('#loader'),

        initialize: function() {
          //下面这个是underscore库中的方法，用来绑定方法到目前的这个对象中，是为了在以后运行环境中调用当前对象的时候能够找到对象中的这些方法。
          _.bindAll(this, 'reset', 'addOne', 'addAll', 'render');

          topics.bind('add',     this.addOne);
          topics.bind('reset',   this.reset);
          topics.bind('all',     this.render);

          this.loader.show();

          topics.fetch({reset: true});  // 设置fetch完之后reset
          this.loadRounter = false;
        },

        events: {
            'click .next_page': 'nextPage',
        },

        render: function(id) {
            console.log('app view' + id);
        }, 

        addOne: function(topic) {
          var view = new TopicView({model: topic});
          this.topic_list.append(view.render().el);
        },

        addAll: function() {
            topics.each(this.addOne);
        },

        reset: function(){
            this.addAll();
            if(!this.loadRounter){
                // 激活路由
                this.loadRounter = true;
                this.app_router = new AppRouter;
                Backbone.history.start({pustState: true});
                //this.app_router.navigate("home");
            }
            this.loader.hide();
        },
    });

    var App = new AppView;

    var AppRouter = Backbone.Router.extend({
        routes: {
            "home": "home",
            "Topic/:id" : "showTopic",
        },

        home: function(){
            App.loader.hide();
            $('#nexter').show();
        },

        showTopic: function(id) {
            alert('show topic' + id);
        },
    });
});
