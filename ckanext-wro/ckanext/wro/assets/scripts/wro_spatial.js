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
            let window_origin = location.origin
            mapWindow =  window.open(`${window_origin}/map/`);
            //mapWindow =  window.open('http://localhost/map');
        },
        _onStorageChange:function(e){
            console.log("value changed")
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
            let spatial_data = this.options.spatial_data
            var geojson_layer
            // the marker option
            var markerOptions = {
                radius: 4,
                fillColor: 'brown',//'#0099FF',
                color: "#fff",
                weight: 3,
                opacity: 0.8,
                fillOpacity: 0.8
            };

            spatial_data.forEach((element, idx) => {
                let element_coords = element.coordinates
                if(idx == 0){
                    var map = L.map('map').setView(element_coords, 5);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
                   //var geo_tiff_layer = L.leafletGeotiff('https://storage.cloud.google.com/wrc_wro_rasters/NASA_POWER_climatology/profile_soil_moisture_annual.tif?authuser=0').addTo(map);
                    // let geo_tiff_bounds = [[-35.0048, 17.5299,],[-21.500010, 34.000014]]

                    // L.imageOverlay("http://localhost/nasa_test.png", geo_tiff_bounds, {
                    //     opacity: 0.8,
                    //     interactive: true
                    // }).addTo(map);
                    //GeoTIFF.fromUrl("http://localhost/test.tif").then(tiff => { console.log(tiff)});
                    // (async function() {
                    //     const tiff = await GeoTIFF.fromUrl('http://localhost/test.tif/');
                    //     const image = await tiff.getImage();
                    //     console.log(image)
                    //   })()
                    let _this = this
                    geojson_layer = L.geoJson(null,{
                        pointToLayer: function (feature, latlng) {
                            return L.circleMarker(latlng, markerOptions);
                        },
                        onEachFeature:function(feature, layer){
                            layer.bindPopup(_this.markupGeojson(feature.properties))
                        }
                    }).addTo(map);
                }
                let props = element["properties"]
                let adjusted_coords = [element_coords[1], element_coords[0]]
                
                let feat = {
                    "type": "Feature",
                    "properties": props,
                    "geometry": {
                        "type": "Point",
                        "coordinates": adjusted_coords
                    }
                }
                
                
                    geojson_layer.addData(feat)
            });      
                
                

            // $.getJSON("https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/africa.geojson",function(data){
            //     L.geoJson(data).addTo(map);
            // })
        },
        markupGeojson:function(props){
            // adding properties popups
            let markup = `
            <table class="table table-striped">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Property</th>
                        <th scope="col">Value</th>
                    </tr>
                </thead>
                <tbody>
        `
    for (const prop in props){
        markup+= `<tr>
                  <td>${prop}</td>
                  <td>${props[prop]}</td>
                  </tr>  
                    `                            }
        
        markup+= `
                </tbody>
                </table>
                `
        return markup
        }
    }
})