ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map("map", {
        center: [55.76, 37.64],
        zoom: 7,
	controls: ['zoomControl', 'fullscreenControl', 'typeSelector']
    });
    buildings.forEach(function(building){
	console.log('NUMBER: ' + building.number);
	console.log('ADDRESS: ' + building.address);
	console.log('FLOORS: ' + building.floors_count);
	ymaps.geocode(building.address, {
            results: 1
	}).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            firstGeoObject.options.set('preset', 'islands#darkBlueDotIconWithCaption');
	    firstGeoObject.properties.set('balloonContentBody', `<a href="/building/${building.number}">Корпус ${building.number}</a>`);
            firstGeoObject.properties.set('iconCaption', building.number);
            myMap.geoObjects.add(firstGeoObject);
	});
    });
}
