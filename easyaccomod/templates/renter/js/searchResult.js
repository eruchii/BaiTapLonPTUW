$(document).ready(function(){
  
  /* 1. Visualizing things on Hover - See next part for action on click */
  $('#stars li').on('mouseover', function(){
    var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
   
    // Now highlight all the stars that's not after the current hovered star
    $(this).parent().children('li.star').each(function(e){
      if (e < onStar) {
        $(this).addClass('hover');
      }
      else {
        $(this).removeClass('hover');
      }
    });
    
  }).on('mouseout', function(){
    $(this).parent().children('li.star').each(function(e){
      $(this).removeClass('hover');
    });
  });
  
  
  /* 2. Action to perform on click */
  $('#stars li').on('click', function(){
    var onStar = parseInt($(this).data('value'), 10); // The star currently selected
    var stars = $(this).parent().children('li.star');
    
    for (i = 0; i < stars.length; i++) {
      $(stars[i]).removeClass('selected');
    }
    
    for (i = 0; i < onStar; i++) {
      $(stars[i]).addClass('selected');
    }
  });

  // 3. Open the dialog when the user hit more filter
  dialog = $(".m-dialog").dialog({
        autoOpen: false,
        width: 700,
        modal: true,
  });
  initEvens();
});


var slideIndex = [1,1,1];
var slideId = ["mySlides1", "mySlides2","mySlides3"]
showSlides(1, 0);
showSlides(1, 1);
showSlides(1,2);

function plusSlides(n, no) {
  showSlides(slideIndex[no] += n, no);
}

function minusSlide(n,no){
  showSlides(slideIndex[no] -= n, no)
}

function showSlides(n, no) {
  var i;
  var x = document.getElementsByClassName(slideId[no]);
  if (n > x.length) {slideIndex[no] = 1}    
  if (n < 1) {slideIndex[no] = x.length}
  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
  }
  x[slideIndex[no]-1].style.display = "block";  
}

function initEvens() {
  // Gán các sự kiện:
  $('#btnAdd').click(function () {
      dialog.dialog('open');
  })

  $('#btnCancel').click(function () {
      dialog.dialog('close');
  })
}