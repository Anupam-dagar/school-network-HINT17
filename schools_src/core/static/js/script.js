//collapse navbar on link click
$(document).on('click','.navbar-collapse.in',function(e) {
    if( $(e.target).is('a') ) {
        $(this).collapse('hide');
    }
});

//scroll to a section
// $('#about-link').click(function() {
//     $('html, body').animate({
//         scrollTop: $('.about').offset().top-50
//     }, 800);
// });
// $('#faq-link').click(function() {
//     $('html, body').animate({
//         scrollTop: $('.faq').offset().top-50
//     }, 800);
// });
(function(){
    var x = 1;
        $('.tab-container .feed').click(function(){
            if(x==1){
            $('.about-profile').toggleClass('highlight unhighlight');
            $('.feed').toggleClass('highlight unhighlight');
            $('.profile-info-table').toggleClass('hide-section show-section');
            $('.feed-posts-container').toggleClass('hide-section show-section');
            x = 0;
            // $.ajax({
            //     type:'GET',
            //     url:'',
            //     success:function(result){

            //     }
            // });
            }
        });
        $('.about-profile').click(function(){
            if(x == 0){
            $('.about-profile').toggleClass('highlight unhighlight');
            $('.feed').toggleClass('highlight unhighlight');
            $('.feed-posts-container').toggleClass('hide-section show-section');
            $('.profile-info-table').toggleClass('hide-section show-section');
            x = 1;
            }
        });
})()


