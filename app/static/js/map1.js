

// function initAutocomplete() {
//         var map = new google.maps.Map(document.getElementById('map'), {
//           center: {lat: -33.8688, lng: 151.2195},
//           zoom: 13,
//           mapTypeId: google.maps.MapTypeId.ROADMAP
//         });

//         // Create the search box and link it to the UI element.
//         var input = document.getElementById('pac-input');
//         var searchBox = new google.maps.places.SearchBox(input);
//         map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

//         // Bias the SearchBox results towards current map's viewport.
//         map.addListener('bounds_changed', function() {
//           searchBox.setBounds(map.getBounds());
//         });

//         var markers = [];
//         // Listen for the event fired when the user selects a prediction and retrieve
//         // more details for that place.
//         searchBox.addListener('places_changed', function() {
//           var places = searchBox.getPlaces();

//           if (places.length == 0) {
//             return;
//           }

//           // Clear out the old markers.
//           markers.forEach(function(marker) {
//             marker.setMap(null);
//           });
//           markers = [];

//           // For each place, get the icon, name and location.
//           var bounds = new google.maps.LatLngBounds();
//           places.forEach(function(place) {
//             var icon = {
//               url: place.icon,
//               size: new google.maps.Size(71, 71),
//               origin: new google.maps.Point(0, 0),
//               anchor: new google.maps.Point(17, 34),
//               scaledSize: new google.maps.Size(25, 25)
//             };

//             // Create a marker for each place.
//             markers.push(new google.maps.Marker({
//               map: map,
//               icon: icon,
//               title: place.name,
//               position: place.geometry.location
//             }));

//             if (place.geometry.viewport) {
//               // Only geocodes have viewport.
//               bounds.union(place.geometry.viewport);
//             } else {
//               bounds.extend(place.geometry.location);
//             }
//           });
//           map.fitBounds(bounds);
//         });
//       }
//       google.maps.event.addDomListener(window, 'load', initAutocomplete);
//       <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAucSUfxFiQtI4imzzPJXoCPfyn6P_9MAs&libraries=places&callback=initAutocomplete"
//         async defer>
//     </script>
      
// Set up some of our variables.
var map; //Will contain map object.
var marker = true;
        
// Function called to initialize / create the map.
// This is called when the page has loaded.      
      
function initMap() {
  // The center location of our map.
    var centerOfMap = new google.maps.LatLng(18.012038939236287, -76.79821014404297);
    // Map options.
    var options = {
      center: centerOfMap, //Set center.
      zoom: 10 //The zoom value.
    };

    // Create the map object.
    map = new google.maps.Map(document.getElementById('map'), options);
        // get the cordinates
        var x = document.getElementById('lat').innerText;
        var y = document.getElementById('lng').innerText;
        var clickedLocation=new google.maps.LatLng(x,y);
        if(marker === true){
            // Create the marker.
            marker = new google.maps.Marker({
                position: clickedLocation,
                map: map,
                draggable: false //make it un-draggable
            });
        }
}

// Load the map when the page has finished loading.
google.maps.event.addDomListener(window, 'load', initMap);