//show the weather info when load the page
const locationEle = document.querySelector(".location");
const iconEle = document.querySelector(".weatherIcon");
const temperatureEle = document.querySelector(".temperature p");
const descriptionEle = document.querySelector(".description p");

//Create the empty weather object
const weather = {};

//Define the temperature units
weather.temperature = {
    unit: "celcius"
}

function showCurrentWeather() {
    fetch("/api/ShowCurrentWeather")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            weather.temperature.value = Math.floor(data['temperature'] - 273);
            weather.description = data['description'];
            weather.iconId = data['weather_icon'];
            weather.city = 'Dublin City';
            weather.country = 'IE';
        }).then(function () {
        renderPage();
    })
}

function renderPage() {
    locationEle.innerHTML = `${weather.city}, ${weather.country}`;
    iconEle.innerHTML = `<img src="static/icons/${weather.iconId}.png"/>`;
    temperatureEle.innerHTML = `${weather.temperature.value}°<span>C</span>`;
    descriptionEle.innerHTML = weather.description;
}



window.onload = function () {
  showCurrentWeather();
};