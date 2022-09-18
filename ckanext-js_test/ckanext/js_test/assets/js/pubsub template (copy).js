"use-strict";

ckan.module('popover',function($){
    return {
        initialize: function(){
            $.proxyAll(this, /_on/);  // anything that begins with _on give it a ref to the element.
            this.el.on('click', this._onClick)
            this.sandbox.subscribe('pub', this._on_publish)
        },
        _onClick:function(e){
            let title = this.options.title;
            let license = this.options.license
            //content = `title=${title}, license=${license} `
            this.el.popover({
                title:title,
                content:"license : creative-commons"
            }),
            this.sandbox.publish('pub', {"el":this.el, "title":"binga"})
        },

        _on_publish:function(data){
            if(this.el !=data.el){
                this.el.popover('hide')
            }
            // el = data.el
            // if(el)
            // el.popover({title:data.title})
        }




    }
})
