var myMap;
var objectManager;

ymaps.ready().then(function () {
    myMap = new ymaps.Map("map", {
        center: [56.7428, 80.4355],
        zoom: 5,
        type: 'yandex#hybrid',
        controls: ['zoomControl', 'routeEditor', 'rulerControl']
    });

    var clusterIcons = [
        {
            href: '/static/fire_predictor/icons/point.png',
            size: [65, 65],
            offset: [-32.5, -32.5]
        },
        {
            href: '/static/fire_predictor/icons/point.png',
            size: [70, 70],
            offset: [-35, -35]
        },
        {
            href: '/static/fire_predictor/icons/point.png',
            size: [75, 75],
            offset: [-37.5, -37.5]
        }
    ];

    objectManager = new ymaps.ObjectManager({
        clusterize: true,
        gridSize: 30,
        clusterIcons: clusterIcons,
        clusterIconContentLayout: null
    });

    var jsonUrl = '/api/v1/thermal_points';

    // Загружаем термоточки
    $.getJSON(jsonUrl, function (jsonArr) {
        if (!jsonArr.length) {
            return;
        }

        var myGeoObjects = [],
            currentId = 0;

        for (var k in jsonArr) {
            if (!jsonArr[k].hasOwnProperty('ya')
                || !jsonArr[k].hasOwnProperty('yi')
                || !jsonArr[k].hasOwnProperty('xa')
                || !jsonArr[k].hasOwnProperty('xi')
                || !jsonArr[k].hasOwnProperty('fire_status')
                || !jsonArr[k].hasOwnProperty('land_category')
            ) {
                return;
            }

            var item = jsonArr[k];

            var centerOfLat = (item.ya + item.yi) / 2,
                centerOfLon = (item.xa + item.xi) / 2;

            var iconName = item.fire_status === 'BRN' ? 'point.png' : 'loc.png';

            myGeoObjects.push({
                type: 'Feature',
                id: currentId++,
                geometry: {
                    type: 'Point',
                    coordinates: [
                        centerOfLat,
                        centerOfLon
                    ],
                },
                options: {
                    iconLayout: 'default#image',
                    iconImageHref: '/static/fire_predictor/icons/' + iconName,
                    iconImageSize: [22, 22],
                    iconImageOffset: [-11, -11],
                    custom: {
                        id: item.id,
                        fire_status: item.fire_status,
                        land_category: item.land_category,
                        date_added: item.date_added,
                        nearest_city_distance: item.nearest_city_distance,
                        city: item.city,
                        county: item.county,
                        state: item.state,
                    }
                }
            });
        }

        // точки в менеджер объектов для отрисовки
        objectManager.add(myGeoObjects);

        //objectManager.add(myGeoObjects);
        myMap.geoObjects.add(objectManager);

        myMap.container.fitToViewport();
        myMap.setBounds(myMap.geoObjects.getBounds(), {
            checkZoomRange: true
        });
    });

    // Загружаем скорость и направления ветра с метеостанций
    jsonUrl = 'http://localhost:88/';

    // Создание метки с круглой активной областью.
    var windLayer = '<div class="placemark_layout_container">' +
        '   <div class="rounded_corners_box_layout">' +
        '       <div><img ' +
        '               src="/static/fire_predictor/icons/arrow.svg" ' +
        '               class="wind-direction-arrow" ' +
        '               style="transform: rotate({{ properties.custom.rotate }}deg); -webkit-transform:rotate({{ properties.custom.rotate }}deg);">' +
        '       </div>' +
        '       <div>{{ properties.custom.wind_speed }} мс</div>' +
        '       <div>{{ properties.custom.temperature }} &deg;</div>' +
        '   </div>' +
        '</div>';
    var circleLayout = ymaps.templateLayoutFactory.createClass(windLayer);

    $.getJSON(jsonUrl, function (jsonArr) {
        if (!jsonArr.length) {
            return;
        }

        for (var k in jsonArr) {
            if (!jsonArr[k].hasOwnProperty('wind_direction')
                || !jsonArr[k].hasOwnProperty('wind_speed')
                || !jsonArr[k].hasOwnProperty('temperature')
                || !jsonArr[k].hasOwnProperty('source')
                || !jsonArr[k].hasOwnProperty('lat')
                || !jsonArr[k].hasOwnProperty('lon')
            ) {
                return;
            }

            var item = jsonArr[k];

            /*layout = layout.replace('{wind_speed}', item.wind_speed);
            layout = layout.replace('{temperature}', item.temperature);*/

            var circlePlacemark = new ymaps.Placemark(
                [item.lat, item.lon], {
                    hintContent: item.wind_direction + ', ' + item.wind_speed + ' м/с',
                    custom: {
                        wind_speed: item.wind_speed,
                        temperature: item.temperature,
                        rotate: arrowRotationByWindDirection(item.wind_direction)
                    }
                }, {
                    iconLayout: circleLayout,
                    iconShape: {
                        type: 'Circle',
                        coordinates: [0, 0],
                        radius: 25
                    }
                }
            );
            myMap.geoObjects.add(circlePlacemark);
        }
    });

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        console.log(coords[0].toPrecision(6), coords[1].toPrecision(6))
    });

    myMap.events.add('boundschange', function () {
        // После каждого сдвига карты будем смотреть, какие объекты попадают в видимую область.
        refreshVisibleList();
    });

    // сразу смотрим, какие объекты попадают на карту
    refreshVisibleList();
});

function refreshVisibleList() {
    setTimeout(function () {
        var objects = objectManager.objects.getAll(),
            visibleObjectsHtml = [];

        objects.forEach(function (object) {
            // Получим данные о состоянии объекта внутри кластера.
            var objectState = objectManager.getObjectState(object.id);

            // Проверяем, находится ли объект в видимой области карты.
            if (objectState.found && objectState.isShown) {
                if (!object.options.custom) {
                    return;
                }

                visibleObjectsHtml.push(buildListItem(object.options.custom));
            }
        });

        // Обновляем список.
        var visibleElement = document.getElementById('pointsList');
        visibleElement.innerHTML = visibleObjectsHtml.join('');
    }, 100)
}

function buildListItem(props) {
    var definition = landCategoryDefinition(props.land_category);

    var date = new Date(props.date_added);

    var options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
    };

    var nearestLocation = null,
        distance = null;

    if (props.nearest_city_distance !== null && props.city.length) {
        if (props.nearest_city_distance >= 1) {
            distance = Math.round(props.nearest_city_distance) + ' км';
        } else {
            distance = Math.round(props.nearest_city_distance * 1000) + ' м';
        }

        nearestLocation = 'В ' + distance + ' ' + props.city;
    }

    return '<div class="point priority-' + definition.priority + '">' +
        '<div>Точка ' + props.id + '<br> <span>' + date.toLocaleString("ru", options) + '</span></div>' +
        '<div>' + definition.title + '</div>' +
        '<div>' +
        '   <div' + (props.fire_status === 'BRN' ? ' class="burning"' : '') + '>' + (props.fire_status === 'BRN' ? 'Горит' : 'Потушен') + '</div>' +
        (props.nearest_city_distance !== null ? '<div>' + nearestLocation + '</div>' : '') +
        '</div>' +
        '</div>';
}

function landCategoryDefinition(category) {
    let landCategoryTitle = 'Категория не установлена';
    let landCategoryPriority = 5;

    if (category === '003001000000') {
        landCategoryTitle = 'Земли сельскохозяйственного назначения';
        landCategoryPriority = 2;
    }
    if (category === '003002000000') {
        landCategoryTitle = 'Земли населённых пунктов';
        landCategoryPriority = 1;
    } else if (category === '003003000000') {
        landCategoryTitle = 'Земли промышленности, энергетики, транспорта, связи, ' +
            'радиовещания, телевидения, информатики, земли для обеспечения космической деятельности, ' +
            'земли обороны, безопасности и земли иного специального назначения';
        landCategoryPriority = 1;
    } else if (category === '003004000000') {
        landCategoryTitle = 'Земли особо охраняемых территорий и объектов';
        landCategoryPriority = 1;
    } else if (category === '003005000000') {
        landCategoryTitle = 'Земли лесного фонда';
        landCategoryPriority = 3;
    } else if (category === '003006000000') {
        landCategoryTitle = 'Земли водного фонда';
        landCategoryPriority = 4;
    } else if (category === '003007000000') {
        landCategoryTitle = 'Земли запаса';
        landCategoryPriority = 4;
    } else if (category === '003008000000') {
        landCategoryTitle = 'Категория не установлена';
        landCategoryPriority = 5;
    }

    return {
        'title': landCategoryTitle,
        'priority': landCategoryPriority,
    }
}

function arrowRotationByWindDirection(directionStr) {
    directionStr = directionStr.toLowerCase();

    if (directionStr === 'северный') {
        return 90;
    } else if (directionStr === 'северо-западный') {
        return 45;
    } else if (directionStr === 'северо-восточный') {
        return 135;
    } else if (directionStr === 'южный') {
        return 270;
    } else if (directionStr === 'юго-восточный') {
        return 315;
    } else if (directionStr === 'юго-западный') {
        return 225;
    } else if (directionStr === 'западный') {
        return 0;
    } else if (directionStr === 'восточный') {
        return 180;
    }
}
