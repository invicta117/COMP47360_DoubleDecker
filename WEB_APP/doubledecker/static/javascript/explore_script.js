// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
const listPos=[
];
const route_name = []


function initMap() {
  const directionsService = new google.maps.DirectionsService();
  // The location of Dublin
  const Dublin = { lat: 53.3498, lng: -6.2603 };
  // The map, centered at Uluru
   map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: Dublin,
  });


  fetch("/api/route-line")
      .then((response) => {
          return response.json();
      })
      .then((data) => {

        // console.log(data)
        document.getElementById("myBtn").addEventListener("click", function(){
          let routeID = []
        r = document.getElementById("searchTxt").value;
        data.forEach(route =>{
          if(route.route_short_name == r)
          {
            routeID.push(route.shape_pt_sequence,
              route.route_short_name,
              route.route_id,
              route.shape_pt_lat, 
              route.shape_pt_lon)
          }

          })
          console.log("routeID:",routeID)
          const stop1 = routeID.slice(0, 5);
          console.log(stop1)
          const stoplast = routeID.slice(-5);
          console.log(stoplast)

          listPos.push({
            key: ["f_lat","f_lng","l_lat", "l_lng"],
            value: [stop1[3],stop1[4],stoplast[3],stoplast[4]],
          })

        console.log(listPos)
        // console.log(listPos[0].value[0])
        // this here is the function which works out the distance of the way points
        for (var i =0; i<listPos.length;i++){
          const bounds = new google.maps.LatLngBounds();
          const startPoint = new google.maps.LatLng(
            listPos[i].value[0],
            listPos[i].value[1]
          );
          const endPoint = new google.maps.LatLng(
            listPos[i].value[2],
            listPos[i].value[3]
          );
      
          const directionsDisplay = new google.maps.DirectionsRenderer({
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
      });

      
    })

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