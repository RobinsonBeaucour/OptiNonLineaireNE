import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

@st.cache
def recup_variable(file):
    a = pd.read_excel(file)
    data_variable = {}
    for var in a[(a["Type"]=='variable')&(a["Count"]>1)]['Name']:
        data_variable[var] = pd.read_excel(file,sheet_name=var,header=2)
    return data_variable
def recup_parameter(file):
    a = pd.read_excel(file)
    data_variable = {}
    for var in a[(a["Type"]=='parameter')&(a["Count"]>1)]['Name']:
        data_variable[var] = pd.read_excel(file,sheet_name=var,header=2)
    return data_variable
def recup_set(file):
    a = pd.read_excel(file)
    data_variable = {}
    for var in a[(a["Type"]=='set')&(a["Count"]>1)]['Name']:
        data_variable[var] = pd.read_excel(file,sheet_name=var,header=2)
    return data_variable

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

def etat_RDE(data_variable,Z,Margin=False):
    Z = 2
    fig = go.Figure()
    for r in data_variable['v']['n'].unique():
        fig.add_trace(
            go.Bar(
                x   =  data_variable['v'][data_variable['v']['n']==r]['t'],
                y   =  data_variable['v'][data_variable['v']['n']==r]['Value'],
                name=   r
            )
        )
    for c in data_variable['Ppompe']['c'].unique():
        for d in data_variable['Ppompe']['d'].unique():
            fig.add_trace(
                go.Scatter(
                    x   =   data_variable['Ppompe'][(data_variable['Ppompe']['c']==c)&(data_variable['Ppompe']['d']==d)]['t'],
                    y   =   data_variable['Ppompe'][(data_variable['Ppompe']['c']==c)&(data_variable['Ppompe']['d']==d)]['Value'],
                    yaxis="y2",
                    name=   f"({c},{d})"
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
            title = f"Etat du réseau de distribution d'eau - Coût : {Z} €"
        )
    if Margin:
        fig.update_layout(
            margin_t = 120
        )
    return fig

def Pompe_RDE(data_variable,Z,Margin=False):
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
    # for c in data_variable['Son']['c'].unique():
    #     for d in data_variable['Son']['d'].unique():
    #         fig.add_trace(
    #             go.Bar(
    #                 x               =   data_variable['Son'][(data_variable['Son']['c']==c)&(data_variable['Son']['d']==d)]['t'],
    #                 y               =   10*data_variable['Son'][(data_variable['Son']['c']==c)&(data_variable['Son']['d']==d)]['Value'],
    #                 marker_color    =   color_map_light[d],
    #                 name            =   f"Statut {c},{d}"
    #             )
    #         )
    # fig.update_layout(
    #     barmode="stack"
    # )
    fig.add_trace(
        go.Scatter(
            x               =   data_variable['Charge'][data_variable['Charge']['n']=='s']['t'],
            y               =   data_variable['Charge'][data_variable['Charge']['n']=='s']['Value'],
            marker_color    =   'black',
            line_dash       =   'dash',
            name            =   f"Charge à s"
        )
    )
    for c in data_variable['Qpompe']['c'].unique():
        for d in data_variable['Qpompe']['d'].unique():
            fig.add_trace(
                go.Scatter(
                    x               =   data_variable['Qpompe'][(data_variable['Qpompe']['c']==c)&(data_variable['Qpompe']['d']==d)]['t'],
                    y               =   data_variable['Qpompe'][(data_variable['Qpompe']['c']==c)&(data_variable['Qpompe']['d']==d)]['Value'],
                    marker_color    =   color_map[d],
                    name            =   f"Débit {c},{d}",
                    stackgroup='one'
                )
            )
    fig.update_layout(
        hovermode='x',
        title = f"Etat des pompes du réseau de distribution d'eau - Coût : {Z} € "
        )
    if Margin:
        fig.update_layout(
            margin_t = 150
        )
    return fig

def Charge_RDE(data_variable,Z):
    fig = go.Figure()
    for n in data_variable['Charge']['n'].unique():
        fig.add_trace(
            go.Scatter(
                x = data_variable['Charge'][data_variable['Charge']['n']==n]['t'],
                y = data_variable['Charge'][data_variable['Charge']['n']==n]['Value'],
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
        title = f"Charge dans le réseau de distribution d'eau - Coût : {Z} € ",
        yaxis_title = "Charge (m)"
    )
    return fig

def Etat_reservoir(data_variable,data_set,data_parameter,reservoir):
    fig = go.Figure()
    demand = pd.merge(data_set['t'][['dim1']].rename(columns={'dim1':'t'}),data_parameter['demand'][data_parameter['demand']['r']==reservoir],on=['t'],how='left')
    demand['Value'] = demand['Value'].fillna(0)
    fig.add_trace(
        go.Scatter(
            x = demand['t'],
            y = -demand['Value'],
            stackgroup='one',
            name = 'Demande'
        )
    )

    fig.add_trace(
        go.Scatter(
            x = data_set['t']['dim1'],
            y = sum(data_variable['Qpipe'][(data_variable['Qpipe']['n.1']==reservoir)&(data_variable['Qpipe']['n']==n)]['Value'] for n in data_set['l'][data_set['l']['n.1']==reservoir]['n']),
            stackgroup='two',
            name = 'Approvisionnement'
        )
    )
    fig.add_trace(
        go.Scatter(
            x = data_set['t']['dim1'],
            y = data_variable['v'][data_variable['v']['n']==reservoir]['Value']-data_variable['v'][data_variable['v']['n']==reservoir]['Lowerbound'],
            name = 'Volume - Volume min'
        )
    )
    fig.update_layout(
        hovermode='x',
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                ),
        title = reservoir,
        margin_t = 200,
        height=700
    )
    return fig


st.set_page_config(layout="wide")

comparaison = st.checkbox("Comparaison")
Z = 2
if comparaison:
    col_1,col_2 = st.columns(2)
    with col_1:
        file    =   "./data_results/" + st.selectbox("Résultat 1",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
        data_variable = recup_variable(file)
        data_parameter = recup_parameter(file)
        st.plotly_chart(etat_RDE(data_variable,Z,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(data_variable,Z,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(data_variable,Z),use_container_width=True)
    with col_2:
        file2    =   "./data_results/" + st.selectbox("Résultat 2",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
        data_variable2 = recup_variable(file2)
        data_parameter2 = recup_parameter(file2)

        st.plotly_chart(etat_RDE(data_variable2,Z2,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(data_variable2,Z2,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(data_variable2,Z2),use_container_width=True)

else:
    file    =   "./data_results/" + st.selectbox("Résultat",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
    data_variable = recup_variable(file)
    data_parameter = recup_parameter(file)
    data_set = recup_set(file)

    st.plotly_chart(etat_RDE(data_variable,Z),use_container_width=True)

    st.plotly_chart(Pompe_RDE(data_variable,Z),use_container_width=True)

    st.plotly_chart(Charge_RDE(data_variable,Z),use_container_width=True)

   
    with st.expander('Données',expanded=False):
        variable = st.selectbox("Variable",options=data_variable.keys())
        index = st.multiselect("Ligne",data_variable[variable].columns)
        column = st.multiselect("Colonne",data_variable[variable].columns)
        value = st.selectbox("Valeur",data_variable[variable].columns)
        # st.dataframe(data_variable[variable])
        try:
            st.dataframe(pd.pivot_table(data_variable[variable], values=value, index=index,columns=column, aggfunc=np.sum))
        except:
            st.text("Paramètres mal choisis")

    liste_reservoir = data_set['r']['n']
    liste_columns = st.columns(len(liste_reservoir))
    for i,reservoir in enumerate(liste_reservoir):
        with liste_columns[i]:
            st.plotly_chart(Etat_reservoir(data_variable,data_set,data_parameter,reservoir),use_container_width=True)