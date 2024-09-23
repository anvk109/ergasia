import spacy
import plotly.graph_objs as go
import pandas as pd
from geopy.geocoders import Nominatim
import pycountry
from googletrans import Translator

# Load spaCy Greek language model
nlp = spacy.load("el_core_news_sm")  # Greek model

# Initialize the Google Translate API
translator = Translator()

# Sample Greek text containing country and city names
text = "Έχω επισκεφθεί το Παρίσι, στη Γαλλία, και το Βερολίνο, στη Γερμανία. Ο φίλος μου ζει στο Τορόντο και θέλω να επισκεφτώ το Τόκιο του χρόνου."

# Process the text using spaCy
doc = nlp(text)

# Extract recognized country names and city names
countries_in_text = []
cities_in_text = []
countries_in_greek = []  # Keep the original Greek names for display
cities_in_greek = []  # Keep the original Greek names for display

for ent in doc.ents:
    if ent.label_ == "GPE":
        translated_entity = translator.translate(ent.text, src='el', dest='en').text
        if pycountry.countries.get(name=translated_entity):
            countries_in_text.append(translated_entity)
            countries_in_greek.append(ent.text)  # Store the Greek name
        else:
            cities_in_text.append(translated_entity)
            cities_in_greek.append(ent.text)  # Store the Greek name

# Print the translations
print("Countries in Greek:")
print(countries_in_greek)

print("\nCities in Greek:")
print(cities_in_greek)

# Use pycountry to match recognized countries to official names and codes
country_codes = []
country_names = []
for country in countries_in_text:
    try:
        country_data = pycountry.countries.lookup(country)
        country_codes.append(country_data.alpha_3)  # ISO Alpha-3 codes for Plotly
        country_names.append(country_data.name)  # Full country names in English
    except LookupError:
        continue

# Initialize geolocator for city coordinates
geolocator = Nominatim(user_agent="city_locator")
city_data = []
for city in cities_in_text:
    try:
        location = geolocator.geocode(city)
        if location:
            city_data.append({'city': city, 'lat': location.latitude, 'lon': location.longitude})
    except:
        continue

# Create a DataFrame for cities
city_df = pd.DataFrame(city_data)
city_df['city_name'] = cities_in_greek  # Add the Greek names for display

# Create a DataFrame for countries
country_df = pd.DataFrame({
    'country_code': country_codes,
    'country_name': countries_in_greek  # Use the Greek names for display
})

# Create a Plotly figure for the world map
fig = go.Figure()

# Add countries layer with Greek names on hover
fig.add_trace(go.Choropleth(
    locations=country_df['country_code'],
    z=[1] * len(country_df),  # Dummy value to color the countries
    colorscale=['lightgray', 'red'],
    showscale=False,
    marker_line_color='black',  # Line color of country boundaries
    marker_line_width=0.5,
    hoverinfo='location',
    hovertemplate='<b>%{customdata}</b><extra></extra>',  # Remove "trace0" and only show country names
    customdata=country_df['country_name'],  # Pass the full Greek country names as custom data
))

# Add city pins with Greek names
fig.add_trace(go.Scattergeo(
    lon=city_df['lon'],
    lat=city_df['lat'],
    text=city_df['city_name'],  # Use the Greek names for display
    mode='markers',
    marker=dict(size=8, color='blue'),
    hoverinfo='text',
    hoverlabel=dict(bgcolor='white'),  # White background for hover labels
    hovertemplate='<b>%{text}</b><extra></extra>',  # Clean up hover template for cities
))

# Update layout for full world map view
fig.update_geos(
    projection_type="natural earth",
    showcountries=True,
    showcoastlines=True,
    showland=True,
    landcolor="lightgray"
)

# Update layout to hide axis lines and ticks
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    geo=dict(showframe=False, showcoastlines=False)
)

# Show the interactive map
fig.show()
