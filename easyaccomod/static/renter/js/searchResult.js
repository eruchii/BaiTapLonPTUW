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
    cnt = 0;
    var onStar = parseInt($(this).data('value'), 10); // The star currently selected
    var stars = $(this).parent().children('li.star');
    
    for (i = 0; i < stars.length; i++) {
      $(stars[i]).removeClass('selected');
    }
    
    for (i = 0; i < onStar; i++) {
      $(stars[i]).addClass('selected');
    }
    cnt = document.querySelectorAll("#stars li.selected").length
    console.log(cnt)
  });

  // 3. Open the dialog when the user hit more filter
  dialog = $(".m-dialog").dialog({
        autoOpen: false,
        width: 700,
        modal: true,
  });
  
  initEvens();

  initImages();
  showSlides(1,0);
  showSlides(1,1);
  showSlides(1,2);
  showSlides(1,3);
  showSlides(1,4);
  showSlides(1,5);
  showSlides(1,6);
});




var slideIndex = [1,1,1,1,1,1];
var slideId = ["mySlides1", "mySlides2","mySlides3","mySlides4","mySlides5","mySlides6"]


function plusSlides(n, no) {
  showSlides(slideIndex[no] += n,no);
}

function minusSlide(n,no){
  showSlides(slideIndex[no] -= n, no)
}

function showSlides(n, no) {
  try{
    var i;
    var x = document.getElementsByClassName(slideId[no]); // tra ve div cua slide
    if (n > x.length) {slideIndex[no] = 1}    // xoay vong hinh anh
    if (n < 1) {slideIndex[no] = x.length}  // xoay vong hinh anh
    for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";  
    }
    x[slideIndex[no]-1].style.display = "block";  // hien thi slide dau tien
  }
  catch(error){
    return
  }
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


// Add Image into its Slideshow
function initImages(){
  var slideHolder = $(".room-card-img")
  for (let i = 0; i < slideHolder.length;i++)
  {
    let imageList = convertStrToList(slideHolder[i].firstElementChild.id)
    console.log(imageList + slideHolder[i].id)

    // id cua Tung Room Card Image, se la Id cua div chua anh slideshow
    for (let j = 0; j < imageList.length;j++)
    {
      // tao anh
      var img = document.createElement("img");
      var src = window.origin + "/static/room_pics/" +imageList[j];
      img.setAttribute("src", src);
 
      var div = document.createElement("div");
      div.setAttribute("class","mySlides"+ slideHolder[i].id)
      div.setAttribute("id","mySlides")

      div.appendChild(img)
      // tao div chua anh

      // Van de : Them anh vao, moi anh 1 div. Hien tai la 1 div chua het cac anh
      // Solution : Gan ID = slideHolder, tao Div chua", 
      // lay id tu slideHolder gan" cho div
      // Append Div

      slideHolder[i].insertBefore(div,slideHolder[i].childNodes[1])
    }
  }
}

function convertStrToList(str) {
  var ans = [];
  var temp = [];
  for (let i = 0; i < str.length; i++) {
      if (str[i] == "'") {
          temp.push(i);
      }
  }
  var str_element = "";
  for (let j = 0; j < temp.length; j+=2) {
      for (let k = temp[j]+1; k < temp[j+1]; k++) {
          str_element += str[k];
      }
      ans.push(str_element);
      str_element = "";
  }
  return(ans)
}

// aElement = document.querySelectorAll(".pagi")
// for (let i = 0; i < aElement.length;i++){
//   if (aElement[i].href.includes('page') == false){
//   hrefLink = window.location.href + "&page="+aElement[i].id
//   aElement[i].setAttribute('href',hrefLink)
//   }
//   else{
//     hrefLink = window.location.href;
//     index = hrefLink.indexOf('page')
//     hrefLink = hrefLink.slice(0,index-1)
//     hrefLink = hrefLink +"&page=" + aElement[i].id
//     aElement[i].setAttribute('href',hrefLink)
//   }
// }

// roomCard = document.querySelectorAll(".room-card")
// for (let i =0 ; i < roomCard.length;i++)
// {
//   roomCard[i].onclick = loadToDetail(roomCard[i])
// }

// function loadToDetail(element){
//   detailSearch = document.querySelector(".detail-search")
//   while(detailSearch.firstChild){
//     detailSearch.removeChild(detailSearch.lastChild)
//   }
//   detailSearch.appendChild(element)
// }