// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
var infoWindow = null;



// define a variable that get a button
var x = document.getElementById('userLocation')

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showUserLocation, showError)
    } else {
        x.innerHTML = 'your browser not support get the location';
    }
}

// get user location and print marker
function showUserLocation(position) {
    lat = position.coords.latitude;
    lon = position.coords.longitude;
    pos = new google.maps.LatLng(lat, lon);
    var myOptions = {
        center: pos, zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL}
    };
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    // map.set(document.getElementById("map"),myOptions);
    // set the marker
    var marker = new google.maps.Marker({position: pos, map: map, title: "You are here!"});

    // from https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse
    var latlng = {lat: lat, lng: lon}
    geocoder
    .geocode({ location: latlng })
    .then((response) => {
      if (response.results[0]) {
          var formatted = response.results[0].formatted_address
          formatted = formatted.replace("Co. ", "")
          console.log(formatted)
          document.getElementById("from").value = formatted
      } else {
        window.alert("No results found");
      }
    })
    .catch((e) => window.alert("Geocoder failed due to: " + e));

}

// handle error
function showError() {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            x.innerHTML = "The user rejected the request for a geographic location."
            break;
        case error.POSITION_UNAVAILABLE:
            x.innerHTML = "Location information is not available."
            break;
        case error.TIMEOUT:
            x.innerHTML = "Request user location timeout。"
            break;
        case error.UNKNOWN_ERROR:
            x.innerHTML = "UNKNOWN_ERROR"
            break;
    }
}

function showCurrentWeather() {
  fetch("/api/ShowCurrentWeather")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
        const current = data['current'];
        const temperature = data['temperature'];
        const description = data['description'];
        var doc = document.getElementById('current');
        doc.innerHTML += '<p>' + current + '</p>' + '<p>' + temperature + '</p>' + '<p>' + description + '</p>';
    });
}

showCurrentWeather()


// the following is based on the code from https://developers.google.com/maps/documentation/javascript/examples/directions-simple#maps_directions_simple-javascript
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();
  const geocoder = new google.maps.Geocoder();
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: { lat: 53.3498, lng: -6.2603 },
  });
  directionsRenderer.setMap(map);
  directionsRenderer.setPanel(document.getElementById("sidebar"));


  //const onChangeHandler = function () {
    // calculateAndDisplayRoute(directionsService, directionsRenderer);
  //};
  //document.getElementById("to").addEventListener("change", onChangeHandler);
  //document.getElementById("from").addEventListener("change", onChangeHandler);
}
initMap()

function findRoute(){
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    console.log("test" + document.getElementById("from").value)
  directionsService
    .route({
      origin: {
        query: document.getElementById("from").value,
      },
      destination: {
        query: document.getElementById("to").value,
      },
      travelMode: google.maps.TravelMode.TRANSIT,
    })
    .then((response) => {
        console.log(response)
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions request failed due to " + status));
}

// the following is based on the code presented in https://www.youtube.com/watch?v=BkGtNBrOhKU also available at https://github.com/sammy007-debug/Google-map-distance-api
//create autocomplete objects for all inputs
var options = {
    componentRestrictions: { country: "IE"}
}

var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);
