"use-strict";
ckan.module("xml_parse",function($){
    return{
        initialize: function(){
            $.proxyAll(this,/_on/); 
            this.el.on("change", this._onChange)
        },
        _onChange:function(e){
            let the_input = document.getElementById('upload_input')
            let _file = the_input.files[0]
            let formData = new FormData();
            formData.append("the_file",_file)
            fetch(window.location.href+'xml_parser/',{method:"POST", body:formData}).
            then(res=>console.log(res))
        }
    }
})