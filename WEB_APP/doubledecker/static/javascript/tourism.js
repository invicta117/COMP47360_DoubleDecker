// This code origionated from https://developers.google.com/maps/documentation/javascript/examples/directions-waypoints#maps_directions_waypoints-javascript
// Initialize and add the map

var colors = ["#0000ff", "#00ff00", "#ff0000", "#000000"]
var directionsdivs = ["directions1", "directions2", "directions3"]
var hiddencontainers = ['#hiddencontainer1', '#hiddencontainer2', '#hiddencontainer3', '#hiddencontainer4']
var routeids = ["#route1", "#route2", "#route3", "#route4"]

function initMap() {
    var directionsService = new google.maps.DirectionsService();

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 6,
        center: {lat: 41.85, lng: -87.65},
    });

    var submit = document.getElementById("submit")
    submit.addEventListener("click", () => {
        var o = document.getElementById("start").value
        $(".hiddencontainer").hide()
        var previous = o;
        var destinations = document.getElementsByClassName("waypoints")
        console.log(destinations)
        for (var i = 0; i < destinations.length; i++) {
            var d = destinations[i].value
            var directionsDisplay = new google.maps.DirectionsRenderer({
                map: map,
                polylineOptions: {strokeColor: colors[i]},
                suppressMarkers: true
            });
            directionsDisplay.setPanel(document.getElementById(directionsdivs[i]));
            $(routeids[i]).html(previous + " -to- " + d)
            calculateAndDisplayRoute(directionsService, directionsDisplay, previous, d);
            previous = d;
            $(hiddencontainers[i]).show()
        }
        console.log(d + " -to- " + o)
        var directionsDisplay = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {strokeColor: colors[3]},
            suppressMarkers: true
        });
        directionsDisplay.setPanel(document.getElementById("directions4"));
        calculateAndDisplayRoute(directionsService, directionsDisplay, d, o);
        $("#route4").html(d + " - to- " + o)
        $('#hiddencontainer4').show()
    });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, origin, destination) {
    const waypts = [];
    const checkboxArray = document.getElementsByClassName("waypoints");

    directionsService
        .route({
            origin: origin,
            destination: destination,
            //waypoints: waypts,
            travelMode: 'TRANSIT',
            transitOptions: {
                modes: ["BUS"]
            }
        })
        .then((response) => {
            console.log(response)
            directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + status));
}

function addStop() {

    var max_stops = 3;
    var number_stops = document.getElementsByClassName("waypoints").length
    if (number_stops < max_stops) {
        console.log("adding stop")
        $('#waypoint-stops').append('<div><select class="waypoints">\n' +
            '                            <option value="Phoenix Park, Dublin 8, Ireland">Phoenix Park</option>\n' +
            '                            <option value="Trinity College, College Green, Dublin 2, Ireland">Trinity College</option>\n' +
            '                        </select><p class="remove"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">\n' +
            '  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>\n' +
            '  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>\n' +
            '</svg></p></div>');
    }
}

// the following is from https://stackoverflow.com/questions/31455020/jquery-parent-remove-is-not-working
$(document).on('click', '.remove', function () {
    $(this).parent().remove();
});