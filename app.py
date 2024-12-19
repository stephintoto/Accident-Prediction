from flask import Flask, render_template , request
import pandas as pd
from datetime import datetime
import folium
from folium.plugins import HeatMap, MarkerCluster
import json
from flask import jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

time_range_map = {
    0: "Midnight [12 AM-3 AM]",
    1: "Early Morning [3 AM-6 AM]",
    2: "Morning [6 AM-9 AM]",
    3: "Late Morning [9 AM-12 PM]",
    4: "Afternoon [12 PM-3 PM]",
    5: "Late Afternoon [3 PM-6 PM]",
    6: "Evening [6 PM-9 PM]",
    7: "Night [9 PM-12 AM]"
}
cluster_map = pd.read_excel("unique_clusters_Tvm.xlsx", index_col="Cluster").to_dict()["Cluster_Place_Name"]

district_data ={'THIRUVANANTHAPURAM CITY': ['Thiruvallam', 'Peroorkada', 'Pettah', 'Thumba', 'Karamana', 'Museum', 'Fort', 'Kovalam', 'Kazhakkuttom', 'Cantonment', 'Medical College', 'Vizhinjam', 'Nemom', 'Sreekariyam', 'Vattiyoorkavu', 'Poojappura', 'Thampanoor', 'Valiyathura', 'Poonthura', 'Vanchiyoor', 'Mannanthala'],'THIRUVANANTHAPURAM RURAL': ['Naruvamoodu', 'Venjarammood', 'Aruvikkara', 'Aryanad', 'Poovar', 'Balaramapuram', 'Kadakkavoor', 'Kilimanoor', 'Pozhiyoor', 'Pothencode', 'Kattakkada', 'Neyyattinkara', 'Kallambalam', 'Vilappilsala', 'Nedumangad', 'Kanjiramkulam', 'Pallickal', 'Vattappara', 'Chirayinkil', 'Varkala', 'Valiyamala', 'Maranalloor', 'Mangalapuram', 'Parassala', 'Marayamuttom', 'Ayiroor ', 'Kadinamkulam', 'Vithura', 'Attingal', 'Neyyardam', 'Nagarur', 'Palode', 'Malayinkil', 'Vellarada', 'Pangode', 'Ariyancode', 'Ponmudi', 'Anchuthengu '],'KOLLAM CITY': ['Eravipuram', 'Kottiyam PS', 'Parippally PS', 'Chathannoor PS', 'Anchalumoodu PS', 'Chavara PS', 'Sakthikulangara PS', 'Ochira PS', 'Kannanelure PS', 'Karunagappally PS', 'Kollam East PS', 'Kollam West PS', 'Paravoor PS', 'Kilikollur PS', 'Pallithottam PS', 'Chavara Thekkumbhagam'],'KOLLAM RURAL': ['Kundara PS', 'Kottarakkara PS', 'Chadayamangalam PS', 'Thenmala PS', 'Pooyappally PS', 'Kunnikode PS', 'Sooranad PS', 'Anchal PS', 'Puthoor PS', 'Punalur PS', 'Chithara (Valavupacha) PS', 'Sasthamcotta PS', 'Eroor PS', 'Kadakkal PS', 'Pathanapuram PS', 'Ezhukone PS', 'Kulathupuzha PS', 'East Kallada PS'],'PATHANAMTHITTA': ['Enathu (old Kakkad)', 'Thiruvalla ', 'Konni ', 'Pandalam ', 'Pulikeezhu ', 'Koipuram ', 'Vadasserikkara', 'Adoor ', 'Chittar ', 'Keezhvaipur ', 'Koodal ', 'Aranmula ', 'Perunadu', 'Pampa ', 'Malayalapuzha', 'Pathanamthitta ', 'Kodumon ', 'Ranny ', 'Perumpetty ', 'Elavumthitta PS', 'Thannithodu ', 'Vechoochira '],'ALAPPUZHA': ['Kanakakunnu', 'Kuthiathode PS', 'Nooranadu', 'Chengannur', 'Arthinkal', 'Ambalapuzha', 'Cherthala', 'Kayamkulam', 'Poochakkal', 'Kareelakulangara', 'Alappuzha North', 'Pattanakkadu', 'Mararikkulam', 'Mannachery', 'Alappuzha South', 'Punnapra', 'Muhamma', 'Harippad', 'Aroor', 'Vallikunnam', 'Veeyapuram', 'Venmony', 'Mavelikara', 'Kurathikad', 'Ramankari', 'Nedumudy', 'Pulincunnu', 'Mannar', 'Edathua', 'Thrikkunnapuzha'],'KOTTAYAM': ['Ponkunnam', 'Pampady', 'Thrikkodithanam', 'Ettumanoor', 'Kottayam West', 'Gandhinagar', 'Ramapuram', 'Kumarakom', 'Changanachery', 'Kanjirappally', 'Chingavanam', 'Kaduthuruthy', 'Manarcadu', 'Kottayam East', 'Vaikom', 'Velloor', 'Pala', 'Mundakayam', 'Kuravilangadu', 'Vakathanam', 'Pallikkathodu', 'Ayarkunnam', 'Kidangoor', 'Thidanadu', 'Thalayolaparambu', 'Erumely', 'Manimala', 'Erattupetta', 'Karukachal', 'Melukavu', 'Marangattupally'],'IDUKKI': ['Peruvanthanam', 'Nedumkandam', 'Vellathooval', 'Thodupuzha', 'Rajakkadu', 'Kattappana', 'Santhanpara', 'Vandiperiyar', 'Udummbanchola PS', 'Karimkunnam', 'Kanjikuzhy', 'Adimali', 'Muttom', 'Upputhara', 'Vandanmedu', 'Kanjar', 'Peerumedu', 'Thankamoney', 'Cumbummettu', 'Kaliyar', 'Kumali', 'Munnar', 'Karimannoor', 'Kulamavu', 'Idukki', 'Devikulam', 'Karimanal', 'Marayoor'],'ERNAKULAM CITY': ['Mulavukadu ', 'Thoppumpady ', 'Cheranelloor ', 'Kalamassery','Ernakulam Central ', 'Thrikkakara', 'Kannamali ', 'Harbour', 'Hill Palace (Thrippunnithura)', 'Ambalamedu', 'Palarivattom ', 'Ernakulam Town North ', 'Maradu', 'Panangad ', 'Eloor ', 'Fort Kochi ', 'Palluruthy Kasaba', 'Udayamperoor', 'Ernakulam Town South ', 'Mattancherry ', 'Kadavanthra ', 'Elamakkara', 'Infopark'],'ERNAKULAM RURAL': ['Kothamangalam', 'Nedumbassery', 'Njarakkal', 'Vazhakulam', 'Aluva', 'Perumbavoor', 'North Parur ', 'Muvattupuzha', 'Kuttampuzha', 'Piravom', 'Angamaly', 'Chottanikkara', 'Vadakkekara', 'Aluva West', 'Kuruppumpady', 'Puthencruz', 'Chengamanadu', 'Kalady', 'Puthenvelikkara', 'Kunnathunadu', 'Mulamthuruthy', 'Edathala', 'Oonnukal', 'Munambam', 'Kodanadu', 'Koothattukulam', 'Varapuzha', 'Pothanikkadu', 'Binanipuram', 'Ramamangalam', 'Thadiyittaparambu', 'Kottapady', 'Ayyampuzha', 'Kalloorkadu'],'THRISSUR CITY' : ['Ollur', 'Peechi', 'Kunnamkulam', 'Chavakkad', 'Viyyur', 'Mannuthy', 'Thrissur Town West ', 'Wadakkanchery', 'Vadakkekkad', 'Pavaratty', 'Thrissur Town East ', 'Medical College PS ', 'Erumapetty', 'Peramangalam', 'Cheruthuruthy', 'Pazhayannoor', 'Chelakkara', 'Guruvayoor', 'Nedupuzha', 'Guruvayoor Temple PS'],'THRISSUR RURAL': ['Vellikulangara', 'Kaipamangalam', 'Pudukkad', 'Irinjalakkuda', 'Anthikad', 'Kodakara', 'Koratty', 'Chalakkudy', 'Cherpu', 'Vadanappally', 'Kodungallur', 'Mathilakam', 'Kattoor', 'Aloor', 'Valappad', 'Varantharappally', 'Mala', 'Athirappally/ Vettilappara'],'PALAKKAD': ['Alathur', 'Mannarkkad', 'Chalissery', 'Pattambi', 'Ottapalam', 'Kuzhalmannam', 'Palakkad Town South', 'Kozhinjampara', 'Koppam', 'Vadakkenchery', 'Kollengode', 'Palakkad Town North', 'Walayar', 'Cherplassery', 'Malampuzha', 'Chittur', 'Sreekrishnapuram', 'Kalladikode', 'Nattukal', 'Meenaksipuram', 'Hemambika Nagar', 'Kongad', 'Thrithala', 'Shornur', 'Mankara', 'Kasaba', 'Nemmara', 'Kottayi', 'Sholayur ', 'Pudunagaram', 'Agali ', 'Mangalam Dam'],'MALAPPURAM': ['Kolathur', 'Ponnani', 'Malappuram', 'Kadampuzha', 'Kuttipuram', 'Valanchery', 'Perinthalmanna', 'Tanur', 'Edakkara', 'Thirurangadi', 'Changaramkulam', 'Kalpakanchery', 'Manjeri', 'Areacode', 'Vazhakkad', 'Kottakkal', 'Perumpadappu', 'Tirur', 'Melattur', 'Kondotty', 'Parappanangadi', 'Wandoor', 'Vengara', 'Vazhikadavu', 'Pothukal', 'Mankada', 'Thenhipalam', 'Karipur Air port PS', 'Nilambur', 'Kalikavu', 'Edavanna', 'Pandikkad', 'Karuvarakundu', 'Pookottumpadam'],'KOZHIKODE CITY':  ['Nadakkave', 'Panniyankara', 'Mavoor', 'Kunnamangalam', 'Chevayur', 'Town Kozhikode', 'Pantheerankavu PS', 'Med. College', 'Elathur', 'Nallalam', 'Feroke', 'Kasaba Kozhikode', 'Vellayil', 'Chemmangad', 'Beypore'],'KOZHIKODE RURAL': ['Perambra ', 'Vatakara ', 'Thiruvambady', 'Kakkur ', 'Mukkom', 'Thamarassery', 'Balussery ', 'Koduvally ', 'Kuttiady ', 'Thotilpalam ', 'Meppayur ', 'Koyilandy ', 'Chompala', 'Peruvannamoozhi ', 'Payyoli ', 'Atholi', 'Nadapuram ', 'Edachery ', 'Valayam ', 'Kodenchery ', 'Koorachundu '],'WAYANAD': ['Padinjarethara', 'Kambalakkad ', 'Kalpetta ', 'Vythiri', 'Kenichira', 'Pulpally', 'Mananthavadi', 'Sulthan Batheri', 'Meenangadi', 'Ambalavayal', 'Panamaram', 'Thirunelli', 'Meppadi', 'Vellamunda', 'Noolpuzha', 'Thondarnadu', 'Thalappuzha'],'KANNUR CITY':  ['Kuthuparamba', 'Valapattanam', 'Kannur Town ', 'Thalassery', 'New Mahe', 'Mattannur', 'Kannavam', 'Chockly', 'Kolavallur', 'Chakkarakkal ', 'Kannapuram', 'Edakkad ', 'Mayyil', 'Dharmadam', 'Pinarayi', 'Panoor', 'Kathirur'],'KANNUR RURAL': ['Pariyaram MC PS', 'Karikottakari', 'Kudiyanmala', 'Taliparamba', 'Iritty', 'Payyannur', 'Cherupuzha', 'Muzhakkunnu', 'Payyavoor', 'Kelakam', 'Peringome', 'Irikkur', 'Sreekandapuram', 'Ulikkal', 'Alakode', 'Peravoor', 'Payangadi', 'Aralam', 'Maloor'],'KASARAGOD': ['Kasaragod', 'Chittarikkal', 'Bekal', 'Melparamba PS', 'Kumbla', 'Nileshwar', 'Chandera', 'Hosdurg', 'Manjeshwar', 'Rajapuram', 'Amabalathara', 'Cheemeni', 'Adhur', 'Vellarikundu', 'Vidyanagar', 'Bedakam', 'Badiadka']}

# Updated file paths for pickle files
time_range_model = joblib.load("models/xgboost_model.pkl")
time_range_visibility_encoder = joblib.load("models/visibility_encoder.pkl")
time_range_time_range_encoder = joblib.load("models/time_range_encoder.pkl")
time_range_label_encoders = joblib.load("models/label_encoders.pkl")

# Accident cluster prediction model
cluster_model = joblib.load("models/TVMmodel.pkl")
cluster_visibility_encoder = joblib.load("models/cluster_Ve.pkl")
cluster_time_range_encoder = joblib.load("models/cluster_tre.pkl")
cluster_label_encoders = joblib.load("models/cluster_le.pkl")

#for severity prediction
model2= joblib.load('model2/xgb_classifier_model.pkl')
label_encoder = joblib.load('model2/label_encoder.pkl')
fe_ps_name = joblib.load('model2/PS Name_freq_encoding.pkl')
fe_district = joblib.load('model2/District_freq_encoding.pkl')
oe = joblib.load('model2/ordinal_encoder.pkl')


# Helper function to create the map
def create_combined_map(selected_district="All", selected_ps_name="All", selected_time_range="All"):
    geojson_police_path = r"export.geojson"
    geojson_taluk_path = r"taluk.geojson"
    excel_file = r"New Traffic Data (1).xlsx"
    df2 = pd.read_excel(excel_file, sheet_name="2022")
    df3 = pd.read_excel(excel_file, sheet_name="2023")
    df_combined = pd.concat([df2, df3], ignore_index=True).dropna(subset=['Latitude', 'Longitude'])

    df_combined['Hour'] = pd.to_datetime(df_combined['Time Accident'], format='%H:%M:%S').dt.hour
    df_combined['Time Range'] = df_combined['Hour'].apply(lambda x: f"{3 * (x // 3)}-{3 * ((x // 3) + 1)}")

    # Filter accident data
    filtered_data = df_combined
    if selected_district != "All":
        filtered_data = filtered_data[filtered_data['District'] == selected_district]
    if selected_ps_name != "All":
        filtered_data = filtered_data[filtered_data['PS Name'] == selected_ps_name]
    if selected_time_range != "All":
        filtered_data = filtered_data[filtered_data['Time Range'] == selected_time_range]

    # Create the base map
    kerala_map = folium.Map(
        location=[10.8505, 76.2711],  # Centering map over Kerala
        zoom_start=7,
        max_bounds=True,
        min_zoom=7,
        max_zoom=18
    )

    # Add accident markers and heatmap
    accident_cluster = MarkerCluster(name="Accident Locations").add_to(kerala_map)
    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=(f"District: {row['District']}<br>Time Range: {row['Time Range']}<br>PS Name: {row['PS Name']}")
        ).add_to(accident_cluster)

    heat_data = df_combined[['Latitude', 'Longitude']].values.tolist()
    HeatMap(heat_data, name="Accident Heat Map", radius=15).add_to(kerala_map)

    # Add police stations (use your own geojson data)
    with open(geojson_police_path, encoding='utf-8') as f:
        police_geojson = json.load(f)

    police_station_cluster = MarkerCluster(name="Police Stations").add_to(kerala_map)
    for feature in police_geojson['features']:
        geometry = feature['geometry']
        props = feature['properties']
        name = props.get("name", "Unknown Police Station")
        if geometry['type'] == 'Point':
            coords = geometry['coordinates']
            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=5, color="red", fill=True, fill_opacity=0.7,
                popup=f"Police Station: {name}"
            ).add_to(police_station_cluster)

    folium.GeoJson(
        geojson_taluk_path,
        name="Taluk Boundaries",
        style_function=lambda feature: {'fillColor': 'blue', 'color': 'black', 'weight': 0.5, 'fillOpacity': 0.0},
        tooltip=folium.GeoJsonTooltip(fields=['TALUK'], aliases=['Taluk Name:'], localize=True)
    ).add_to(kerala_map)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(kerala_map)

    # Save the map to an HTML file
    map_path = 'static/traffic_map.html'
    kerala_map.save(map_path)
    return map_path

@app.route("/get_ps_names")
def get_ps_names():
    selected_district = request.args.get("district", "All")
    excel_file = r"New Traffic Data (1).xlsx"
    df2 = pd.read_excel(excel_file, sheet_name="2022")
    df3 = pd.read_excel(excel_file, sheet_name="2023")
    df = pd.concat([df2, df3], ignore_index=True).dropna(subset=['Latitude', 'Longitude'])

    if selected_district == "All":
        ps_names = df['PS Name'].dropna().unique().tolist()
    else:
        ps_names = df[df['District'] == selected_district]['PS Name'].dropna().unique().tolist()

    ps_names.sort()
    return jsonify(ps_names)

@app.route("/")
def home():
    excel_file = r"New Traffic Data (1).xlsx"
    df2 = pd.read_excel(excel_file, sheet_name="2022")
    df3 = pd.read_excel(excel_file, sheet_name="2023")
    df = pd.concat([df2, df3], ignore_index=True).dropna(subset=['Latitude', 'Longitude'])

    # Extract unique filter options
    districts = df['District'].dropna().unique().tolist()
    ps_names = df['PS Name'].dropna().unique().tolist()
    df['Hour'] = pd.to_datetime(df['Time Accident'], format='%H:%M:%S').dt.hour
    df['Time Range'] = df['Hour'].apply(lambda x: f"{3 * (x // 3)}-{3 * ((x // 3) + 1)}")
    time_ranges = df['Time Range'].dropna().unique().tolist()
    time_ranges.sort(key=lambda x: int(x.split('-')[0].strip()))
    


    # Get the selected filters from query parameters
    selected_district = request.args.get("district", "All")
    selected_ps_name = request.args.get("ps_name", "All")
    selected_time_range = request.args.get("time_range", "All")

    # Filter accident data
    filtered_data = df
    if selected_district != "All":
        filtered_data = filtered_data[filtered_data['District'] == selected_district]
    if selected_ps_name != "All":
        filtered_data = filtered_data[filtered_data['PS Name'] == selected_ps_name]
    if selected_time_range != "All":
        filtered_data = filtered_data[filtered_data['Time Range'] == selected_time_range]

    # Metrics calculation
    total_accidents = df['FIR No'].count()  # Change 'Accidents' to your column name
    total_deaths = df['Death'].sum()  # Change 'Deaths' to your column name
    total_pedestrians = filtered_data['Pedestrian'].sum()  # Replace with actual column name for pedestrians
    most_vehicle_type = filtered_data['Accussed Vehicle'].mode()[0]  # Replace with the column name for vehicle types
    total_minor_injuries = filtered_data['Minor'].sum()  # Replace with the actual column for minor injuries

    # Get the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate the map path
    map_path = create_combined_map(selected_district, selected_ps_name, selected_time_range)

    # Pass the filter options and other data to the HTML template
    return render_template(
        'index.html',
        accidents=total_accidents,
        deaths=total_deaths,
        current_time=current_time,
        map_path=map_path,
        pedestrians=total_pedestrians,
        vehicle_type=most_vehicle_type,
        minor_injuries=total_minor_injuries,
        districts=["All"] + sorted(districts),
        ps_names=["All"] + sorted(ps_names),
        time_ranges=["All"] + sorted(time_ranges),
        selected_district=selected_district,
        selected_ps_name=selected_ps_name,
        selected_time_range=selected_time_range,
    )

def safe_label_encode(encoder, value):
    """
    Safely encode a single value using the LabelEncoder.
    Returns -1 if the value is unseen.
    """
    try:
        return encoder.transform([value])[0]
    except ValueError:
        return -1

def safe_frequency_encode(encoding_dict, value):
    """
    Safely encode a value using the frequency encoding dictionary.
    Returns 0 if the value is unseen.
    """
    return encoding_dict.get(value, 0)


@app.route("/severity-prediction", methods=["GET", "POST"])
def severity_prediction():
    districts = list(district_data.keys()) 
    if request.method == "POST":
        # Get input values from the form
        accident_time_of_day = request.form['accident_time_of_day']
        lanes_road = request.form['lanes_road']
        weather = request.form['weather']
        type_road = request.form['type_road']
        traffic_control = request.form['traffic_control']
        accident_factor = request.form['accident_factor']
        district = request.form['district']
        ps_name = request.form['ps_name']
        type_area = request.form['type_area']
        divider = request.form['divider']
        
        # Create a dataframe for input
        input_data = pd.DataFrame([[accident_time_of_day, lanes_road, weather, type_road, 
                                    traffic_control, accident_factor, district, ps_name, 
                                    type_area, divider]], 
                                  columns=['Accident Time of Day', 'Lanes Road', 
                                           'Weather', 'Type Road', 'Traffic Control', 
                                           'Accident factor', 'District', 'PS Name', 
                                           'Type Area', 'Divider'])
        
        # Apply Label Encoding using the same encoder
        input_data['Accident Time of Day'] = safe_label_encode(label_encoder, accident_time_of_day)
        input_data['Lanes Road'] = safe_label_encode(label_encoder, lanes_road)
        input_data['Weather'] = safe_label_encode(label_encoder, weather)
        input_data['Type Road'] = safe_label_encode(label_encoder, type_road)
        input_data['Traffic Control'] = safe_label_encode(label_encoder, traffic_control)
        input_data['Accident factor'] = safe_label_encode(label_encoder, accident_factor)
        
        # Apply Frequency Encoding
        input_data['PS Name'] = safe_frequency_encode(fe_ps_name, ps_name)
        input_data['District'] = safe_frequency_encode(fe_district, district)
        
        # Apply Ordinal Encoding directly
        try:
            input_data['Type Area'] = oe.transform([[type_area]])[0][0]  # Correct use of transform
            input_data['Divider'] = oe.transform([[divider]])[0][0]  # Correct use of transform
        except ValueError:
            input_data['Type Area'] = -1  # Default for unknown values
            input_data['Divider'] = -1  # Default for unknown values
        
        # Make the prediction using the model
        prediction = model2.predict(input_data)
        
        # Map numeric prediction to actual accident type labels
        accident_type_map = {
            0: 'Grevious Injury',
            1: 'Minor Injury',
            2: 'Fatal',
            3: 'Non Injury'
        }
        
        # Convert the numeric prediction to the human-readable label
        prediction_result = accident_type_map.get(prediction[0], 'Unknown')
        
        return render_template("severity_prediction.html", prediction=prediction_result,districts=districts)
    
    return render_template("severity_prediction.html", districts=districts)

@app.route('/fetch_police_stations', methods=['GET'])
def fetch_police_stations():
    district = request.args.get('district')  # Selected district
    police_stations = district_data.get(district, [])  # Fetch corresponding PS
    return jsonify(police_stations)


@app.route("/time-range-prediction", methods=["GET", "POST"])
def time_range_prediction():

    districts = list(district_data.keys()) 

    return render_template('time_range_prediction.html',districts=districts)

@app.route("/predict", methods=["POST"])
def predict():
   if request.method == "POST":
    try:
        # Extract inputs from form
        district = request.form["district"]
        ps_name = request.form["ps_name"]
        weather = request.form["weather"]
        visibility = request.form["visibility"]
        date_input = request.form["date"]

        # Process date input
        date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        day_of_week = date_obj.strftime("%A")

        # Encode features for time range prediction
        tr_district_encoded = time_range_label_encoders["District"].transform([district])[0]
        tr_ps_name_encoded = time_range_label_encoders["PS Name"].transform([ps_name])[0]
        tr_weather_encoded = time_range_label_encoders["Weather"].transform([weather])[0]
        tr_visibility_encoded = time_range_visibility_encoder.transform([[visibility]])[0][0]
        tr_day_of_week_encoded = time_range_label_encoders["Day of Week"].transform([day_of_week])[0]

        # Combine features for time range prediction
        time_range_features = np.array([[tr_district_encoded, tr_ps_name_encoded, tr_weather_encoded,
                                          tr_visibility_encoded, tr_day_of_week_encoded, month, day]], dtype=np.float32)

        # Debugging: Print time range features
        print("Time Range Features:", time_range_features)

        # Predict accident time range
        time_range_numeric = time_range_model.predict(time_range_features)[0]  # Numeric prediction
        time_range_prediction = time_range_map.get(time_range_numeric, "Unknown Time Range")

        # Check if cluster prediction is required
        if district in ["THIRUVANANTHAPURAM CITY", "THIRUVANANTHAPURAM RURAL"]:
            # Encode features for cluster prediction
            cl_district_encoded = cluster_label_encoders["District"].transform([district])[0]
            cl_ps_name_encoded = cluster_label_encoders["PS Name"].transform([ps_name])[0]
            cl_weather_encoded = cluster_label_encoders["Weather"].transform([weather])[0]
            cl_visibility_encoded = cluster_visibility_encoder.transform([[visibility]])[0][0]
            cl_day_of_week_encoded = cluster_label_encoders["Day of Week"].transform([day_of_week])[0]
            cl_time_range_encoded = time_range_numeric

            # Combine features for cluster prediction
            cluster_features = np.array([[cl_district_encoded, cl_ps_name_encoded, cl_weather_encoded,
                                           cl_visibility_encoded, cl_time_range_encoded, cl_day_of_week_encoded,
                                           month, day]], dtype=np.float32)

            # Debugging: Print cluster features
            print("Cluster Features:", cluster_features)

            # Predict accident cluster
            cluster_numeric = cluster_model.predict(cluster_features)[0]  # Numeric prediction
            cluster_prediction = cluster_map.get(cluster_numeric, "Unknown Cluster")

            # Render result with both predictions
            return render_template(
                "result.html",
                time_range_prediction=time_range_prediction,
                cluster_prediction=cluster_prediction
            )
        else:
            # Render result with only time range prediction
            return render_template(
                "result.html",
                time_range_prediction=time_range_prediction,
                cluster_prediction=None
            )

    except Exception as e:
        return f"Error occurred: {e}"

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))