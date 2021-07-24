// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
var infoWindow = null;

// the following is from https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
$(function () {
    $("#datetimepicker1").datetimepicker();
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
var latlng
// get user location and print marker
function showUserLocation(position) {
    lat = position.coords.latitude;
    lon = position.coords.longitude;
    pos = new google.maps.LatLng(lat, lon);
    var myOptions = {
        center: pos,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        navigationControlOptions: {
            style: google.maps.NavigationControlStyle.SMALL
        }
    };
    //map = new google.maps.Map(document.getElementById("map"), myOptions);
    //map.set(document.getElementById("map"),myOptions);
    // set the marker
    //var marker = new google.maps.Marker({position: pos, map: map, title: "You are here!"});
    // from https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse
    latlng = {
        lat: lat,
        lng: lon
    };
    //geocoder
    //.geocode({ location: latlng })
    //.then((response) => {
    //  if (response.results[0]) {
    //      var formatted = response.results[0].formatted_address
    //      formatted = formatted.replace("Co. ", "")
    //      console.log(formatted)
    //
    //  } else {
    //    window.alert("No results found");
    //  }
    //})
    //.catch((e) => window.alert("Geocoder failed due to: " + e));
    document.getElementById("from").value = "CURRENT LOCATION"
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




// the following is based on the code from https://developers.google.com/maps/documentation/javascript/examples/directions-simple#maps_directions_simple-javascript
const directionsService = new google.maps.DirectionsService();
const directionsRenderer = new google.maps.DirectionsRenderer();
const geocoder = new google.maps.Geocoder();

function initMap() {
    const menuI = document.querySelector(".hamburger-menu");

    const navbar = document.querySelector(".navbar");

    menuI.addEventListener("click", () => {
        navbar.classList.toggle("change");
    });
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: {
            lat: 53.3498,
            lng: -6.2603
        },
        styles:[
            {
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#ebe3cd"
                }
              ]
            },
            {
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#523735"
                }
              ]
            },
            {
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#f5f1e6"
                }
              ]
            },
            {
              "featureType": "administrative",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#c9b2a6"
                }
              ]
            },
            {
              "featureType": "administrative.land_parcel",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#dcd2be"
                }
              ]
            },
            {
              "featureType": "administrative.land_parcel",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#ae9e90"
                }
              ]
            },
            {
              "featureType": "landscape.natural",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#dfd2ae"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#dfd2ae"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#93817c"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#a5b076"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "weight": 2
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "labels.text",
              "stylers": [
                {
                  "weight": 3.5
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#447530"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#f5f1e6"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "labels.text",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#fdfcf8"
                }
              ]
            },
            {
              "featureType": "road.arterial",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#f8c967"
                }
              ]
            },
            {
              "featureType": "road.highway.controlled_access",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#e98d58"
                }
              ]
            },
            {
              "featureType": "road.highway.controlled_access",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#db8555"
                }
              ]
            },
            {
              "featureType": "road.local",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#806b63"
                }
              ]
            },
            {
              "featureType": "transit.line",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#dfd2ae"
                }
              ]
            },
            {
              "featureType": "transit.line",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#8f7d77"
                }
              ]
            },
            {
              "featureType": "transit.line",
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#ebe3cd"
                }
              ]
            },
            {
              "featureType": "transit.station",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#dfd2ae"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#b9d3c2"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#92998d"
                }
              ]
            }
          ]
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

function findRoute() {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}


// the following code is based on the google docs documentation from https://developers.google.com/maps/documentation/javascript/directions
function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    console.log("test" + document.getElementById("from").value)
    var datetime = $('#datetimepicker1').data("datetimepicker")["_viewDate"]["_d"]
    console.log(datetime)
    if (document.getElementById("from").value == "CURRENT LOCATION") {
        var request = {
            origin: latlng,
            destination: {
                query: document.getElementById("to").value,
            },
            travelMode: 'TRANSIT',
            transitOptions: {
                departureTime: new Date(datetime),
                modes: ["BUS"]
            }
        };
        console.log(latlng)
        console.log(request)
        directionsService.route(request, function (response, status) {
            if (status == 'OK') {
                console.log(response)
                directionsRenderer.setDirections(response);
            }
        });
    } else {
        // the following is based on the following google documentation https://developers.google.cn/maps/documentation/javascript/examples/directions-simple?hl=zh-cn
        var request = {
            origin: document.getElementById("from").value,
            destination: {
                query: document.getElementById("to").value,
            },
            travelMode: 'TRANSIT',
            transitOptions: {
                departureTime: new Date(datetime),
                modes: ["BUS"]
            }
        };
        console.log(latlng)
        console.log(request)
        directionsService.route(request, function (response, status) {
            if (status == 'OK') {
                console.log(response)
                directionsRenderer.setDirections(response);
            }
        });
    }
}

// the following is based on the code presented in https://www.youtube.com/watch?v=BkGtNBrOhKU also available at https://github.com/sammy007-debug/Google-map-distance-api
//create autocomplete objects for all inputs
var options = {
    componentRestrictions: {
        country: "IE"
    }
}

var input1 = document.getElementById("from");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("to");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);