"use-strict";

ckan.module('js_test',function($){
    return {
        initialize: function(){
            $.proxyAll(this, /_on/);  // anything that begins with _on give it a ref to the element.
            this.el.on('change', this._onChange)
            this.sandbox.subscribe('pub', this._on_publish)
        },
        _onChange:function(e){
            console.log("it's changed !")
            this.sandbox.publish('pub', this.el.is(':checked'))
        },
    }
});

ckan.module('disappear',function($){
    return {
        initialize:function(){
            $.proxyAll(this,/on/); 
            this.sandbox.subscribe('pub', this.onPublish)
        },
        onPublish:function(check_state){
            if(check_state){
                this.el.hide()
            }
            else{
                this.el.show()
            }
        }
    }
})