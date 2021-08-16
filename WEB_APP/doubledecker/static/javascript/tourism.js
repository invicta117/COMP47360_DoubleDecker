// This code origionated from https://developers.google.com/maps/documentation/javascript/examples/directions-waypoints#maps_directions_waypoints-javascript
// Initialize and add the map

var colors = ["#0000ff", "#00ff00", "#ff0000", "#000000"]
var directionsdivs = ["directions1", "directions2", "directions3", "directions4"]
var hiddencontainers = ['#hiddencontainer1', '#hiddencontainer2', '#hiddencontainer3', '#hiddencontainer4']
var routeids = ["#route1", "#route2", "#route3", "#route4"]
var tourism = ["tourism1", "tourism2", "tourism3", "tourism4"]
var directionsDisplays = [];
var markersDisplays = [];
var map;
var pos;

var places = {
    "attraction":
        {
            0: {
                "name": 'National Museum of Ireland',
                "address": "National Museum of Ireland - Archaeology, Kildare Street, Dublin 2, Ireland",
                "lat": 53.34024334788384,
                "lng": -6.254841710382612,
            },
            1: {
                "name": 'Guinness Storehouse',
                "address": "Guinness Storehouse, Saint Catherine\'s, Dublin 8, Ireland",
                "lat": 53.341785814004886,
                "lng": -6.286732559527315,
            },
            2: {
                "name": 'Howth',
                "address": "Howth, Dublin, Ireland",
                "lat": 53.379913165900405,
                "lng": -6.057499107605555
            }
        },
    "food": {
        0: {
            "name": 'Spitalfields',
            "address": "Spitalfields, The Coombe, Merchants Quay, Dublin 8",
            "lat": 53.3398813383553,
            "lng": -6.275718359527415
        },
        1: {
            "name": 'Wing\'s World Cuisine',
            "address": "Wing's World Cuisine, Wolfe Tone Street, North City, Dublin",
            "lat": 53.34903370674537,
            "lng": -6.26773869021117
        },
        2: {
            "name": 'PHX Bistro',
            "address": "PHX Bistro, Ellis Quay, Smithfield, Dublin",
            "lat": 53.347092589476155,
            "lng": -6.281589528843021
        },
    }
}

function initMap() {
    var directionsService = new google.maps.DirectionsService();
    var infoWindow = new google.maps.InfoWindow();

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: {
            lat: 53.3498,
            lng: -6.2603
        }
    });

    for (var i = 0; i < 4; i++) {
        var directionsDisplay = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {strokeColor: colors[i]},
            suppressMarkers: true,
        });
        var marker = new google.maps.Marker({
            position: {lat: 53.34943864163513, lng: -6.260527882816787},
            map: null,
            label: {color: '#ffffff', text: String.fromCharCode('A'.charCodeAt() + i)} // from char code from https://stackoverflow.com/questions/12504042/what-is-a-method-that-can-be-used-to-increment-letters/34483399
        });

        directionsDisplay.setPanel(document.getElementById(directionsdivs[i]));
        directionsDisplays.push(directionsDisplay)
        markersDisplays.push(marker)
    }
    markersDisplays[0].setMap(map)
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
            },
            () => {
                handleLocationError(true, infoWindow, map.getCenter());
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    var start = document.getElementById("start")
    start.addEventListener("change", async () => {
        var o = document.getElementById("start").value
        if (o == "General Post Office, Dublin, O'Connell Street Lower, North City, Dublin 1, Ireland") {
            reset()
            markersDisplays[0].setPosition({lat: 53.34943864163513, lng: -6.260527882816787})
            map.panTo({lat: 53.34943864163513, lng: -6.260527882816787})
            markersDisplays[0].setMap(map)
        } else {
            reset()
            markersDisplays[0].setPosition({lat: pos.lat, lng: pos.lng})
            map.panTo({lat: pos.lat, lng: pos.lng})
            markersDisplays[0].setMap(map)
        }
        //console.log("change")
    })


    var submit = document.getElementById("submit")
    submit.addEventListener("click", async () => {

            var o = document.getElementById("start").value
            if (o != "General Post Office, Dublin, O'Connell Street Lower, North City, Dublin 1, Ireland") {
                o = new google.maps.LatLng(pos.lat, pos.lng)
            }
            var complete_route = ""
            var o_text = document.getElementById("start").selectedOptions[0].text
            $(".hiddencontainer").hide()
            var previous = o;
            //console.log("this is the current position" + previous)
            var previous_text = o_text;
            var destinations = document.getElementsByClassName("waypoints")
            var random_destinations = [];
            for (var i = 0; i < destinations.length; i++) {
                var d = destinations[i].value
                //console.log(places[d])
                var place = places[d][Math.floor(Math.random() * Object.keys(places[d]).length)] // random comes from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
                while (random_destinations.indexOf(place) != -1) {
                    place = places[d][Math.floor(Math.random() * Object.keys(places[d]).length)] // random comes from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
                }
                random_destinations.push(place)
            }

            var departure = $('#datetimepicker1').data("datetimepicker")["_viewDate"]["_d"]
            //console.log(destinations)
            for (var i = 0; i < random_destinations.length; i++) {
                var d = random_destinations[i].address
                //console.log(d)
                var d_text = random_destinations[i].name
                var route_text = previous_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[i] + '"></i> ' + d_text
                $(routeids[i]).html(route_text)
                complete_route = complete_route + previous_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[i] + '"></i> '
                departure = await calculateAndDisplayRoute(directionsService, directionsDisplays[i], previous, d, departure);
                //console.log(departure)
                if (departure == null) {
                    break
                }
                //console.log(random_destinations[i].lat + " " + random_destinations[i].lng)
                markersDisplays[i + 1].setPosition({lat: random_destinations[i].lat, lng: random_destinations[i].lng})
                markersDisplays[i + 1].setMap(map)
                previous = d;
                previous_text = d_text;
                $(hiddencontainers[i]).show()
            }
            if (departure == null) {
                //console.log("warning no directions available")
                $("#route4").html("No route available please try another start location")
            } else {
                //console.log(d + ' <i class=\"bi bi-arrow-right\" id="' + tourism[i] + '"></i> ' + o)
                calculateAndDisplayRoute(directionsService, directionsDisplays[3], d, o, departure);
                $("#route4").html(d_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[3] + '"></i> ' + o_text)
                complete_route = complete_route + d_text + ' <i class=\"bi bi-arrow-right\" id="' + tourism[3] + '"></i> ' + o_text
                //showRoute(0)
                document.getElementById("complete-route").innerHTML = complete_route
                showAllRoutes()
            }
            $('#hiddencontainer4').show()
        }
    );
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, origin, destination, departure) {
    //console.log("origin" + origin)
    //console.log("destination" + destination)
    var request = {
        origin: origin,
        destination: destination,
        travelMode: 'TRANSIT',
        transitOptions: {
            departureTime: new Date(departure),
            modes: ["BUS"]
        }
    };
    var result = directionsService.route(request, function (response, status) {
        //console.log(response)
        if (status == 'OK') {
            directionsRenderer.setDirections(response);
            if (Object.keys(response["routes"][response["routes"].length - 1]["legs"][[response["routes"][response["routes"].length - 1]["legs"].length - 1]]).includes("arrival_time")) {
                return addHour(response["routes"][response["routes"].length - 1]["legs"][[response["routes"][response["routes"].length - 1]["legs"].length - 1]].arrival_time.value)
            }
            return addHour(departure)
        }
    }).catch(e => {
        return null
    });
    ;
    return result
}

function addHour(time) { // from https://stackoverflow.com/questions/1050720/adding-hours-to-javascript-date-object
    time = new Date(time)
    return time.setHours(time.getHours() + 1);
}

function addStop() {
    var max_stops = 3;
    var number_stops = document.getElementsByClassName("waypoints").length
    if (number_stops < max_stops) {
        //console.log("adding stop")
        $('#waypoint-stops').append('<div><select class="waypoints">\n' +
            '<option value="attraction">Attraction</option>\n' +
            '<option value="food">Food</option>\n' +
            '</select></div>');
    }
}

function removeStop() {
    var min_stops = 1;
    var number_stops = document.getElementsByClassName("waypoints").length
    if (number_stops > min_stops) {
        document.getElementsByClassName("waypoints")[number_stops - 1].remove();
    }
}

function showAllRoutes() {
    for (var i = 0; i < 4; i++) {
        directionsDisplays[i].setMap(map)

    }
}

function reset() {
    document.getElementById("complete-route").innerHTML = ''
    $(".hiddencontainer").hide()
    for (var d = 0; d < 4; d++) {
        directionsDisplays[d].setMap(null)
        markersDisplays[d].setMap(null)
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
// the following implementation of how to close detail tags is from https://stackoverflow.com/questions/16751345/automatically-close-all-the-other-details-tags-after-opening-a-specific-detai/56194608
    var details = document.querySelectorAll("details");
    details.forEach((target) => {
        target.addEventListener("click", () => {
            details.forEach((detail) => {
                if (detail !== target) {
                    detail.open = false;
                }
            });
        });
    });
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

// the following is from https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
$(function () {
    $("#datetimepicker1").datetimepicker();
});