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
 
ckan.module('ckanext_wro_toggle_repeating_field_visibilty', function($){
  return {
    initialize:function(){
      $.proxyAll(this,/_on/); 
      //this.sandbox.subscribe('pub', this._onPublish);    // for some reason the pubsub didn't work 
      //let author_checkbox = $('#field-authors-0-contact_same_as_author-None');   // this gave some inconveniences
      let author_checkbox = $('#field-authors-0-contact_same_as_author')
      author_checkbox.on('change',this._onAlternatePublish)

      // change the required (*) required element visibility
      let data_classification_fieldset = $("#data_classification-field_set")
      data_classification_fieldset.change(this._onChange)

      $('#field-authors-0-contact_same_as_author').change(this._onCheckChange)

    },
    _onAlternatePublish:function(e){
      contact_fields = $(".contact_person_getter")   // didn't use this.el because there are muliple fields with the same config
      contact_fields_label = $('label[for="field-contact_person"]')
      if(e.target.checked){
        contact_fields.hide();
        contact_fields_label.hide();
      }
      else{
        contact_fields.show();
        contact_fields_label.show();
      }
    },
    _onChange:function(e){
      let spans = this.el.find('.control-required')
      reference_date = $('.data_reference_date_getter')
      reference_date_label = $('label[for="field-data_reference_date"]')
      
      if(e.target.value == 'static'){ 
      // kepping this span for inspiration
      spans.each((index, el)=>{ el.style.visibility = 'hidden' })
      reference_date.hide()
      reference_date_label.hide()
      }
     else {
       reference_date.show()
       reference_date_label.show()
       // kepping this for inspiration
       spans.each((index, el)=>{ el.style.visibility = 'visible'}) 
      }

    },

    _onCheckChange:function(e){
      e.target.value = e.target.checked
      console.log(e.target.checked)
      console.log(e.target.value)
    }
  
  }
});


 ckan.module('ckanext_wro_toggle_data_collection_field',function($){
   /**
    toogle the visibility of one input "Name of organization collected the data" if a checkbox 
    "did author / contact orgnization collect the data" is checked,
    
    attrs
    =====
    inialize: sets up global variables, event listeners
              data_collection_checkbox(id): the checkbox to toggle, the checkbox has an event listener
                "change" with a callback _OnChange to sense if the checkbox state is changed to check/uncheck.
    _onChange: callback function with the checkbox "change" event, it toggles the visibility of 
               "Name of organization collected the data" input field.



    */
    return {
     initialize:function(){
      $.proxyAll(this, /_on/)
       let data_collecton_checkbox = $('#field-did_author_or_contact_organization_collect_the_data')
       data_collecton_checkbox.on('change', this._onChange)
      },
      _onChange:function(e){
        data_collector_field_label = $('label[for="field-data_collection_organization')
        if(e.target.checked){
          this.el.hide();
          this.el.required = false
          data_collector_field_label.hide()
        }
        else{
          this.el.show();
          data_collector_field_label.show();
        }
      }
  }
 });

//  ckan.module("ckanext_toggle_date_reference",function($){
//     return{
//       initialize:function(){
//         $.proxyAll(this, /_on/);
//         let data_classification_fieldset = $("#data_classification-field_set")
//         data_classification_fieldset.change(this._onChange)
      
//       },

//       _onChange:function(e){
//         first_date_ref = $('#field-data_reference_date-0-data_reference_date_to')
//         second_date_ref = $('#field-data_reference_date-0-data_reference_date_from')
//         if(first_date_ref){first_date_ref.required = !first_date_ref.required}
//         else if(second_date_ref){second_date_ref.required = !second_date_ref.required}
//         console.log(e.target.value)
//       }

//     }
//  })















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