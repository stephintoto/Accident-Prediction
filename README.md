# Traffic Accident Analysis and Prediction

Explore traffic accident insights, predict accident trends, and analyze accident data with a modern, interactive web application.

## Introduction

Traffic accidents are a pressing concern in today’s urban environments. This project aims to provide data-driven insights into traffic accidents while offering predictive capabilities for key metrics, including severity, time-range trends, and location-based analysis.

## Features

- **Severity Prediction**: Predict the severity of traffic accidents using historical data.
- **Peak Time Analysis**: Identify high-risk time periods for accidents.
- **Accident Insights**: Detailed visualizations on accident trends, fatalities, minor injuries, and vehicle types involved.
- **Embedded Map**: View accident locations via an interactive map.

## Technologies Used

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Visualization**: Matplotlib, Plotly
- **Database**: Excel Files
- **Other Libraries**: FontAwesome, Pandas, NumPy

## Setup Instructions

Follow the steps below to set up and run the project locally.

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/traffic-accident-analysis.git
    cd traffic-accident-analysis
    ```

2. **Set up a Python Virtual Environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # For Linux/macOS
    env\Scripts\activate     # For Windows
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask App**:
    ```bash
    python app.py
    ```

5. **Open in Browser**:
    Navigate in your web browser.

## Usage

1. Navigate the sidebar to access different pages:
    - Home
    - Severity Prediction
    - Peak Time Prediction
    - About
2. Use the filter dropdowns to refine your analysis based on specific criteria (district, police station, etc.).
3. Explore the interactive map to view accident trends.


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Bootstrap for frontend styling.
- FontAwesome for icons.
- Flask for backend framework.
- Data sourced from [relevant traffic authorities/data sources].
