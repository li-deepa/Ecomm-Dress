
 $(document).ready(function(){
    //create variable
    var counts = 0;
    $(".wishlist").click(function () {
    //to number and increase to 1 on each click
       counts += +1;
       $(".cart-wish").animate({
    //show span with number
                 opacity: 1
             }, 300, function () {
    //write number of counts into span
                 $(this).text(counts);
             });
         }); 
 });

 