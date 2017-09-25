/**
 * Created by sunping on 2017/9/22.
 */

$(function () {
    var error_username = true,
        error_password = true;

    var input_uname = $('#username'),
        input_pwd = $('#pwd'),
        input_remember = $('#remember');


    input_uname.blur(function () {
        // 用户名不能为空
        username = input_uname.val();
        if (username == '') {
            input_uname.next().html('用户名不能为空').show();
            error_username = true
        } else {
            input_uname.next().hide();
            error_username = false;
        }

    });

    input_pwd.blur(function () {
        // 密码不能为空
        password = input_pwd.val();
        if (password == '') {
            input_pwd.next().html('密码不能为空').show();
            error_password = true;
        } else {
            input_pwd.next().hide();
            error_password = false;
        }
    });

    $('#login_btn').click(function () {
        // alert(input_remember.is(':checked')); // true/false
        if (error_username == false && error_password == false) {
            csrf = $('input[name="csrfmiddlewaretoken"]').val();
            param = {
                'csrfmiddlewaretoken': csrf,
                'username': username,
                'password': password,
                'remember': input_remember.is(':checked')
            };
            console.log(param);
            $.post('/user/login/', param, function (data) {
                // {res:结果} 1:正确 0:错误
                if (data.res == 1) {
                    // 跳转首页
                    // location.href = '/'
                    location.href = data.next_path;
                } else {
                    input_uname.next().html('用户名或密码错误').show();
                }
            })
        }
    })


});

