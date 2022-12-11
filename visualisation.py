import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

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

def etat_RDE(Volume,Conso,Z,Margin=False):
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
                    name=   f"Elec {c},{d}",
                    marker_color = color_map[d]
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
    if Margin:
        fig.update_layout(
            margin_t = 120
        )
    return fig

def Pompe_RDE(States,Gpompe,Qpompe,Z,Margin=False):
    fig = go.Figure()
    for c in States.index.get_level_values(0).unique():
        for d in States.index.get_level_values(1).unique():
            fig.add_trace(
                go.Bar(
                    x               =   States.loc[c,d].index,
                    y               =   10*States.loc[c,d].iloc[:,0],
                    marker_color    =   color_map_light[d],
                    name            =   f"Statut {c},{d}",
                    hoverinfo       =   'skip'
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
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
            ),
    hovermode='x',
    title = f"Etat des pompes du réseau de distribution d'eau - Coût : {Z.iloc[0,0]} € "
    )
    if Margin:
        fig.update_layout(
            margin_t = 150
        )
    return fig

def Charge_RDE(Charge,Z):
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
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                ),
        hovermode='x',
        title = f"Charge dans le réseau de distribution d'eau - Coût : {Z.iloc[0,0]} € ",
        yaxis_title = "Charge (m)"
    )
    return fig

st.set_page_config(layout="wide")

comparaison = st.checkbox("Comparaison")

if comparaison:
    col_1,col_2 = st.columns(2)
    with col_1:
        file    =   "./data_results/" + st.selectbox("Résultat 1",options=os.listdir('./data_results')) + "/"
        Volume  =   pd.read_csv(file + "volume.txt")
        Conso   =   pd.read_csv(file + "Conso.txt")
        Z       =   pd.read_csv(file + "ZZ.txt")
        Qpompe  =   pd.read_csv(file + "DebitPompe.txt")
        Gpompe  =   pd.read_csv(file + "ChargePompe.txt")
        States  =   pd.read_csv(file + "States.txt")
        Charge  =   pd.read_csv(file + "ChargeReseau.txt")

        st.plotly_chart(etat_RDE(Volume,Conso,Z,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(States,Gpompe,Qpompe,Z,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(Charge,Z),use_container_width=True)
    with col_2:
        file2    =   "./data_results/" + st.selectbox("Résultat 2",options=os.listdir('./data_results')) + "/"
        Volume2  =   pd.read_csv(file2 + "volume.txt")
        Conso2   =   pd.read_csv(file2 + "Conso.txt")
        Z2       =   pd.read_csv(file2 + "ZZ.txt")
        Qpompe2  =   pd.read_csv(file2 + "DebitPompe.txt")
        Gpompe2  =   pd.read_csv(file2 + "ChargePompe.txt")
        States2  =   pd.read_csv(file2 + "States.txt")
        Charge2  =   pd.read_csv(file2 + "ChargeReseau.txt")

        st.plotly_chart(etat_RDE(Volume2,Conso2,Z2,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(States2,Gpompe2,Qpompe2,Z2,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(Charge2,Z2),use_container_width=True)

else:
    file    =   "./data_results/" + st.selectbox("Résultat",options=os.listdir('./data_results')) + "/"
    Volume  =   pd.read_csv(file + "volume.txt")
    Conso   =   pd.read_csv(file + "Conso.txt")
    Z       =   pd.read_csv(file + "ZZ.txt")
    Qpompe  =   pd.read_csv(file + "DebitPompe.txt")
    Gpompe  =   pd.read_csv(file + "ChargePompe.txt")
    States  =   pd.read_csv(file + "States.txt")
    Charge  =   pd.read_csv(file + "ChargeReseau.txt")

    st.plotly_chart(etat_RDE(Volume,Conso,Z),use_container_width=True)

    st.plotly_chart(Pompe_RDE(States,Gpompe,Qpompe,Z),use_container_width=True)

    st.plotly_chart(Charge_RDE(Charge,Z),use_container_width=True)