// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
var infoWindow = null;

function initMap() {
    // The location of Uluru
    const Dublin = { lat: 53.3498, lng: -6.2603 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: Dublin,

});



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

showCurrentWeather();


class AutocompleteDirectionsHandler {
    // we don't need to choose the mode of travel
  map;
  originPlaceId;
  destinationPlaceId;
  directionsService;
  directionsRenderer;
  constructor(map) {
    this.map = map;
    this.originPlaceId = "";
    this.destinationPlaceId = "";
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer();
    this.directionsRenderer.setMap(map);
    const originInput = document.getElementById("origin");
    const destinationInput = document.getElementById("destination");
    const originAutocomplete = new google.maps.places.Autocomplete(originInput);
    // Specify just the place data fields that you need.
    originAutocomplete.setFields(["place_id"]);
    const destinationAutocomplete = new google.maps.places.Autocomplete(
      destinationInput
    );
    // Specify just the place data fields that you need.
    destinationAutocomplete.setFields(["place_id"]);
    this.setupPlaceChangedListener(originAutocomplete, "ORIG");
    this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(origin);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
      destination
    );
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
  }
  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete.
}
}
