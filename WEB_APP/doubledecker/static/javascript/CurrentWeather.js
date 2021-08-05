
//Weather
//SELECT ELEMENTS
const locationEle = locationElement = document.querySelector(".location");
const iconEle = document.querySelector(".weather-icon");
const temperatureEle = document.querySelector(".temperature-value");
const descriptionEle = document.querySelector(".temperature-description");



//APP DATA
const weather = {};
weather.temperature = {
   unit: "celsius"
}

//Get weather from API
//window.onload = function getWeather(){
function ShowCurrentWeather(){

    fetch("/api/ShowCurrentWeather")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            weather.temperature.value = Math.floor(data['temperature']);
            weather.description = data['description'];
            weather.iconId = data['weather_icon'];
            weather.city = 'Dublin City';
            weather.country = 'IE';
            console.log(weather.iconId);
        }).then(function () {
        displayWeather();
    })
}


//DISPLAY WEATHER TO UI
function displayWeather() {
    locationEle.innerHTML = "Dublin";
    iconEle.innerHTML = `<img src="./icons/${weather.iconId}.png"/>`;
    temperatureEle.innerHTML = `${weather.temperature.value}°<span>C</span>`;
    descriptionEle.innerHTML = weather.description;
}

window.onload = function() {
    ShowCurrentWeather();
}
