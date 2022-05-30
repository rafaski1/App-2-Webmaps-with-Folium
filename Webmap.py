"""
This webmap, built with folium and pandas, will visually present various data on a world map,
read from JSON files such as pinpoint locations and area indicators on separate layers.
As a result, HTML file will be produced for the user to interact with.
layer 1: base worldmap
layer 2: volcanoes in the USA, color-coded for different elevations
layer 3: population for each country, color-coded for different value brackets
"""

import folium
import pandas

#volcanoes
data = pandas.read_csv("Volcanoes_USA.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def elev_color(elev):
    if elev < 1500:
        return "green"
    elif 1500 <= elev <=2500:
        return "orange"
    elif 2500 < elev < 3500:
        return "red"
    else:
        return "darkred"

map = folium.Map(location=[39.74, -104.95], zoom_start=5, tiles="OpenStreetMap")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=7, popup=str(el) + " m",
        fill_color=elev_color(el), color = "gray", fill=True, fill_opacity=0.7))

#population
fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data = open("world.json", "r", encoding="utf-8-sig").read(),
    style_function=lambda x: {"color": "gray", "fillColor": "green" if x["properties"]["POP2005"] < 10000000 else "orange"
    if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")