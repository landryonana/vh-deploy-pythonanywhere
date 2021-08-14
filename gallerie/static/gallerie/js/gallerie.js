$(document).ready(function(){
    
    var loadGallerieDetailImage = function(){
        var btn = $(this); 
        console.log('message')
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-image .modal-content').html("");
                $('#modal-image').modal("show");
            },
            success:function(resp) {
                $('#modal-image .modal-content').html(resp.detail_image);
            }
        })
    }

    $('.gallerie-btn-detail').click(loadGallerieDetailImage);

})
  