// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
function initMap() {
  const directionsService = new google.maps.DirectionsService();
  // The location of Dublin
  const Dublin = { lat: 53.3498, lng: -6.2603 };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: Dublin,
  });
  var listPos = [
    {
      arriveeLat: 53.2864489905228,
      arriveeLng: -6.15989900807043,
      departLat: 53.4173526533912,
      departLng: -6.27853875647111,
    },
    {
      arriveeLat: 53.3996460936412,
      arriveeLng: -6.12803757377896,
      departLat: 53.3505177759176,
      departLng: -6.25626764847559,
    },
  ];
  var bounds = new google.maps.LatLngBounds();
  for (var i = 0; i < listPos.length; i++) {
    var startPoint = new google.maps.LatLng(
      listPos[i]["departLat"],
      listPos[i]["departLng"]
    );
    var endPoint = new google.maps.LatLng(
      listPos[i]["arriveeLat"],
      listPos[i]["arriveeLng"]
    );
    var directionsDisplay = new google.maps.DirectionsRenderer({
      map: map,
      preserveViewport: true,
    });
    calculateAndDisplayRoute(
      directionsService,
      directionsDisplay,
      startPoint,
      endPoint,
      bounds
    );
  }
}

function calculateAndDisplayRoute(
  directionsService,
  directionsDisplay,
  startPoint,
  endPoint,
  bounds
) {
  directionsService.route(
    {
      origin: startPoint,
      destination: endPoint,
      travelMode: "TRANSIT",
    },
    function (response, status) {
      if (status === "OK") {
        console.log(response);
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
      x.innerHTML='your browser not support get the location';
  }
}

// get user location and print marker
function showUserLocation(position) {
lat = position.coords.latitude;
lon = position.coords.longitude;
pos = new google.maps.LatLng(lat, lon);
  var myOptions={
  center:pos,zoom:12,
  mapTypeId:google.maps.MapTypeId.ROADMAP,
  mapTypeControl:false,
  navigationControlOptions:{style:google.maps.NavigationControlStyle.SMALL}
};
  map = new google.maps.Map(document.getElementById("map"),myOptions);
  // map.set(document.getElementById("map"),myOptions);
// set the marker
  var marker = new google.maps.Marker({position:pos,map:map,title:"You are here!"});

}

// handle error
function showError() {
    switch(error.code)
{
  case error.PERMISSION_DENIED:
    x.innerHTML="The user rejected the request for a geographic location."
    break;
  case error.POSITION_UNAVAILABLE:
    x.innerHTML="Location information is not available."
    break;
  case error.TIMEOUT:
    x.innerHTML="Request user location timeout。"
    break;
  case error.UNKNOWN_ERROR:
    x.innerHTML="UNKNOWN_ERROR"
    break;
}
}