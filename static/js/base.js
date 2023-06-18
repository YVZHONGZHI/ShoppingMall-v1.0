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