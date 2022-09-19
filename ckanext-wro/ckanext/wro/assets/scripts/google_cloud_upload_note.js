ckan.module("google_cloud_upload_modal", function($){
    /*
        display and hide the google cloud storage modal,
        events comes from both the close button and the save
        buttons. 
    */
    let modal = document.querySelector(".google_cloud_note_modal")
    return{
        initialize:function(){
            $.proxyAll(this,/_on/);
            // the save buttons
            let saveButtonsContainer = document.querySelector(".form-actions")
            for(let item of saveButtonsContainer.children){
                item.addEventListener("click", this.openModal)
            }
            // the close button
            let close_btn = document.querySelector(".google_cloud_upload_note_modal_btn")
            close_btn.addEventListener("click", this.toggleModal)



        }
        ,
        toggleModal:function(e){
            if(modal.style.display == "none"){
                modal.style.display = "block"
            }
            else{
                modal.style.display = "none"
            }
        }
        ,
        openModal: function(e){
            setTimeout(function(){
                modal.style.display = "block"
            },1000)
        }
    }
})