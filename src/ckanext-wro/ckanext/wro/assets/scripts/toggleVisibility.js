/**
 * Ckan module toggle_visibilty is for some elements in ckan_scheming that needs
 * to respond to other elements (e.g checkbox Did the Author / Contact organization collect the data?)
 * toggle the visibility of Contact section if checked.
 * 
 */

 "use strict";

ckan.module('example_theme_popover', function ($) {
    return {
      initialize: function () {
        console.log("I've been initialized for element: ", this.el);
      }
    };
  });