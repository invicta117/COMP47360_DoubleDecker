// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 53.3498, lng: -6.2603 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: uluru,
});
// The marker, positioned at Uluru
const marker = new google.maps.Marker({
  position: uluru,
  map: map,
});
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