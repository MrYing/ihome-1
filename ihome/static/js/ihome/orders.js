//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    var queryData = decodeQuery();
    var role = queryData["role"];
    // 查询房客订单
    $.get('/api/1.0/orders?role=' + role, function (res) {
            if (res.re_code == '0') {
                render_template = template('orders-list-tmpl', {'orders': res.data.order_list});
                $('.orders-list').html(render_template);
                //  查询成功之后需要设置评论的相关处理

                $('.order-pay').on('click', function () {
                    var orderId = $(this).parents('li').attr('order-id');
                    $.ajax({
                        url: 'api/1.0/orders/' + orderId + '/payment',
                        type: 'put',
                        dataType: 'json',
                        headers: {
                            'X-CSRFToken': getCookie('csrf_token'),
                        },
                        success: function (res) {
                            if ('4101' == res.re_code) {
                                location.href = '/login.html';
                            } else if ('0' == res.re_code) {
                                location.href = res.data.pay_url;
                            }
                        }
                    })
                });


                $(".order-comment").on("click", function () {
                    var orderId = $(this).parents("li").attr("order-id");
                    $(".modal-comment").attr("order-id", orderId);

                    $(".modal-comment").on('click', function () {
                        var orderId = $(this).attr("order-id");
                        var reason = $('#comment').val();
                        if (!reason) {
                            reason = "五星好评!";
                        }
                        // console.log((orderId))
                        $.ajax({
                            url: '/api/1.0/orders/comment/' + orderId,
                            type: 'put',
                            data: JSON.stringify({'reason': reason}),
                            contentType: 'application/json',
                            headers: {'X-CSRFToken': getCookie('csrf_token')},
                            success: function (response) {
                                if (response.re_code == '0') {
                                    $('#comment-modal').modal('hide');
                                    alert(response.msg);
                                    $('.orders-list li[order-id=' + orderId + ']').find('button').remove();
                                    $('.orders-list li[order-id=' + orderId + ']').find('ul li:last').text("订单状态：已完成");
                                    $('.orders-list li[order-id=' + orderId + ']').find('ul').append("<li>我的评论：" + reason + "</li>");
                                } else if (response.re_code == '4103') {
                                    alert(response.msg);
                                }
                            }
                        })
                    })
                });


                $(".order-cancel").on("click", function () {
                    var orderId = $(this).parents("li").attr("order-id");
                    $(".modal-comment").attr("order-id", orderId);

                    $(".modal-comment").on('click', function () {
                        var orderId = $(this).attr("order-id");
                        var reason = $('#comment').val();
                        if (!reason) {
                            alert('请填写取消理由！');
                            return;
                        }
                        // console.log((orderId))
                        $.ajax({
                            url: 'api/1.0/orders/' + orderId,
                            type: 'delete',
                            data: JSON.stringify({'reason': reason}),
                            contentType: 'application/json',
                            headers: {'X-CSRFToken': getCookie('csrf_token')},
                            success: function (response) {
                                if (response.re_code == '0') {
                                    $('#comment-modal').modal('hide');
                                    $('.orders-list li[order-id=' + orderId + ']').remove();
                                } else if (response.re_code == '4103') {
                                    alert(response.msg)
                                }
                            }
                        })
                    });


                })
            } else if (res.re_code == '4101') {
                location.href = '/login.html'
            } else {
                alert(res.msg)
            }
        }
    );

});
