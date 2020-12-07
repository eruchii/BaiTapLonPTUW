var likeBtn = document.querySelector(".like btn")
var user_id = 


likeBtn.onclick = () =>{
    if (likeBtn.value == false)
    {
        fetch("/renter/api/addLike",
        {
            method : 'POST',
            credentials : "include",
            body : JSON.stringify([),
            caches: 'no-cache',
            headers : new Headers(
            {
                "content-type":"application/json"
            })
        })
    }
    
}