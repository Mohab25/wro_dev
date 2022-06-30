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
            mapWindow =  window.open('http://34.71.13.135/map');
        },
        _onStorageChange:function(e){
            $('#field-spatial').val(window.localStorage.getItem("geo_bounds"));
            mapWindow.close()
        }
    }
    
})

ckan.module('geo_data_preview', function($){
    return{
        initialize:function(){
            $.proxyAll(this,/_on/);
            let map_div_holder = document.getElementById("map")
            map_div_holder.style.width="100%"; map_div_holder.style.height="600px"; 
            let map = L.map('map').setView([-29.064594, 24.619973], 5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
            $.getJSON("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/africa.geojson",function(data){
                L.geoJson(data).addTo(map);
            })
        }
    }
})