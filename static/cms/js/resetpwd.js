$(function(){
   $('input[type=button]').on('click',function(event){
       event.preventDefault();
       oldpwd=$('input[name=old_password]');
       newpwd=$('input[name=new_password]');
       newpwd2=$('input[name=new_password2]');

       var old_password=oldpwd.val();
       var new_password=newpwd.val();
       var new_password2=newpwd2.val();


       zlajax.post({
           'url':'/cms/resetpwd/',
           'data':{
             'oldpwd':old_password,
             'newpwd':new_password,
             'newpwd2':new_password2
           },
           'success':function(data){
               if(data['code']==200 ){
                   zlalert.alertSuccessToast('恭喜!密码修改成功');
                   oldpwd.val('')
                   newpwd.val('')
                   newpwd2.val('')
               }else{
                   var message=data['meaasge'];
                    zlalert.alertInfo(message);
               }

           },
           'fail':function(error){
               zlalert.alertNetworkError(error);
           }
       });
   });
});