/**
 * Created by ryan on 2018/1/2.
 */
var fullurl = window.location.href
var splitlist = fullurl.split('/')
var type = splitlist[splitlist.length-2]
// var data_length = $.ajax({
//         type: "get",
//         url: "http://127.0.0.1:5000/api/totalarticles",
//         data: { type: type},
//         success: function (data) {
//                 return data;
//         }
//     });
function get_articles(pageid) {
       $.ajax({
        type: "get",
        url: "http://127.0.0.1:5000/api/articles",
        data: { pageid: pageid, type: type},
        async: false,
        success: function (data) {
             total = data['data']['total']
            if (total!=0){
            var html = '';
            $.each(data['data']['bloglist'], function () {
                html += '<div class="blogs">';
                html += '<h3><a class="title" href="/article/'+this.id+'/">'+this.title+'</a></h3>';
                html += '<figure><img src="/img/0.gif" ></figure>'
                html +='<ul class="shortcontent"><p>看到昔日好友发了一篇日志《咎由自取》他说他是一个悲观者，感觉社会抛弃了他，脾气、' +
                    '性格在6年的时间里变化很大，很难适应这个社会。人生其实就是不断犯错的过程，在这个过程中不断的犯错，' +
                    '不断的吸取教训，不断的成长。也许日子里的惊涛骇浪，不过是人生中的水花摇晃，别用显微镜放大你的悲伤。' +
                    '</p> <a href="/article/'+this.id+'/" class="readmore">阅读全文&gt;&gt;</a></ul>';
                html += '<p class="autor">';
                html += '<span>作者: '+this.author+'</span>';
                html += '<span>分类:【<a>'+this.type+'</a>】</span>';
                html += '<span>浏览:（<a>'+this.visit+'</a>）</span></p>';
                html += '<div class="dateview">'+this.time+'</div>';
                html += '</div>'
            });
             $('#bloglist').html(html)
            }else {
                var html = '<div class="noarticle"><p>本栏目下暂无文章!</p></div>';
                $('#bloglist').html(html)
            }
        }
    });
    return total
}

 layui.use(['laypage'], function() {
     get_articles(1);
     var laypage = layui.laypage;
     laypage.render({
         elem: 'page',
         count: total,
         layout: ['prev', 'page', 'next'],
         jump: function (obj, first) {
                if(!first){
                    var pageid = obj.curr;
                    get_articles(pageid)
                }
         }
     });
 });



    //      $.ajax({
    //     type: "get",
    //     url: "http://127.0.0.1:5000/api/articles",
    //     data: { pageid: obj.curr, type: type},
    //     success: function Getnums(data) {
    //         if (data.length!=0){
    //         var html = '';
    //         $.each(data['data']['bloglist'], function () {
    //             html += '<div class="blogs">';
    //             html += '<h3><a class="title" href="/article/'+this.id+'/">'+this.title+'</a></h3>';
    //             html += '<figure><img src="/img/0.gif" ></figure>'
    //             html +='<ul class="shortcontent"><p>看到昔日好友发了一篇日志《咎由自取》他说他是一个悲观者，感觉社会抛弃了他，脾气、' +
    //                 '性格在6年的时间里变化很大，很难适应这个社会。人生其实就是不断犯错的过程，在这个过程中不断的犯错，' +
    //                 '不断的吸取教训，不断的成长。也许日子里的惊涛骇浪，不过是人生中的水花摇晃，别用显微镜放大你的悲伤。' +
    //                 '</p> <a href="/article/'+this.id+'/" class="readmore">阅读全文&gt;&gt;</a></ul>';
    //             html += '<p class="autor">';
    //             html += '<span>作者: '+this.author+'</span>';
    //             html += '<span>分类:【<a>'+this.type+'</a>】</span>';
    //             html += '<span>浏览:（<a>'+this.visit+'</a>）</span></p>';
    //             html += '<div class="dateview">'+this.time+'</div>';
    //             html += '</div>'
    //         });
    //          $('#bloglist').html(html)
    //         }else {
    //             var html = '<div class="noarticle"><p>本栏目下暂无文章!</p></div>';
    //             $('#bloglist').html(html)
    //         }
    //     }
    // });
