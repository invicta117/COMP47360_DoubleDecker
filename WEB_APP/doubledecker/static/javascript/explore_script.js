function initMap() {
    // The location of Uluru
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