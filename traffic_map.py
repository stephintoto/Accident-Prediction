<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Traffic Accident Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <!-- FontAwesome for icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <!-- Leaflet CSS for Map -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body onload="initializeSidebar()">
    <div class="d-flex">
        <!-- Sidebar -->
        <div id="sidebar" class="sidebar bg-light collapsed">
            <button class="btn toggle-btn" onclick="toggleSidebar()" title="Toggle Sidebar">
                <i class="fas fa-bars"></i>
            </button>
            <div class="sidebar-content">
                <ul class="nav flex-column mt-5"><!-- Increased margin-top to move Home icon lower -->
                    <li class="nav-item">
                        <a class="nav-link text-dark" href="/">
                            <i class="fas fa-home"></i>
                            <span class="nav-text">Home</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-dark" href="/severity-prediction">
                            <i class="fas fa-thermometer-half"></i>
                            <span class="nav-text">Severity Prediction</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-dark" href="/time-range-prediction">
                            <i class="fas fa-clock"></i>
                            <span class="nav-text">Peak Time Prediction</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-dark" href="/about">
                            <i class="fas fa-info-circle"></i>
                            <span class="nav-text">About</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Main content -->
        <div id="content" class="content p-4">
            <header class="mb-4">
                <h1 class="display-4 text-primary">Welcome to Traffic Accident Analysis</h1>
                <p class="lead text-muted">Explore insights, predict accident trends, and analyze traffic accident data.</p>
            </header>
            <body>
                <div class="container">
                    <!-- Header Section -->
                    <header class="text-center mt-5">
                        <h1>Accidents Dashboard</h1>
                    </header>
            
                    <!-- Three Data Cards Section -->
                    <section class="row mt-4">
                        <!-- Card 1: Number of Accidents -->
                        <div class="col-md-4 mb-4">
                            <div class="card shadow-sm card-accidents">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Number of Accidents</h5>
                                    <h2 id="accidents-count">{{ accidents }}</h2>
                                </div>
                            </div>
                        </div>
            
                        <!-- Card 2: Number of Deaths -->
                        <div class="col-md-4 mb-4">
                            <div class="card shadow-sm card-deaths">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Number of Deaths</h5>
                                    <h2 id="deaths-count">{{ deaths }}</h2>
                                </div>
                            </div>
                        </div>
            
                        <!-- Card 3: Current Date and Time -->
                        <div class="col-md-4 mb-4">
                            <div class="card shadow-sm card-time">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Current Date & Time</h5>
                                    <h2 id="current-time">{{ current_time }}</h2> <!-- This will be dynamically updated -->
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </body>

            <!-- Cards Section -->
            <section class="row">
                <div class="col-md-6 mb-4">
                    <div class="card shadow-sm">
                        <img src="{{ url_for('static', filename='images/severity.jpg') }}" class="card-img-top" alt="Severity Prediction">
                        <div class="card-body">
                            <h5 class="card-title">Severity Prediction</h5>
                            <p class="card-text">Predict the severity of accidents based on location.</p>
                            <a href="/severity-prediction" class="btn btn-dark">Go to Severity Prediction</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-4">
                    <div class="card shadow-sm">
                        <img src="{{ url_for('static', filename='images/time.jpg') }}" class="card-img-top" alt="Peak Time Prediction">
                        <div class="card-body">
                            <h5 class="card-title">Peak Time Prediction</h5>
                            <p class="card-text">Identify the time slots with the highest number of accidents.</p>
                            <a href="/time-range-prediction" class="btn btn-dark">Go to Peak Time Prediction</a>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Map Section: Add map below the cards -->
            <section class="map-section mt-5">
                <h3 class="text-center">Accidents Map</h3>
                <div id="map" style="height: 400px;"></div> <!-- This is the map container -->
            </section>

            <footer class="text-center mt-5 py-4 bg-light">
                <p>&copy; 2024 Traffic Insights | All Rights Reserved</p>
            </footer>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
    <script>
        // Initialize the Leaflet map
        var map = L.map('map').setView([{{ map_center_lat }}, {{ map_center_lon }}], 12); // Set the initial view with the center coordinates

        // Add a TileLayer to the map (OpenStreetMap tiles)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add markers for each accident (assuming accident data is passed as a list of coordinates)
        {% for accident in accidents_data %}
            L.marker([{{ accident.lat }}, {{ accident.lon }}])
                .addTo(map)
                .bindPopup("Accident Location: {{ accident.location }}");
        {% endfor %}
    </script>
</body>
</html>
