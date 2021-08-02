// This code origionated from https://developers.google.com/maps/documentation/javascript/examples/directions-waypoints#maps_directions_waypoints-javascript
// Initialize and add the map

var colors = ["#0000ff", "#00ff00", "#ff0000", "#000000"]
var directionsdivs = ["directions1", "directions2", "directions3", "directions4"]
var hiddencontainers = ['#hiddencontainer1', '#hiddencontainer2', '#hiddencontainer3', '#hiddencontainer4']
var routeids = ["#route1", "#route2", "#route3", "#route4"]
var tourism = ["tourism1", "tourism2", "tourism3", "tourism4"]
var directionsDisplays = [];
var map;

function initMap() {
    var directionsService = new google.maps.DirectionsService();
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: {
            lat: 53.3498,
            lng: -6.2603
        }
    });
    for (var i = 0; i < 4; i++) {
        var directionsDisplay = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {strokeColor: colors[i]},
        });
        directionsDisplay.setPanel(document.getElementById(directionsdivs[i]));
        directionsDisplays.push(directionsDisplay)
    }
    var submit = document.getElementById("submit")
    submit.addEventListener("click", () => {
        var o = document.getElementById("start").value
        var o_text = document.getElementById("start").selectedOptions[0].text
        $(".hiddencontainer").hide()
        var previous = o;
        var previous_text = o_text;
        var destinations = document.getElementsByClassName("waypoints")
        var departure = Date.now()
        console.log(destinations)
        for (var i = 0; i < destinations.length; i++) {
            var d = destinations[i].value
            var d_text = destinations[i].selectedOptions[0].text
            $(routeids[i]).html(previous_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[i] + '"></i> ' + d_text)
            departure = calculateAndDisplayRoute(directionsService, directionsDisplays[i], previous, d, departure);
            previous = d;
            previous_text = d_text;
            $(hiddencontainers[i]).show()
        }
        console.log(d + ' <i class=\"bi bi-arrow-right\" id="' + tourism[i] + '"></i> ' + o)
        calculateAndDisplayRoute(directionsService, directionsDisplays[3], d, o, departure);
        $("#route4").html(d_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[3] + '"></i> ' + o_text)
        $('#hiddencontainer4').show()
        showRoute(0)
        document.getElementById("search").open = false;
    });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, origin, destination, departure) {

    directionsService
        .route({
            origin: origin,
            destination: destination,
            travelMode: 'TRANSIT',
            transitOptions: {
                departureTime: new Date(departure),
                modes: ["BUS"]
            }
        })
        .then((response) => {
            console.log(response)
            directionsRenderer.setDirections(response);
            // get the arrival time
            return addHour(response["routes"][response["routes"].length - 1]["legs"][[response["routes"][response["routes"].length - 1]["legs"].length - 1]].arrival_time.value)
        })
        .catch((e) => window.alert("Directions request failed due to " + status));
    return addHour(departure)
}

function addHour(time) { // from https://stackoverflow.com/questions/1050720/adding-hours-to-javascript-date-object
    time = new Date(time)
    return time.setHours(time.getHours() + 1);
}

function addStop() {

    var max_stops = 3;
    var number_stops = document.getElementsByClassName("waypoints").length
    if (number_stops < max_stops) {
        console.log("adding stop")
        $('#waypoint-stops').append('<div><select class="waypoints">\n' +
            '<option value="Phoenix Park, Dublin 8, Ireland">Phoenix Park</option>\n' +
            '<option value="National Museum of Ireland - Archaeology, Kildare Street, Dublin 2, Ireland">National Museum of Ireland</option>\n' +
            '<option value="Guinness Storehouse, Saint Catherine\'s, Dublin 8, Ireland">Guinness Storehouse</option>\n' +
            '<option value="Howth, Dublin, Ireland">Howth</option>\n' +
            '<option value="Dun Laoghaire Harbour, Dún Laoghaire, Dublin, Ireland">Dun Laoghaire Harbour</option>\n' +
            '</select><p class="remove"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle" viewBox="0 0 16 16">\n' +
            '  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>\n' +
            '  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>\n' +
            '</svg></p></div>');
    }
}

function showRoute(i) {
    for (var d = 0; d < 4; d++) {
        if (d == i) {
            directionsDisplays[i].setMap(map)
        } else {
            directionsDisplays[d].setMap(null)
        }
    }
}


// the following is from https://stackoverflow.com/questions/31455020/jquery-parent-remove-is-not-working
$(document).on('click', '.remove', function () {
    $(this).parent().remove();
});