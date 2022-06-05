let map = L.map('map').setView([-29.064594, 24.619973], 5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

            // // fontawesome icons with leaflet  
            // let marcadorEscuelas = L.AwesomeMarkers.icon({
            //     icon: "fa-university",
            //     prefix: "fa",
            //     markerColor: "red",
            //     iconColor: "white",
            // });

            // L.marker([-34.36526053977009, 18.471965789794925], {icon: marcadorEscuelas}).addTo(map).bindPopup("that one who called binga")

            let controlOptions = {  
            position: 'topleft',
            drawCircleMarker:false,  
            drawCircle: false,
            drawPolyline: false,
            drawPolygon: false,
            drawText: false, 
            cutPolygon: false,
            rotateMode: false,

            }

            let editOnlyControlOptions = JSON.parse(JSON.stringify(controlOptions))
            editOnlyControlOptions.drawRectangle = false
            editOnlyControlOptions.drawMarker = false


            map.pm.addControls(controlOptions);  

            let bounds = [] 

            map.on('click', function(e) {
            bounds.push([e.latlng.lat, e.latlng.lng])
            });

            map.on('pm:create', (e) => {
            map.pm.removeControls(controlOptions)
            //map.pm.toggleControls(controlOptions)      // also an option is just to toggle the visibility of controls not removing them.
            map.pm.addControls(editOnlyControlOptions)
            window.localStorage.setItem('geo_bounds', bounds);    
        });


            map.on('pm:remove', e=>{
            map.pm.removeControls(editOnlyControlOptions)
            // this doesn't show up, needs handling ========================
            map.addControls(controlOptions)
            })
