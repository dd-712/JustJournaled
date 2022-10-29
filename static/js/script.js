
// profile.html
addBtn = document.querySelector(".pCard_add");
if (addBtn) {
    addBtn.addEventListener("click",()=>{
        document.querySelector(".pCard_card").classList.toggle("pCard_on");
        if(document.querySelector(".fa-minus"))
            document.querySelector(".pCard_add").innerHTML='<i class="fa fa-plus"></i>';
        else 
        document.querySelector(".pCard_add").innerHTML='<i class="fa fa-minus"></i>';
    });
}