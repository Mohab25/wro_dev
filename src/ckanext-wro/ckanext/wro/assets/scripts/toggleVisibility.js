/**
 * Ckan module toggle_visibilty is for some elements in ckan_scheming that needs
 * to respond to other elements (e.g checkbox Did the Author / Contact organization collect the data?)
 * toggle the visibility of Contact section if checked.
 * 
 * ======= the general workflow
 *         grap things by their ids and show/hide them according to the correspondent checkbox
 *         change the schema from ckanext-scheming by adding custom presets that hold the js modules.
 * 
 *  ===== how this code can imporove:
 *        currently it uses jquery to get elements from screen, i need to use pubsub for that
 */

 "use-strict";
 // keeping this to show that using pubsub didn't work before trying to grap things by ids.   
 ckan.module('ckanext_wro_metadata_form_checkbox_module',function($){
    //  return {
    //      initialize: function(){
    //          $.proxyAll(this, /_on/); 
            
    //         //this.el.on('change', this._onChange)
    //          //this.sandbox.subscribe('pub')
    //       },
    //      _onChange:function(e){
    //          console.log("it's changed !", this.el.is(':checked'))
             //this.sandbox.publish('pub', this.el.is(':checked'))
//         },
        //  teardown: function(){
        //    this.sandbox.unsubscribe('pub')
        //  }
     //}
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
      contact_fields = $(".getter_contact_person")   // didn't use this.el because there are muliple fields with the same config
      contact_fields_label = $('label[for="field-contact_person"]')
      if(e.target.checked){
        contact_fields.hide();
        contact_fields_label.hide();
      }
      else{
        contact_fields.show();
        contact_fields_label.show();
      }
    }
  
  }
});


 ckan.module('ckanext_wro_toggle_data_collection_field',function($){
    return {
     initialize:function(){
      $.proxyAll(this, /_on/)
       console.log('data collection loaded !')
       let data_collecton_checkbox = $('#field-did_author_or_contact_organization_collect_the_data-None')
       data_collecton_checkbox.on('change', this._onChange)
      },
      _onChange:function(e){
        data_collector_field_label = $('label[for="field-data_collection_organization')
        if(e.target.checked){
          this.el.hide();
          data_collector_field_label.hide()
        }
        else{
          this.el.show();
          data_collector_field_label.show();
        }
      }
  }
 });

