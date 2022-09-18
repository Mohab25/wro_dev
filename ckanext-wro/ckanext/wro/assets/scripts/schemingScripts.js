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


// ===================================
// DRY function
// previously checked from the same sessoin, did something go wrong with the submission? saves and retrieve the results

let isCheckboxPreviouslySet = function(checkbox_session_name,checkbox_element, hide_element=null){
  $(document).ready(function(e){

    /* use the session after a submittion failure
      to save the user from re-inputing
    */

    let checkedPreviously = sessionStorage.getItem(checkbox_session_name)
    if (checkedPreviously != null){
      let previously_checked_bool = "true" === checkedPreviously // convert string to boolean in js, Bool always returns true if value is not null
      
      checkbox_element.prop("checked", previously_checked_bool)
      checkbox_element.value = checkedPreviously
    
    }

  })


}

/*
  also you need to query the database to check if this is an update or a new 
  submission, if it's an update, i need the values from there first.
*/

let edit_session_submitted_previously = function(checkbox_element){
  // is there any previous value?
  return checkbox_element.is(":checked")

}

// hide elements according to whether
// the checkbox is check

let hide_conditionally = function(hide_element,previously_checked_bool ){
  if(hide_element != null){
    if(previously_checked_bool == true){ 
      for (let item of hide_element){item.hide()}
    }
    
      else{
        for (let item of hide_element){item.show()}
      }
  }
}

// ===================================

/*
  sets the checkbox for author same as contact and 
  date reference fields.

  called from:
  ---------
  1. templates/scheming/multiple_checkbox_mod: this is the first call.
  2. templates/package/edit.html: to get the pkg_dict when the form is edited
   

*/

ckan.module('ckanext_wro_toggle_repeating_field_visibilty', function($){
  let author_checkbox = $('#field-authors-0-contact_same_as_author');
  let data_classification_fieldset = $("#data_classification-field_set");
  let contact_fields = $(".contact_person_getter")
  let contact_fields_label = $('label[for="field-contact_person"]')

  return {
    initialize:function(){
      $.proxyAll(this,/_on/); 
      // for some reason the pubsub didn't work
      //this.sandbox.subscribe('pub', this._onPublish);

      if(this.options.author_contact_collected_data == true){
        // this for the edit page.
        author_checkbox.prop("checked", true)
        author_checkbox.val(true)
        contact_fields.hide();
        contact_fields_label.hide();
      }
      
      author_checkbox.on('change',this._onAlternatePublish);
            
      // change the required (*) required element visibility
      // handles the classification
      data_classification_fieldset.change(this._onChange);

    },
    _onAlternatePublish:function(e){
      // didn't use this.el because there are muliple fields with the same config
      
      if(e.target.checked){
        contact_fields.hide();
        contact_fields_label.hide();
      }
      else{
        contact_fields.show();
        contact_fields_label.show();
      }
      e.target.value = e.target.checked.toString()
      sessionStorage.setItem("contactPerson_check", e.target.checked)
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
  
  }
});


   /*  ===================== Module Documentation

    toogle the visibility of one input "Name of organization collected the data" if a checkbox 
    "did author / contact orgnization collect the data" is checked,
    
    attrs
    =====
    inialize: sets up global variables, event listeners
              data_collection_checkbox(id): the checkbox to toggle, the checkbox has an event listener
                "change" with a callback _OnChange to sense if the checkbox state is changed to check/uncheck.
    _onChange: callback function with the checkbox "change" event, it toggles the visibility of 
               "Name of organization collected the data" input field.

  called from:
  ---------
  1. 
  2. templates/package/edit.html: to get the pkg_dict when the form is edited
    
  
  */


 ckan.module('ckanext_wro_toggle_data_collection_field',function($){
    let data_collecton_checkbox = $('#field-did_author_or_contact_organization_collect_the_data')
    let data_collector_field_label = $('label[for="field-data_collection_organization')
    let data_collection_org = $('#field-data_collection_organization')
    return {
     initialize:function(){
      $.proxyAll(this, /_on/)
      console.log(this.options)
      if(this.options.author_contact_collected_data == true){
        data_collecton_checkbox.prop("checked", true)
        data_collecton_checkbox.val(true)
        data_collection_org.hide();
        data_collection_org.required = false
        data_collector_field_label.hide()
      }
       data_collecton_checkbox.on('change', this._onChange)

       //isCheckboxPreviouslySet("dataCollection_check", data_collecton_checkbox, [$('label[for="field-data_collection_organization'), this.el])

      },

      _onChange:function(e){
        
        if(e.target.checked){
          this.el.hide();
          this.el.required = false
          data_collector_field_label.hide()
        }
        else{
          this.el.show();
          data_collector_field_label.show();
        }
        e.target.value = e.target.checked.toString()
        sessionStorage.setItem("dataCollection_check", e.target.checked)
      
      }
  }
 });

ckan.module('ckanext_wro_title_field_word_count',function($){
  /*
    ================= Module Documentation
  
    displays how many words the users used with the title
    (the title is limited to 100 words)

    =================
  */

  return {
    initialize:function(){
      $.proxyAll(this, /_on/)
      let title_input = $('#field-title')  
      title_input.on('input',this._onChange)
    },

    _onChange:function(e){
      let title_label = $('label[for="field-title')
      text = "Dataset title (" + e.target.value.length + "/100 maximum characters"
      //text = `Dataset title (${e.target.value.length}/100 maximum characters)`
      title_label.text(text)
    },

  }

})

/*
===================== handles the agreement checkbox


  called from:
  ---------
  1. 
  2. templates/package/edit.html: to get the pkg_dict when the form is edited
*/


ckan.module('ckanext_wro_checkboxs_handler',function($){
  // handle the agreement checkbox.
  // handle is resource a supplementray material checkbox 
  let agreement_checkbox = $('#field-agreement')
  let is_resource_supplementary = $("#field-is_data_supplementary")

  return{
    initialize:function(){
      $.proxyAll(this, /_on/)
      // for edit template
      if(this.options.agreement == true){
        agreement_checkbox.prop("checked", true)
        agreement_checkbox.val(true)
      }

      agreement_checkbox.on("change", this._onAgreementChange)
      
      // previously checked from the same sessoin, did something go wrong with the submission? saves and retrieve the results
      //isCheckboxPreviouslySet("agreement_check", agreement_checkbox)

      // handling supplementary
      is_resource_supplementary.on("change", this._onSupplementary_change)
      
    },
    _onAgreementChange:function(e){
        sessionStorage.setItem("agreement_check", e.target.checked)
        e.target.value = e.target.checked.toString()
    },
    _onSupplementary_change:function(e){
      e.target.value = e.target.checked.toString()
    }

  }
})

ckan.module('ckanext_wro_scheming_display_page_raws_visibility_control', function($){
  
  /*
    conditionally change the display of two fields, according to values
    of other two fields, the data collection 
    orgnization and contact person fields, if the data collection
    org is the same as author/contact, and if the author is the same
    as contact respectivly this field should disappear.

  called from:
  ---------
  1. templates/scheming/display_snippets/text_mod.html

  */
  
  return{
    initialize:function(){
      $.proxyAll(this, /_on/);
      let dataset_rows_heads = $(".dataset-label")
      $.each(dataset_rows_heads,function(){
        let str = $(this).text()
        // the author field 
        if(str.includes("Is this author a contact person for the dataset?")){
          let td = $(this).next()
          let td_text = td.text()
          if(td_text.includes("true")){$(this).parent().parent().parent().parent().parent().next().hide()}
        }        
        
        if(str.includes("Did the author / contact organization collect the data?")){
          let td = $(this).next()
          let td_text = td.text()
          
          if(td_text.includes("true")){
            $(this).parent().next().hide()
          }
        }


      })
    }
  }
})

ckan.module("uncaptialize_emails",function($){
  /*
    module documentation:
      as the wro client request initial letters to be captialized in the dataset display pages
      email fields are affected by implementing the style text-transform:captialize over the   
      page, thus this module is created.
      it is used with the scheming/display_snippets/text_mod.html. 
  */
  return {
    initialize:function(){
      $.proxyAll(this, /_on/);
      let email_field = $(".dataset-label")
      if(email_field.html().toLowerCase() == "email"){email_field.next()[0].style.textTransform = "initial"}    
    }
  }
})