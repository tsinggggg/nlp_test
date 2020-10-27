$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

$("a[href^='#'].anchor").on('click', function (e) {

    // prevent default anchor click behavior
    e.preventDefault();

    // store hash
    var hash = this.hash;

    // animate
    $('html, body').animate({
        scrollTop: $(hash).offset().top
    }, 300, function () {

        // when done, add hash to url
        // (default click behaviour)
        window.location.hash = hash;
    });

});


$(document).ready(function () {

    $(" #ta_filter_btn > button.btn").on("click", function(){
       var letter =  $(this).text().toUpperCase();

	$(" #ta_detail_table tr td:nth-child(2)").each(function () {
            $(this).parent().show();
            if(letter == "FAILED" && $(this).text().toUpperCase().indexOf(letter) == -1){
                $(this).parent().hide();
            }
            if(letter == "SKIPPED" && $(this).text().toUpperCase().indexOf(letter) == -1){
                $(this).parent().hide();
            }
            if(letter == "SUCCESSFUL" && ($(this).text().toUpperCase().indexOf("FAILED") != -1 ||
             $(this).text().toUpperCase().indexOf("SKIPPED") != -1)){
                $(this).parent().hide();
            }
       });
   });

});