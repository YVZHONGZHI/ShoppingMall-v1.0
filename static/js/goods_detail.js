$(function (){
    $('.action').click(function () {
        let isUp = $(this).hasClass('diggit')
        let $div = $(this)
        let goods_id = $div.children().attr('goods_id')
        $.ajax({
            url:'/up_or_down/',
            type:'post',
            data: {'goods_id':goods_id, 'is_up':isUp},
            success:function (args) {
                if (args.code === 1000) {
                    $('#digg_tips').text(args.msg)
                    let oldNum = $div.children().text()
                    $div.children().text(Number(oldNum) + 1)
                }
                else {
                    $('#digg_tips').html(args.msg)
                }
            }
        })
    })
})


$(function (){
    $('#id_car').click(function () {
        let goods_id = $('#id_car').attr('goods_id')
        $.ajax({
            url:'/shop_car/',
            type:'post',
            data: {'goods_id':goods_id},
            success:function (args) {
                if (args.code === 1000) {
                    $('#car_tips').text(args.msg)
                }
                else {
                    $('#car_tips').html(args.msg)
                }
            }
        })
    })
})


$(function (){
    let parentId = null
    $('.reply').click(function () {
        let commentUserName = $(this).attr('username')
        parentId = $(this).attr('comment_id')
        $('#id_comment').val('@ ' + commentUserName + '\n').focus()
    })


    $('#id_submit').click(function () {
        let content = $('#id_comment').val()
        let goods_id = $('#id_comment').attr('goods_id')
        let userName = $('#id_comment').attr('userName')
        if (parentId) {
            let indexNum = content.indexOf('\n') + 1
            content = content.slice(indexNum)
        }
        $.ajax({
            url:'/comment/',
            type:'post',
            data: {'goods_id':goods_id, 'content':content, 'parent_id':parentId},
            success:function (args) {
                if (args.code === 1000) {
                    $('#error').text('评论成功')
                    $('#id_comment').val('')
                    let temp = `<li class="list-group-item">
                                    <span>
                                        最新评论
                                    </span>
                                    <span>
                                        &nbsp;·&nbsp;&nbsp;${args.msg}
                                    </span>
                                    <span>
                                        &nbsp;·&nbsp;&nbsp;${userName}
                                    </span>
                                    <span>
                                        <br>
                                        <br>
                                        <a class="pull-right reply" style='text-decoration:none'>回复</a>
                                    </span>
                                    <div>
                                        ${content}
                                    </div>
                                </li>`
                    $('.list-group').append(temp)
                    parentId = null
                }
                else {
                    $('#error').html(args.msg)
                }
            }
        })
    })
})


$(function (){
    $("#set_password").click(function () {
        $.ajax({
            url:'/set_password/',
            type:'post',
            data: {'old_password':$('#id_old_password').val(), 'new_password':$('#id_new_password').val(), 'confirm_password':$('#id_confirm_password').val()},
            success:function (args) {
                if (args.code===1000) {
                    alert(args.msg)
                    window.location.reload()
                }
                else {
                    $("#password_error").text(args.msg)
                }
            }
        })
    })
})


$(function (){
    $("#avatar").change(function () {
        let myFileReaderObj = new FileReader();
        let fileObj = $(this)[0].files[0];
        myFileReaderObj.readAsDataURL(fileObj)
        myFileReaderObj.onload = function () {
            $('#myimg').attr('src', myFileReaderObj.result)
        }
    })
})


$(function (){
    $("#set_avatar").click(function () {
        let formDateObj = new FormData();
        formDateObj.append('avatar',$('#avatar')[0].files[0]);
        $.ajax({
            url:'/set_avatar/',
            type:'post',
            data:formDateObj,
            contentType:false,
            processData:false,
            success:function (args) {
                if (args.code === 1000) {
                    alert(args.msg)
                    window.location.reload()
                }
            }
        })
    })
})


function test() {
	let inputEle = document.getElementById("search");
	let search = inputEle.value;
	if(search === ''){
		alert("关键字不能为空!")
	}
	else{
		alert("不  给  搜  索")
	}
}