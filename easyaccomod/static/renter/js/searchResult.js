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
    
    data = {}
    data.user_id = $(".user_comment").attr('id')
    data.room_id = $(".post_comment").attr('id')
    if ($(stars).hasClass('selected'))
    {
      postData('/renter/api/removeLike',data).
      then(
        $(stars).removeClass('selected')
      )
    }
    else
    {
      postData('/renter/api/addLike',data).
      then( 
        $(stars).addClass('selected') 
      )
    }
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

async function postData(url='',data){
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

aElement = document.querySelectorAll(".pagi")
for (let i = 0; i < aElement.length;i++){
  if (aElement[i].href.includes('page') == false){
  hrefLink = window.location.href + "?page="+aElement[i].id
  aElement[i].setAttribute('href',hrefLink)
  }
  else{
    hrefLink = window.location.href;
    index = hrefLink.indexOf('page=');
    index = index+5;
    hrefLink = hrefLink.slice(0,index)
    
    hrefLink = hrefLink + aElement[i].id
    console.log(hrefLink)
    aElement[i].setAttribute('href',hrefLink)
  }
}

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

roomCard = document.querySelectorAll(".room-card")
$(roomCard).on('click',function(){
  $('.user_comment').removeClass('no-display')
  data ={}
  data.room_id = this.id
  var x = $('.detail-search').firstElementChild
  // Co het data roi, chi viec load.
  postData('/renter/api/getRoomById',data).
  then(response => {
    room = response.data
    // ban_cong: true
    // chung_chu: false
    // city: "HN"
    // dieu_hoa: false
    // district: "9658"
    // gia_dien: 2552
    // gia_nuoc: 9066
    // image: "['bancong7.jpeg', 'bedroom7.jpeg', 'kitchen7.jpeg', 'livingroom7.jpeg']"
    // info: "Create room info"
    // nong_lanh: true
    // phong_bep: 2
    // phong_tam: 2
    // price: 2900000
    // room_number: 4
    // room_type_id: 3
    // tien_ich_khac: null
    // ward: "9658"
    loadRoomDetail(room)
  }).then( 
    postData('/renter/api/getPostByRoomID',data).then(
      response => loadComment(response)
    )
  )
})


function loadComment(response){
  var x = $(".post_comment")
  x.empty()
  $(".post_comment").attr("id",response.data["id"])
  for (let i = 0; i < response.data["comment"].length;i++){
    // var p = document.createElement("p")
    // var content= document.createTextNode(response.data["comment"][i].content)
    // p.append(content)
    // content= document.createTextNode(response.data["comment"][i].user_id)
    // p.append(content)
    // var div = document.createElement("div")
    // div.append(p)
    // x.append(div)
    var comment = `<div class="cmt" style="padding-left:10px; margin-top:10px;width: 100%;height: 5rem; border-radius:0.5rem; border:0.8px solid">
    <p>Comment By: ${response.data["comment"][i].username}</p>
    <p>${response.data["comment"][i].content}</p>
</div>`;
    x.append(comment)
  }
  user_id = $(".user_comment").attr("id")

  testCheckLike(user_id,response.data["id"])
}

function loadRoomDetail(data){

  $('.detail-search .room-info').remove()
  $('.detail-search .room-card').remove()
  if (data.ban_cong)
      data.ban_cong = "Có" 
    else
      data.ban_cong = "Không có"
    if (data.chung_chu)
      data.chung_chu = ""
    else
      data.chung_chu = "Không"
    if (data.dieu_hoa)
      data.dieu_hoa = "Có"
    else
      data.dieu_hoa = "Không có"
    if (data.nong_lanh)
      data.nong_lanh = "Có"
    else 
      data.nong_lanh = "Không có"
    if (!data.tien_ich_khac)
      data.tien_ich_khac = "Không có"
    
    data.image = convertStrToList(data.image)
    imageholder=''
    for (let j = 0; j < data.image.length;j++)
    {

      var src = window.origin + "/static/room_pics/" +data.image[j];

      imageholder += `<div class="mySlides6" id="mySlides" style="display: block;"><img src=${src}></div>`
    }
    let roomInfo = 
    `<div class="room-info">
        
          <h3>Vị trí : ${data.location}.</h3>
          <p class="room-detail"></br>
          Giá cả : ${data.price}VND Giá thuê - ${data.gia_dien}VND Giá / số nước - ${data.gia_nuoc}VND Giá / số điện
          </br>       
          Cơ sở vật chất: Loại phòng: ${data.roomType} -  ${data.phong_tam} phòng tắm ${data.loai_phong_tam}- ${data.phong_bep} phòng bếp ${data.loai_phong_bep}
          ${data.ban_cong} ban công - ${data.chung_chu} Chung chủ - ${data.dieu_hoa} điều hòa - ${data.nong_lanh} bình nóng lạnh
          </br>
          Tiện ích khác: ${data.tien_ich_khac}
        </p>
     </div>
    <div class="room-card" id="6" style="display:flex; flex-direction:column;">
      <div class="room-card-img" id="6" style="transform: translateX(0rem);">
        ${imageholder}
        <a class="prev" onclick = "minusSlide(-1,5)">&#10094;</a>
        <a class="next" onclick = "plusSlides(1,5)">&#10095;</a>
      </div>
     </div>
    `
    $('.detail-search').prepend(roomInfo)
    showSlides(1,5);
}


$("#submit_comment").click(function(){
    data ={}
    data["content"] = document.querySelector('#user_comment').value
    data["user_id"] = document.querySelector('.user_comment').id
    data["post_id"] = $(".post_comment").attr("id")
    console.log($(".post_comment").attr("id"))
    postData("/renter/api/Comment",data)
    window.alert("Bình luận đã được ghi nhận ! Đang chờ kiểm duyệt")
    document.querySelector('#user_comment').value = ""
})


function testCheckLike(user_id,post_id){
  data = {}
  data["user_id"] = user_id
  data["post_id"] = post_id
  postData("/renter/api/checkLikeByUser",data).then(
    response => {
      if (response.status == "True")
      {
        let likeIcon = document.querySelector("li.star")
        likeIcon.classList.add("selected")
      }
      else
      {
        let likeIcon = document.querySelector("li.star")
        likeIcon.classList.remove("selected")
      }
    }
  )
}


document.querySelector(".bedminus").addEventListener("click",function(){
  x = parseInt($("#bedroom").text())
  if (x > 0 ){
    x-=1;
  }
  $("#bedroom").text(x);
})

document.querySelector(".bedbonus").addEventListener("click",function(){
  x = parseInt($("#bedroom").text())
  x+=1;
  $("#bedroom").text(x);
})

document.querySelector(".bathminus").addEventListener("click",function(){
  x = parseInt($("#bathroom").text())
  if (x > 0 ){
    x-=1;
  }
  $("#bathroom").text(x);
})

document.querySelector(".bathbonus").addEventListener("click",function(){
  x = parseInt($("#bathroom").text())
  x+=1;
  $("#bathroom").text(x);
})


$(".js-expand").click(function() {
      $(".js-hiddenform").slideToggle();
});