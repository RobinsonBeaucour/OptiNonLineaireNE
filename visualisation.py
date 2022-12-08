import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

file    =   st.text_input("chemin",value="./data_results/4WT_small_pressure_NE/")
Volume  =   pd.read_csv(file + "volume.txt")
Conso   =   pd.read_csv(file + "Conso.txt")
Z       =   pd.read_csv(file + "ZZ.txt")
Qpompe  =   pd.read_csv(file + "DebitPompe.txt")
Gpompe  =   pd.read_csv(file + "ChargePompe.txt")
States  =   pd.read_csv(file + "States.txt")
Charge  =   pd.read_csv(file + "ChargeReseau.txt")

fig = go.Figure()
for n in Volume.index.get_level_values(0).unique():
    if n.startswith("r"):
        # print(Volume.loc[n])
        fig.add_trace(
            go.Bar(
                x   =   Volume.loc[n].index,
                y   =   Volume.loc[n].iloc[:,0],
                name=   f"Volume {n}"
            )
        )
for c in Conso.index.get_level_values(0).unique():
    for d in Conso.index.get_level_values(1).unique():
        fig.add_trace(
            go.Scatter(
                x   =   Conso.loc[c,d].index,
                y   =   Conso.loc[c,d].iloc[:,0],
                yaxis="y2",
                name=   f"Elec {c},{d}"
            )
        )
fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
            ),
        hovermode='x',
        yaxis=dict(
            title="m3" ,
            # range=[0,df["Consommation (MW)"].max()*1.1]
            ),
        yaxis2=dict(title="kW",
        # range=[df["Coût MWh"].min()*0.95,df["Coût MWh"].max()*1.1],
        anchor="free",
        overlaying="y",
        side="right",
        position=1
        ),
        title = f"Etat du réseau de distribution d'eau - Coût : {Z.iloc[0,0]} €"
    )

st.plotly_chart(fig,use_container_width=True)

color_map   =   {
    'p1'    :   'red',
    'p2'    :   'blue',
    'p3'    :   'green'
}
color_map_light   =   {
    'p1'    :   'lightcoral',
    'p2'    :   'lightblue',
    'p3'    :   'lightgreen'
}
fig = go.Figure()
for c in States.index.get_level_values(0).unique():
    for d in States.index.get_level_values(1).unique():
        fig.add_trace(
            go.Bar(
                x               =   States.loc[c,d].index,
                y               =   10*States.loc[c,d].iloc[:,0],
                marker_color    =   color_map_light[d],
                name            =   f"Statut {c},{d}"
            )
        )
fig.update_layout(
    barmode="stack"
)
for c in Gpompe.index.get_level_values(0).unique():
    for d in Gpompe.index.get_level_values(1).unique():
        fig.add_trace(
            go.Scatter(
                x               =   Gpompe.loc[c,d].index,
                y               =   Gpompe.loc[c,d].iloc[:,0],
                marker_color    =   color_map[d],
                line_dash       =   'dash',
                name            =   f"Gain Charge {c},{d}"
            )
        )
for c in Qpompe.index.get_level_values(0).unique():
    for d in Qpompe.index.get_level_values(1).unique():
        fig.add_trace(
            go.Scatter(
                x               =   Qpompe.loc[c,d].index,
                y               =   Qpompe.loc[c,d].iloc[:,0],
                marker_color    =   color_map[d],
                name            =   f"Débit {c},{d}"
            )
        )
fig.update_layout(
    hovermode='x',
    title = f"Etat des pompes du réseau de distribution d'eau - Coût : {Z.iloc[0,0]} € "
    )

st.plotly_chart(fig,use_container_width=True)

fig = go.Figure()
for n in Charge.index.get_level_values(0).unique():
    fig.add_trace(
        go.Scatter(
            x = Charge.loc[n].index,
            y = Charge.loc[n].iloc[:,0],
            name = n
        )
    )
fig.update_layout(
    hovermode='x',
    title = f"Charge dans le réseau de distribution d'eau - Coût : {Z.iloc[0,0]} € "
)

st.plotly_chart(fig,use_container_width=True)