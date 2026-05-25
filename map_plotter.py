from __future__ import annotations
import os
import folium

MAP_OUTPUT_PATH = "outputs/maps/distance_map.html"


class MapPlotter:

    @staticmethod
    def generate_map(
        place1: str,
        place2: str,
        coord1: tuple[float, float],
        coord2: tuple[float, float],
        distance: float,
        output_path: str = MAP_OUTPUT_PATH,
    ) -> str:
        """
        Render an interactive Folium map with two markers connected by a line.

        Returns the absolute path to the saved HTML file.
        """
        center_lat = (coord1[0] + coord2[0]) / 2
        center_lon = (coord1[1] + coord2[1]) / 2

        m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

        for place, coord in ((place1, coord1), (place2, coord2)):
            folium.Marker(
                location=coord,
                popup=folium.Popup(place, max_width=200),
                tooltip=place,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

        folium.PolyLine(
            locations=[coord1, coord2],
            color="#e74c3c",
            weight=2.5,
            opacity=0.8,
            tooltip=f"Distance: {distance:.2f} km",
        ).add_to(m)

        # Midpoint label — white pill with black text, offset above the line
        mid_lat = (coord1[0] + coord2[0]) / 2
        mid_lon = (coord1[1] + coord2[1]) / 2
        label_html = (
            f'<div style="'
            f'font-size:13px;'
            f'font-weight:bold;'
            f'color:#000000;'
            f'background:rgba(255,255,255,0.92);'
            f'border:1.5px solid #555;'
            f'border-radius:6px;'
            f'padding:3px 8px;'
            f'white-space:nowrap;'
            f'box-shadow:1px 1px 4px rgba(0,0,0,0.25);'
            f'">{distance:,.2f} km</div>'
        )
        folium.Marker(
            location=[mid_lat, mid_lon],
            icon=folium.DivIcon(
                html=label_html,
                icon_size=(130, 30),
                # Anchor centres horizontally and places the box above the point
                icon_anchor=(65, 40),
            ),
        ).add_to(m)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        m.save(output_path)

        return os.path.abspath(output_path)