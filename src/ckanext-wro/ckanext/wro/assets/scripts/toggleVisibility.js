/**
 * Ckan module toggle_visibilty is for some elements in ckan_scheming that needs
 * to respond to other elements (e.g checkbox Did the Author / Contact organization collect the data?)
 * toggle the visibility of Contact section if checked.
 * 
 * 
 * 
 *  ===== how this code can imporove:
 *        currently it uses jquery to get elements from screen, i need to use pubsub for that
 */

 "use-strict";

 ckan.module('ckanext_wro_metadata_form_checkbox_module',function($){
     return {
         initialize: function(){
             $.proxyAll(this, /_on/); 
            
            //this.el.on('change', this._onChange)
             //this.sandbox.subscribe('pub')
          },
         _onChange:function(e){
             console.log("it's changed !", this.el.is(':checked'))
             //this.sandbox.publish('pub', this.el.is(':checked'))
         },
        //  teardown: function(){
        //    this.sandbox.unsubscribe('pub')
        //  }
     }
 });
 
ckan.module('ckanext_wro_toggle_repeating_field_visibilty', function($){
  return {
    initialize:function(){
      console.log('module repeating fields is loaded !')
      $.proxyAll(this,/_on/); 
      //this.sandbox.subscribe('pub', this._onPublish);    // for some reason the pubsub didn't work 
      //let author_checkbox = $('#field-authors-0-contact_same_as_author-None');   // this gave some inconveniences
      let author_checkbox = $('#field-authors-0-contact_same_as_author-None')
      author_checkbox.on('change',this._onAlternatePublish)
    },
    _onAlternatePublish:function(e){
      console.log('checked')
      contact_fields = $(".getter_contact_person")
      //console.log('binga',contact_fields)
      if(e.target.checked){
        contact_fields.hide();
        $('label[for="field-contact_person"]').hide();
      }
      else{
        contact_fields.show();
        $('label[for="field-contact_person"]').show();
      }
    }
  
  }
});


//  ckan.module('tester',function($){
//    return {
//      initialize:function(){
//        console.log('binga')
//        this.sandbox.subscribe('pub', this._onPub)
//      },
//      _onPub:function(){
//         console.log('binga is published')
//      },
//      teardown: function(){
//       this.sandbox.unsubscribe('pub')
//     }
//     }
//  });

