$(document).ready(function(){

    $('#id_image').parent().css('overflow', 'auto')
    
    setTimeout(() => {
        $("#is_add").hide()
    }, 2000);

    $('#id_is_superuser').parent().addClass('red_superuser');
    

    var loadUserDetail = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-user-detail .modal-content').html("");
                $('#modal-user-detail').modal("show");
            },
            success:function(resp) {
                $('#modal-user-detail .modal-content').html(resp.detail_user);
            }
        })
    }

    $('.user-btn-detail').click(loadUserDetail);

})
