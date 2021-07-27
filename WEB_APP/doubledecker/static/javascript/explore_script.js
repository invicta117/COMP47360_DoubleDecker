// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
const listPos = [];
const route_name = [];
var directionsDisplays,
  directionsService;


function initMap() {

  // nav bar work
  const menuI = document.querySelector(".hamburger-menu");
  const navbar = document.querySelector(".navbar");
  menuI.addEventListener("click", () => {
    navbar.classList.toggle("change");
  });

  // google service for route and map displays
  directionsService = new google.maps.DirectionsService();
  directionsDisplays = new Array();
  // The location of Dublin
  const Dublin = {
    lat: 53.3498,
    lng: -6.2603
  };
  // The map, centered at Uluru
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: Dublin,
    styles: [{
        "elementType": "geometry",
        "stylers": [{
          "color": "#ebe3cd"
        }]
      },
      {
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#523735"
        }]
      },
      {
        "elementType": "labels.text.stroke",
        "stylers": [{
          "color": "#f5f1e6"
        }]
      },
      {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#c9b2a6"
        }]
      },
      {
        "featureType": "administrative.land_parcel",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#dcd2be"
        }]
      },
      {
        "featureType": "administrative.land_parcel",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#ae9e90"
        }]
      },
      {
        "featureType": "landscape.natural",
        "elementType": "geometry",
        "stylers": [{
          "color": "#dfd2ae"
        }]
      },
      {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [{
          "color": "#dfd2ae"
        }]
      },
      {
        "featureType": "poi",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#93817c"
        }]
      },
      {
        "featureType": "poi.park",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#a5b076"
        }]
      },
      {
        "featureType": "poi.park",
        "elementType": "labels.icon",
        "stylers": [{
          "weight": 2
        }]
      },
      {
        "featureType": "poi.park",
        "elementType": "labels.text",
        "stylers": [{
          "weight": 3.5
        }]
      },
      {
        "featureType": "poi.park",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#447530"
        }]
      },
      {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [{
          "color": "#f5f1e6"
        }]
      },
      {
        "featureType": "road",
        "elementType": "labels.text",
        "stylers": [{
          "visibility": "off"
        }]
      },
      {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [{
          "color": "#fdfcf8"
        }]
      },
      {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [{
          "visibility": "off"
        }]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [{
          "color": "#f8c967"
        }]
      },
      {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry",
        "stylers": [{
          "color": "#e98d58"
        }]
      },
      {
        "featureType": "road.highway.controlled_access",
        "elementType": "geometry.stroke",
        "stylers": [{
          "color": "#db8555"
        }]
      },
      {
        "featureType": "road.local",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#806b63"
        }]
      },
      {
        "featureType": "transit.line",
        "elementType": "geometry",
        "stylers": [{
          "color": "#dfd2ae"
        }]
      },
      {
        "featureType": "transit.line",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#8f7d77"
        }]
      },
      {
        "featureType": "transit.line",
        "elementType": "labels.text.stroke",
        "stylers": [{
          "color": "#ebe3cd"
        }]
      },
      {
        "featureType": "transit.station",
        "elementType": "geometry",
        "stylers": [{
          "color": "#dfd2ae"
        }]
      },
      {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [{
          "color": "#b9d3c2"
        }]
      },
      {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [{
          "color": "#92998d"
        }]
      }
    ]
  });
  document.getElementById("myBtn").addEventListener("click", function () {
    const route_short_name = document.getElementById("searchTxt").value;

    fetch("/api/stations/?station=" + route_short_name )
      .then((response) => {
        return response.json();
      })
      .then((data) => {

        listPos.pop();
        stop1 = data[0];
        stoplast = data[data.length-1];
        console.log(stop1,stoplast)
        listPos.push({
          key: [route_short_name],
          value: [stop1.stop_lat, stop1.stop_lon, stoplast.stop_lat, stoplast.stop_lon],
        })

        console.log("list of positions:", listPos)
        // console.log(listPos[0].value[0])
        // this here is the function which works out the distance of the way points
        for (var i = 0; i < listPos.length; i++) {
          bounds = new google.maps.LatLngBounds();
          startPoint = new google.maps.LatLng(
            listPos[i].value[0],
            listPos[i].value[1]
          );
          endPoint = new google.maps.LatLng(
            listPos[i].value[2],
            listPos[i].value[3]
          );

          directionsDisplay = new google.maps.DirectionsRenderer({
            map: map,
          });
          calculateAndDisplayRoute(
            directionsService,
            directionsDisplay,
            startPoint,
            endPoint,
            bounds
          );
        }
        directionsDisplays.push(directionsDisplay);
        console.log("I am directions array", directionsDisplays)

      });

  })

}
console.log("this is outside:", listPos)

function clearItem() {
  // Clean previous routes
  for (var i = 0; i < directionsDisplays.length; i++) {
    console.log(directionsDisplays)
    directionsDisplays[i].setMap(null);
  }
  directionsDisplays.pop();
  listPos.pop();
  // console.log(`I am directions array after ${directionsDisplays}`);
}

function clearAll() {
  location.reload();
}

function calculateAndDisplayRoute(
  directionsService,
  directionsDisplay,
  startPoint,
  endPoint,
  bounds
) {
  directionsService.route({
      origin: startPoint,
      destination: endPoint,
      travelMode: "TRANSIT",
    },
    function (response, status) {
      if (status === "OK") {
        console.log("I am response: ", response);
        directionsDisplay.setDirections(response);
        bounds.union(response.routes[0].bounds);
        map.fitBounds(bounds);
      } else {
        window.alert("Impossible d afficher la route " + status);
      }
    }
  );
}

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
    center: pos,
    zoom: 12,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    mapTypeControl: false,
    navigationControlOptions: {
      style: google.maps.NavigationControlStyle.SMALL
    }
  };
  map = new google.maps.Map(document.getElementById("map"), myOptions);
  // map.set(document.getElementById("map"),myOptions);
  // set the marker
  var marker = new google.maps.Marker({
    position: pos,
    map: map,
    title: "You are here!"
  });

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