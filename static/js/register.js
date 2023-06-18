$(function (){
    $("#myfile").change(function () {
        let myFileReaderObj = new FileReader();
        let fileObj = $(this)[0].files[0];
        myFileReaderObj.readAsDataURL(fileObj)
        myFileReaderObj.onload = function () {
            $('img').attr('src', myFileReaderObj.result)
        }
    })
})


function judge() {
	$(function (){
        let formDateObj = new FormData();
        $.each($('#w').serializeArray(),function (index, obj) {
            formDateObj.append(obj.name, obj.value)
        })
        formDateObj.append('avatar',$('#myfile')[0].files[0]);
        $.ajax({
            url:'',
            type:'post',
            data:formDateObj,
            contentType:false,
            processData:false,
            success:function (args) {
                if (args.code===1000) {
                    setTimeout(()=>{alert('注  册  成  功!')},200)
                }
                else {
                    $.each(args.msg,function (index,obj) {
                        let targetId = '#id_' + index;
                        $(targetId).parent().next().children().text(obj[0])
                    })
                }
            }
        })
	})
}


$(function (){
    $('input').focus(function () {
        $(this).parent().next().children().text('')
    })
})