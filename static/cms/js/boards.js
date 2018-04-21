$(function(){
   $('#add_board_btn').on('click',function(){
       event.preventDefault();
       zlalert.alertOneInput({
           'text':'请输入板块名称',
           'placeholder':'版块名称',
           'confirmCallback':function(inputValue){
               zlajax.post({
                  'url':'/cms/aboards/',
                   'data':{
                      'name':inputValue
                   },
                   'success':function(data){
                      if(data['code']==200){
                          window.location.reload();
                      }else{
                          zlalert.alertInfo(data['message']);
                      }
                   }
               });

           }
       })
   });

});

$(function(){
    $('.edit-board-btn').on('click',function(){
    var $this=$(this);
    var tr=$this.parent().parent();
    var name=tr.attr('data-name');
    var board_id=tr.attr('data-id');

    zlalert.alertOneInput({
       'text':'请输入版块名称',
        'placeholder':name,
        'confirmCallback':function(inputValue){
           zlajax.post({
              'url':'/cms/uboards/',
               'data':{
                  'board_id':board_id,
                   'name':inputValue
               },
               'success':function(data){
                  if(data['code']==200){
                      window.location.reload();
                  }else{
                      zlalert.alertInfo(data['message'])
                  }
               }
           });
        }
    });

    });

});


$(function(){
    $('.delete-board-btn').on('click',function(event){
        event.preventDefault();
        var $this=$(this);
        var board_id=$this.parent().parent().attr('data-id');
        zlalert.alertConfirm({
            'title':'删除版块',
            'msg':'确认删除该版块吗?',
            'confirmCallback':function(){
                zlajax.post({
                   'url':'/cms/dboards/',
                   'data':{
                       'board_id':board_id
                   } ,
                    'success':function(data){
                       if(data['code']==200){
                           window.location.reload();
                       }else{
                           zlalert.alertInfo(data['message']);
                       }
                    }
                });
            }
        })
    })
});