// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
const listPos=[
];
function initMap() {
  const directionsService = new google.maps.DirectionsService();
  // The location of Dublin
  const Dublin = { lat: 53.3498, lng: -6.2603 };
  // The map, centered at Uluru
   map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: Dublin,
  });

  fetch("/api/route-stops")
      .then((response) => {
          return response.json();
      })
      .then((data) => {
        console.log(data)
          var originDropDown = document.getElementById("start");
          var opt = document.createElement("option");
          // let f_lat = data['stop_lat'][0];
          // let f_lon = data['stop_lon'][0];
          // let l_lat = data['stop_lat'][data['stop_lat'].length -1];
          // let l_lon = data['stop_lon'][data['stop_lon'].length -1];
          let f_lat = 53.3911764950851;
          let f_lon = -6.26219900048751;
          let l_lat = 53.3244315442597;
          let l_lon = -6.21176919149074;
            opt.value= [f_lat,f_lon,l_lat,l_lon]
            // opt.innerHTML = data['route_short_name'][0];
            // originDropDown.add(opt);
            // console.log(opt.value)
        // data.forEach(stop =>{
        //     listPos.push({
        //       key: ["name","lat","lng"],
        //       value: [stop['route_short_name'],stop['stop_lat'],stop['stop_lon']],
        //     })

        // })
        // console.log(listPos)

        const bounds = new google.maps.LatLngBounds();
          const startPoint = new google.maps.LatLng(
            f_lat,
            f_lon
          );
          const endPoint = new google.maps.LatLng(
            l_lat,
            l_lon
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

// const listPos=[{
// }];

// function showStop(){

//   fetch("/api/stop4")
//       .then((response) => {
//           return response.json();
//       })
//       .then((data) => {
//         console.log(data)
//         listPos.arriveeLat = data['stop_lat'][0];
//         listPos.arriveeLng = data['stop_lon'][0];
//         listPos.departLat = data['stop_lat'][data['stop_lat'].length-1];
//         listPos.departLng = data['stop_lon'][data['stop_lat'].length-1];
//         console.log(listPos)
//       })
//       .then(function () {
//         calculateAndDisplayRoute();
//     })
// }
// window.onload = function() {
//   showStop();
// }