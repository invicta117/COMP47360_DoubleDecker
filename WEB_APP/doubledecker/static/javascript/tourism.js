// This code origionated from https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Initialize and add the map
var map;
var start_point = [];

console.log(start_point)


function initMap() {
    // nav bar work
    const menuI = document.querySelector(".hamburger-menu");

    const navbar = document.querySelector(".navbar");

    menuI.addEventListener("click", () => {
        navbar.classList.toggle("change");
    });

    // The location of Dublin
    const Dublin = {
        lat: 53.3498,
        lng: -6.2603
    };
    // The map, centered at Uluru
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: Dublin,
    });

}


function showRoute() {
    const cen = {
        lat: 53.3498,
        lng: -6.2603
    };
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: cen,
    });
    if (start_point.length == 0) {
        window.alert("Please Click User Location First" + status);
    }else {
        const directionDisplay = new google.maps.DirectionsRenderer({
            map: this.map
        })
        // get the user select
        const Dname = selectD();
        console.log(Dname)
        let dest = '';
        if (Dname == 'Phoenix Park') {
            dest = 'phoenix park dublin 8'
        }else if (Dname == 'Trinity College') {
            dest = 'Trinity College Dublin, College Green, Dublin 2'
        }else if (Dname == 'Grafton Street') {
            dest = 'Grafton Street'
        }else if (Dname == 'St.stephens') {
            dest = 'St Stephen\'s Green'
        }else if (Dname == 'Howth') {
            dest = 'Howth'
        }else if (Dname == 'National Museum') {
            dest = 'National Museum of Ireland - Archaeology'
        }
        else if (Dname == 'Guinness Storehouse') {
            dest ='Guinness Storehouse, Dublin 8'
        }else if (Dname == 'National Gallery of Ireland') {
            dest = 'National Gallery of Ireland'
        }else if (Dname == 'Merrion Square') {
            dest = 'Merrion Square'
        }else if (Dname == 'GPO Museum') {
            dest = 'GPO Museum'
        }
        console.log(dest)
        const start = new google.maps.LatLng(start_point[0], start_point[1])
        const directionsService = new google.maps.DirectionsService();
        const request = {
            origin: start,
            destination: dest,
            travelMode: 'TRANSIT',
            transitOptions: {
                modes: ["BUS"]
            }
        }
        directionsService.route(request, function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionDisplay.setDirections(response);
            }
        });
    }
}

/**
 * return  destination user select
 */
function selectD() {
    var selectObj = document.getElementById("select2");
    var index = selectObj.selectedIndex;
    var des = selectObj.options[index].value;
    console.log(des);
    return des;
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
    start_point.push(lat);
    start_point.push(lon);

    pos = new google.maps.LatLng(lat, lon);
    // set the marker
    var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: "You are here!"
    });
    const infoWindow = new google.maps.InfoWindow({
        content: "You are here!"
    })
    marker.addListener("click", () => {
        infoWindow.open(map, marker);
    })
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