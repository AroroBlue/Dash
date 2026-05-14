from dash import Dash, dcc, html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd

from receiver import UDPReceiver
from aircraft_store import AircraftStore


# =========================================================
# CREATE DASH APP
# =========================================================

app = Dash(__name__)

store = AircraftStore()


# =========================================================
# START RECEIVERS
# =========================================================

receiver_original = UDPReceiver(
    host="0.0.0.0",
    port=30001,
    source_name="ORIGINAL",
    aircraft_store=store
)

receiver_filtered = UDPReceiver(
    host="0.0.0.0",
    port=30002,
    source_name="FILTERED",
    aircraft_store=store
)

receiver_original.start()
receiver_filtered.start()


# =========================================================
# DASH LAYOUT
# =========================================================

app.layout = html.Div([

    html.H1(
        "Saudi Arabia CAT048 Validation Dashboard",
        style={"textAlign": "center"}
    ),

    html.Div([

        dcc.Checklist(
            id="feed_selector",

            options=[
                {
                    "label": "Original Feed",
                    "value": "ORIGINAL"
                },

                {
                    "label": "Filtered Feed",
                    "value": "FILTERED"
                }
            ],

            value=["ORIGINAL", "FILTERED"],

            inline=True
        )

    ]),

    dcc.Graph(
        id="radar_map",
        style={"height": "90vh"}
    ),

    dcc.Interval(
        id="update_interval",
        interval=1000,
        n_intervals=0
    )
])


# =========================================================
# CALLBACK
# =========================================================

@app.callback(

    Output("radar_map", "figure"),

    Input("update_interval", "n_intervals"),
    Input("feed_selector", "value")
)

def update_map(_, enabled_sources):

    store.cleanup()

    targets = store.get_targets()

    targets = [
        t for t in targets
        if t["source"] in enabled_sources
    ]

    fig = go.Figure()

    colors = {
        "ORIGINAL": "blue",
        "FILTERED": "red"
    }

    for source in ["ORIGINAL", "FILTERED"]:

        source_targets = [
            t for t in targets
            if t["source"] == source
        ]

        if not source_targets:
            continue

        df = pd.DataFrame(source_targets)

        fig.add_trace(

            go.Scattermapbox(

                lat=df["lat"],
                lon=df["lon"],

                mode="markers",

                marker=dict(
                    size=10,
                    color=colors[source]
                ),

                name=source,

                text=[

                    (
                        f"Callsign: {row['callsign']}<br>"
                        f"Track: {row['track_number']}<br>"
                        f"ICAO: {row['icao']}<br>"
                        f"Altitude: {row['altitude']}<br>"
                        f"Speed: {row['speed']}<br>"
                        f"Heading: {row['heading']}"
                    )

                    for _, row in df.iterrows()
                ],

                hoverinfo="text"
            )
        )

    fig.update_layout(

        mapbox_style="carto-positron",

        mapbox=dict(

            center=dict(
                lat=23.8859,
                lon=45.0792
            ),

            zoom=4.5
        ),

        margin=dict(
            l=0,
            r=0,
            t=40,
            b=0
        ),

        legend=dict(
            orientation="h"
        )
    )

    return fig


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=8050
    )