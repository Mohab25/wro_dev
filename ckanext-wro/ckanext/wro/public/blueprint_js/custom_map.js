const map_container = document.getElementById("map")
const initMap = function(){const map = new google.maps.Map(map_container, {
    zoom:5,
    center:{lat: -29.064594, lng: 24.619973}
})


const drawManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.MARKER,
    drawingControl: true,
    drawingControlOptions: {
        position: google.maps.ControlPosition.LEFT_CENTER,
        drawingModes:[
            google.maps.drawing.OverlayType.RECTANGLE,
            google.maps.drawing.OverlayType.MARKER,
            
        ]
    }, 
    markerOptions: {
        icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
      },
    rectangleOptions:{
        editable: true,
        draggable: true,
        strokeColor: "#4682b4"
    },
})

drawManager.setMap(map); 

google.maps.event.addListener(drawManager, 'overlaycomplete', function(event) {
    if (event.type == 'rectangle') {
          let north_east = event.overlay.getBounds().getNorthEast().toJSON()
          let north_east_list = [north_east.lat, north_east.lng]
          let south_west = event.overlay.getBounds().getSouthWest().toJSON()
          let south_west_list = [south_west.lat, south_west.lng]
          let north_west = [north_east_list[0], south_west_list[1]]
          let south_east = [south_west_list[0], north_east_list[1]]
        
          let bounds = [...north_west, ...south_east] 
        
          window.localStorage.setItem('geo_bounds', bounds);
    }

    else if(event.type == 'marker'){
        let position = event.overlay.getPosition()?.toJSON()
        let bounds = [position.lat, position.lng]
        console.log(bounds)
        window.localStorage.setItem('geo_bounds', bounds);
    }

  });

}

window.initMap = initMap