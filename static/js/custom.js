var map;
var sensors_location_url = '/sensors_data';
var sensors_speed_data_url = '/sensor_speed_data';
var min_latitude = -30.0;
var max_latitude = -33.84967248876616;
var min_longitude = 150.5276435546875;
var max_longitude = 151.2276435546875;

// Create an array to store markers
var markers = {};



function fetchData(min_latitude, max_latitude, min_longitude, max_longitude) {
    // Specify the URL of your DRF endpoint

    var initialStartDate = $('#dateRangePicker').data('daterangepicker').startDate.format('YYYY-MM-DD');
    var initialEndDate = $('#dateRangePicker').data('daterangepicker').endDate.format('YYYY-MM-DD');
    console.log('Current Date Range on Page Load: ' + initialStartDate + ' to ' + initialEndDate);

    // Make the AJAX request using the fetch API
    var query_params = `?min_latitude=${min_latitude}&max_latitude=${max_latitude}&min_longitude=${min_longitude}&max_longitude=${max_longitude}&date=${initialStartDate+"/"+initialEndDate}`;
    fetch(sensors_location_url + query_params)
        .then(response => {
            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            // Process the retrieved data
            if (data.status === 200) {
                // Data retrieval was successful
                const sensorData = data.data;
                // Iterate through the sensor data
                for (const entry of sensorData) {
                    latitudeKey = entry.latitude+"_"+entry.longitude.toString()

                    if (!markers.hasOwnProperty(latitudeKey)){
                        var marker = new google.maps.Marker({
                            position: { lat: entry.latitude, lng: entry.longitude },
                            map: map,
                            title: entry.name
                        });
                        markers[latitudeKey] = marker;

                        marker.addListener('click', function() {
                            fetchSensorSpeedData(entry.name);
                        });
                    }
                }

            } else {
                console.error(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            // Handle any network errors or exceptions
            console.error('Fetch error:', error);
        });
}


function initMap() {
    // Define the map's center and zoom level
    var mapOptions = {
        center: { lat: max_latitude, lng: max_longitude },
        zoom: 10 // Adjust the zoom level as needed
    };

    // Create a new Google Map instance
    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    geocoder = new google.maps.Geocoder();

    const cityDropdown = document.getElementById('cityDropdown');
    cityDropdown.addEventListener('change', updateMapLocation);

    // Add a zoom_changed event listener
    google.maps.event.addListener(map, 'zoom_changed', function() {
        // Get the current zoom level
        const bounds = map.getBounds();
        const ne = bounds.getNorthEast(); // Northeast corner
        const sw = bounds.getSouthWest(); // Southwest corner

        const minLat = sw.lat(); // Minimum Latitude
        const maxLat = ne.lat(); // Maximum Latitude
        const minLng = sw.lng(); // Minimum Longitude
        const maxLng = ne.lng(); // Maximum Longitude

        fetchData(minLat, maxLat, minLng, maxLng);

    });


    // Add a dragend event listener
    google.maps.event.addListener(map, 'dragend', function() {
        // Get the updated center coordinates of the map after panning

        const bounds = map.getBounds();
        const ne = bounds.getNorthEast(); // Northeast corner
        const sw = bounds.getSouthWest(); // Southwest corner

        const minLat = sw.lat(); // Minimum Latitude
        const maxLat = ne.lat(); // Maximum Latitude
        const minLng = sw.lng(); // Minimum Longitude
        const maxLng = ne.lng(); // Maximum Longitude


        fetchData(minLat, maxLat, minLng, maxLng);


    });


}



function updateMapLocation() {
    const cityDropdown = document.getElementById('cityDropdown');
    const selectedCity = cityDropdown.value;

    geocoder.geocode({ address: selectedCity }, function(results, status) {
        if (status === 'OK' && results[0]) {
            map.setCenter(results[0].geometry.location);

            const bounds = map.getBounds();
            const ne = bounds.getNorthEast(); // Northeast corner
            const sw = bounds.getSouthWest(); // Southwest corner

            const minLat = sw.lat(); // Minimum Latitude
            const maxLat = ne.lat(); // Maximum Latitude
            const minLng = sw.lng(); // Minimum Longitude
            const maxLng = ne.lng(); // Maximum Longitude

            fetchData(minLat, maxLat, minLng, maxLng);
        } else {
            console.error('Geocode was not successful for the following reason: ' + status);
        }
    });
}

$('input[name="dateRangePicker"]').daterangepicker();

// Initialize the DateRangePicker
$('#dateRangePicker').daterangepicker({
    startDate: moment().subtract(7, 'days'), // Initial start date
    endDate: moment(), // Initial end date
    ranges: {
        'Last 7 Days': [moment().subtract(7, 'days'), moment()],
        'Last 30 Days': [moment().subtract(30, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    }
});



$('#dateRangePicker').on('apply.daterangepicker', function(ev, picker) {
    var startDate = picker.startDate.format('YYYY-MM-DD');
    var endDate = picker.endDate.format('YYYY-MM-DD');
    console.log('Selected Date Range: ' + startDate + ' to ' + endDate);
    var entries = Object.entries(markers);
    for (var i = 0; i < entries.length; i++) {
        var key = entries[i][0];
        var value = entries[i][1];
        entries[i][1].setMap(null);
    }
    markers = {}
    const bounds = map.getBounds();
    const ne = bounds.getNorthEast(); // Northeast corner
    const sw = bounds.getSouthWest(); // Southwest corner

    const minLat = sw.lat(); // Minimum Latitude
    const maxLat = ne.lat(); // Maximum Latitude
    const minLng = sw.lng(); // Minimum Longitude
    const maxLng = ne.lng(); // Maximum Longitude

    fetchData(minLat, maxLat, minLng, maxLng);
});





function fetchSensorSpeedData(name) {

    var query_params = `?name=${name}`;
    fetch(sensors_speed_data_url + query_params)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 200) {

                const speed_data = data.data;
                // Initialize arrays for each category
                var labels = [];
                var vehicle_speed = [];
                var speed_limit = [];
                var deviation = [];

                // Iterate through the original data and extract values
                speed_data.forEach(function(item) {
                    labels.push(item.timestamp);
                    vehicle_speed.push(item.vehicle_speed);
                    speed_limit.push(item.speed_limit);
                    deviation.push(item.deviation);
                });

                create_sensor_speed_bar_chart(labels, vehicle_speed, speed_limit, deviation);
                console.log(calculateAverage(vehicle_speed));
                console.log(calculateAverage(deviation));
                create_sensor_average_speed_bar_chart(name, calculateAverage(vehicle_speed), calculateAverage(deviation));


            } else {
                console.error(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            // Handle any network errors or exceptions
            console.error('Fetch error:', error);
        });
}


function calculateAverage(arr) {
    if (arr.length === 0) {
        return 0;
    }

    var sum = arr.reduce(function (total, value) {
        return total + value;
    }, 0);

    return sum / arr.length;
}





function create_sensor_speed_bar_chart(labels, vehicle_speed, speed_limit, deviation){

    // Check if a chart with ID 'lineChart' already exists
    const existingChart = Chart.getChart("sensor_speed_bar_char");

    // If an existing chart is found, destroy it
    if (existingChart) {
        existingChart.destroy();
    }

    // Get the canvas element
    var ctx = document.getElementById('sensor_speed_bar_char').getContext('2d');

    var data = {
        labels: labels,
        datasets: [
            {
                label: 'Vehicle Speed',
                backgroundColor: 'blue',
                data: vehicle_speed
            },
            {
                label: 'Speed Limit',
                backgroundColor: 'red',
                data: speed_limit
            },
            {
                label: 'Deviation',
                backgroundColor: 'pink',
                data: deviation
            }
        ]
    };



    var options = {
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true
            }
        }
    };

    // Create the bar chart
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}



function create_sensor_average_speed_bar_chart(labels, average_speed, average_deviation){

    const existingChart = Chart.getChart("sensor_average_speed_bar_char");

    // If an existing chart is found, destroy it
    if (existingChart) {
        existingChart.destroy();
    }

    // Get the canvas element
    var ctx = document.getElementById('sensor_average_speed_bar_char').getContext('2d');

    var data = {
        labels: [labels],
        datasets: [
            {
                label: 'Vehicle Average Speed',
                backgroundColor: '#edc3a0',
                data: [average_speed]
            },
            {
                label: 'Vehicle Average Speed Deviation',
                backgroundColor: 'red',
                data: [average_deviation]
            }
        ]
    };



    var options = {
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true
            }
        }
    };

    // Create the bar chart
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}



initMap();
fetchData(min_latitude, max_latitude, min_longitude, max_longitude);










