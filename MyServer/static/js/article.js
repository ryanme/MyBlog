/**
 * Created by ryan on 2018/1/2.
 */
  var fullurl = window.location.href;
  var splitlist = fullurl.split('/');
  var num = splitlist[splitlist.length-2];
  var article_type = document.title;
  var menutype = article_type.split(' - ')[0];

layui.use('util', function(){
  var util = layui.util;
  //执行
  util.fixbar({
    bar1: true,
    css: {right: 50, bottom: 20},
    bgcolor: '#393D49',
    click: function(type){
      if(type=='bar1'){
        $(location).attr('href', '/blog/'+menutype+'/');
      }
    }
  });
});