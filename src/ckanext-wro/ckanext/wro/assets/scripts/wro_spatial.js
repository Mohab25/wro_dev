"use-strict"

ckan.module("wro_spatial",function($){
    return{
        initialize:function(){
            $.proxyAll(this,/_on/); 
            this.el.on('click', this._onClick)
            window.localStorage.setItem('geo_bounds', '');  // avoiding a bug with chrome : https://stackoverflow.com/a/58177957/7765766
            window.addEventListener("storage",this._onStorageChange);
        },
        _onClick:function(e){
            mapWindow =  window.open('http://localhost/map');
        },
        _onStorageChange:function(e){
            $('#field-spatial').val(window.localStorage.getItem("geo_bounds"));
            mapWindow.close()
        }
    }
    
})

// ckan.module('wro_custom_map', function($){
//     return{
//         initialize:function(){
//             console.log('bings')
//             // tried the custom map module but did't work with the blueprint
//             //migrated to the blueprint template directory
//         }
//     }
// })