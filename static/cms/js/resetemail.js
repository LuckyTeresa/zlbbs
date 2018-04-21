$(function(){
    $('#email-captcha').on('click',function(event){
        var email=$('input[name=new_email]').val();
        console.log(email);
        if(! email){
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
           'url':'/cms/email_captcha/',
            'data':{
              'email':email
            },
            'success':function(data){
               if(data['code']==200){
                   zlalert.alertSuccessToast('邮件发送成功,请注意查收!');
               }else{
                   zlalert.alertInfo(data['message']);
               }
            },
            'fail':function(error){
                zlalert.alertNetworkError();
            }
        });

    });
});

$(function(){
   $('#submit').on('click',function(event){
       event.preventDefault();
       var emailE=$('input[name=new_email]');
       var captchaE=$('input[name=captcha]');

       var email=emailE.val();
       var captcha=captchaE.val();

       zlajax.post({
          'url':'/cms/resetemail/',
           'data':{
              'email':email,
               'captcha':captcha
           },
           'success':function(data){
              if(data['code']==200){
                  zlalert.alertSuccessToast('恭喜!邮箱修改成功!');
                  emailE.val('');
                  captchaE.val('');
              }else{
                 zlalert.alertInfo(data['message']);
              }

           },
           'fail':function(error){
               zlalert.alertNetworkError();
           }
       });


   });
});