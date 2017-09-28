/**
 * Created by sunping on 2017/9/27.
 */
$(function () {
    var num_show = $('.num_show');

    $('.add').click(function () {
        // 加1
        var goods_count = parseInt(num_show.val()) + 1;
        num_show.val(goods_count);
        update_total_price()
    });
    $('.minus').click(function () {
        // 减1
        var goods_count = parseInt(num_show.val()) - 1;
        if (goods_count < 1){
            goods_count = 1;
        }
        num_show.val(goods_count);
        update_total_price()
    });
    function update_total_price() {
        // 计算总价
        var goods_price = parseFloat($('.show_pirze').children('em').text());  // 单价
        var goods_count = parseInt($('.num_show').val());  // 总数
        var total_price = goods_price * goods_count;
        $('.total').children('em').text(total_price.toFixed(2) + '元');
    }
    num_show.blur(function () {
        // 手动输入
        // 校验输入数据的合法性
        var goods_count = $(this).val();
        if (parseInt(goods_count) < 1 || goods_count.trim().length == 0 || isNaN(goods_count)){
            goods_count = 1
        }
        num_show.val(parseInt(goods_count));
        update_total_price();
    });


    $('#add_cart').click(function () {
        // 判断用户是否登录
        // {% if request.session.islogin %}
            var $add_x = $('#add_cart').offset().top;
            var $add_y = $('#add_cart').offset().left;

            var $to_x = $('#show_count').offset().top;
            var $to_y = $('#show_count').offset().left;

            $(".add_jump").css({'left':$add_y+80,'top':$add_x+10,'display':'block'});
            // 已登录, 发送 ajax的get 请求保存到数据库, 参数:商品 id 和商品数目
            // var goods_id = {{ goods.id }};
            // alert(goods_id+':'+ parseInt(num_show.val()));
            $.get('/cart/add/?goods_id='+goods_id+'&goods_count='+parseInt(num_show.val()), function (data) {
                // {res: 结果} 1: 添加成功 0: 添加失败
                if(data.res){
                    // 执行动画
                    $(".add_jump").stop().animate({
                        'left': $to_y+7,
                        'top': $to_x+7},
                        "fast", function() {  // "slow", "normal", 或 "fast"
                            $(".add_jump").fadeOut('fast',function(){
                                // 改变总数量
                                $('#show_count').text(parseInt($('#show_count').text()) + parseInt(num_show.val()));
                            });
                    });

                }else {
                    alert('添加失败')
                }
            });

        // {% else %}
            // 未登录
            alert('请先登录');
        // {% endif %}
    })
})