$(document).ready(function(){
    
    var loadRapportDetailBoss = function(){
        var btn = $(this); 
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-detail .modal-content').html("");
                $('#modal-detail').modal("show");
            },
            success:function(resp) {
                $('#modal-detail .modal-content').html(resp.detail_info);
            }
        })
    }

    $('.rapport-btn-detail').click(loadRapportDetailBoss);

})
  