import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

@st.cache
def get_variable(file):
    """
    This function reads an Excel file and extracts the data for variables that have a count greater than 1.

    Args:
        file (str): The path to the Excel file.

    Returns:
        dict: A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
    """
    a = pd.read_excel(file)
    data_variable = {}
    # Extract the names of the variables that have a count greater than 1
    for var in a[(a["Type"]=='variable')&(a["Count"]>1)]['Name']:
        # Read the data for each variable from the Excel file
        data_variable[var] = pd.read_excel(file, sheet_name=var, header=2)
    return data_variable

def get_parameter(file):
    """
    This function reads an Excel file and extracts the data for parameters that have a count greater than 1.

    Args:
        file (str): The path to the Excel file.

    Returns:
        dict: A dictionary containing the data for each parameter. The keys are the parameter names, and the values are pandas DataFrames containing the data for each parameter.
    """
    a = pd.read_excel(file)
    data_parameter = {}
    # Extract the names of the parameters that have a count greater than 1
    for var in a[(a["Type"]=='parameter')&(a["Count"]>1)]['Name']:
        # Read the data for each parameter from the Excel file
        data_parameter[var] = pd.read_excel(file, sheet_name=var, header=2)
    return data_parameter

def get_set(file):
    """
    This function reads an Excel file and extracts the data for sets that have a count greater than 1.

    Args:
        file (str): The path to the Excel file.

    Returns:
        dict: A dictionary containing the data for each set. The keys are the set names, and the values are pandas DataFrames containing the data for each set.
    """
    a = pd.read_excel(file)
    data_set = {}
    # Extract the names of the sets that have a count greater than 1
    for var in a[(a["Type"]=='set')&(a["Count"]>1)]['Name']:
        # Read the data for each set from the Excel file
        data_set[var] = pd.read_excel(file, sheet_name=var, header=2)
    return data_set

def comments(file):
    """
    This function reads the 'comments' sheet in an Excel file and displays the comments in a markdown format.

    Args:
        file (str): The path to the Excel file.
    """
    with st.expander("Commentaires",expanded=False):
        try:
            # Read the comments from the 'comments' sheet in the Excel file
            comments =  pd.read_excel(file,sheet_name='comments').iloc[0,0]
            # Display the comments in a markdown format
            st.markdown(comments)
        except:
            # If there are no comments, display a message
            st.markdown("Pas de commentaires")

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
    """
    This function creates a plot showing the state of the water distribution network.
    Args:
        data_variable (dict): A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
        Z (float): The cost of the water distribution network.
        Margin (bool, optional): Whether to add a margin to the top of the plot. Default is False.

    Returns:
        plotly.graph_objects.Figure: A plot showing the state of the water distribution network.
    """
    fig = go.Figure()
    # Add a bar plot for each unique value of 'n' in the 'v' DataFrame
    for r in data_variable['v']['n'].unique():
        fig.add_trace(
            go.Bar(
                x   =  data_variable['v'][data_variable['v']['n']==r]['t'],
                y   =  data_variable['v'][data_variable['v']['n']==r]['Value'],
                name=   r
            )
        )
    # Add a scatter plot for each unique pair of values of 'c' and 'd' in the 'Ppompe' DataFrame
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
    # Update the layout of the plot
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
            # range=[df["Co??t MWh"].min()*0.95,df["Co??t MWh"].max()*1.1],
            anchor="free",
            overlaying="y",
            side="right",
            position=1
            ),
            title = f"Etat du r??seau de distribution d'eau - Co??t : {Z} ???"
        )
    # If Margin is True, add a margin to the top of the plot
    if Margin:
        fig.update_layout(
            margin_t = 120
        )
    return fig

def Pompe_RDE(data_variable,Z,Margin=False):
    """
    This function creates a plot showing the state of the pumps in the water distribution network.

    Args:
        data_variable (dict): A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
        Z (float): The cost of the water distribution network.
        Margin (bool, optional): Whether to add a margin to the top of the plot. Default is False.

    Returns:
        plotly.graph_objects.Figure: A plot showing the state of the pumps in the water distribution network.
    """
    color_map   =   {
        'p1'    :   'red',
        'p2'    :   'blue',
        'p3'    :   'green',
        'p4'    :   'magenta',
    }
    color_map_light   =   {
        'p1'    :   'lightcoral',
        'p2'    :   'lightblue',
        'p3'    :   'lightgreen',
        'p4'    :   'plum'    
    }
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x               =   data_variable['Charge'][data_variable['Charge']['n']=='s']['t'],
            y               =   data_variable['Charge'][data_variable['Charge']['n']=='s']['Value'],
            marker_color    =   'black',
            line_dash       =   'dash',
            name            =   f"Charge ?? s"
        )
    )
    for c in data_variable['Qpompe']['c'].unique():
        for d in data_variable['Qpompe']['d'].unique():
            fig.add_trace(
                go.Scatter(
                    x               =   data_variable['Qpompe'][(data_variable['Qpompe']['c']==c)&(data_variable['Qpompe']['d']==d)]['t'],
                    y               =   data_variable['Qpompe'][(data_variable['Qpompe']['c']==c)&(data_variable['Qpompe']['d']==d)]['Value'],
                    marker_color    =   color_map[d],
                    name            =   f"D??bit {c},{d}",
                    stackgroup='one'
                )
            )
    fig.update_layout(
        hovermode='x',
        title = f"Etat des pompes du r??seau de distribution d'eau - Co??t : {Z} ??? "
        )
    if Margin:
        fig.update_layout(
            margin_t = 150
        )
    return fig

def Charge_RDE(data_variable,Z):
    """
    This function creates a plot showing the charge in the water distribution network.
    Args:
        data_variable (dict): A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
        Z (float): The cost of the water distribution network.

    Returns:
        plotly.graph_objects.Figure: A plot showing the charge in the water distribution network.
    """
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
        title = f"Charge dans le r??seau de distribution d'eau - Co??t : {Z} ??? ",
        yaxis_title = "Charge (m)"
    )
    return fig

def Etat_reservoir(data_variable,data_set,data_parameter,reservoir):
    """
    This function creates a plot showing the state of a given reservoir in the water distribution network.
    Args:
        data_variable (dict): A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
        data_set (dict): A dictionary containing the data for each set. The keys are the set names, and the values are pandas DataFrames containing the data for each set.
        data_parameter (dict): A dictionary containing the data for each parameter. The keys are the parameter names, and the values are pandas DataFrames containing the data for each parameter.
        reservoir (str): The name of the reservoir to plot.

    Returns:
        plotly.graph_objects.Figure: A plot showing the state of the given reservoir in
    """
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

def path_to_n(n,data_set):
    """
    This function returns the path from the given node to the source node in the water distribution network.

    Args:
        n (str): The name of the node.
        data_set (dict): A dictionary containing the data for each set. The keys are the set names, and the values are pandas DataFrames containing the data for each set.
    
    Returns:
        list: A list containing the names of the nodes from the given node to the source node.
    """
    path = [n]
    while n !='s':
        n = data_set['l'][data_set['l']['n.1']==n]['n'].iloc[0]
        path.append(n)
    return path

def Chemin_charge(data_parameter,data_variable,data_set,n):
    """
    This function creates a plot showing the height and charge at each node along a path from the source node to a given node in the water distribution network.
    
    Args:
        data_parameter (dict): A dictionary containing the data for each parameter. The keys are the parameter names, and the values are pandas DataFrames containing the data for each parameter.
        data_variable (dict): A dictionary containing the data for each variable. The keys are the variable names, and the values are pandas DataFrames containing the data for each variable.
        data_set (dict): A dictionary containing the data for each set. The keys are the set names, and the values are pandas DataFrames containing the data for each set.
        n (str): The name of the node to end at.
    
    Returns:
        plotly.graph_objects.Figure: A plot showing the height and charge at each node along the path from the source node to the given node.
    """
    # Initialize a Figure object
    fig = go.Figure()
    
    # Get the path from the source node to the given node
    path = path_to_n(n,data_set)
    path = path[::-1]
    fig.add_trace(
        go.Scatter(
            x = path,
            y = pd.concat([pd.DataFrame([['s',0,0]],columns=data_parameter['height'].columns),data_parameter['height'][data_parameter['height']['n'].isin(path)]])['Value'],
            name = 'hauteur'
        )
    )
    for t in data_set['t']['dim1']:
        # if t == 't1':
        fig.add_trace(
        go.Scatter(
            x = path,
            y = data_variable['Charge'][(data_variable['Charge']['n'].isin(path))&(data_variable['Charge']['t']==t)]['Value'],
            name = t,
            # visible='legendonly'
        )
        )
    fig.update_layout(
        hovermode='x',
        height = 700,
        title = n
    )
    return fig

st.set_page_config(layout="wide")

comparaison = st.checkbox("Comparaison")
if comparaison:
    col_1,col_2 = st.columns(2)
    with col_1:
        file    =   "./data_results/" + st.selectbox("R??sultat 1",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
        Z = np.round(pd.read_excel(file,sheet_name='Scalar').iloc[8,2],4)
        data_variable = get_variable(file)
        data_parameter = get_parameter(file)
        comments(file)
        st.plotly_chart(etat_RDE(data_variable,Z,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(data_variable,Z,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(data_variable,Z),use_container_width=True)
    with col_2:
        file2    =   "./data_results/" + st.selectbox("R??sultat 2",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
        Z2 = np.round(pd.read_excel(file2,sheet_name='Scalar').iloc[8,2],4)
        data_variable2 = get_variable(file2)
        data_parameter2 = get_parameter(file2)
        comments(file2)
        st.plotly_chart(etat_RDE(data_variable2,Z2,True),use_container_width=True)

        st.plotly_chart(Pompe_RDE(data_variable2,Z2,True),use_container_width=True)

        st.plotly_chart(Charge_RDE(data_variable2,Z2),use_container_width=True)

else:
    file    =   "./data_results/" + st.selectbox("R??sultat",options=[file for file in os.listdir('./data_results') if file.endswith('.xlsx')])
    Z = np.round(pd.read_excel(file,sheet_name='Scalar').iloc[8,2],4)
    data_variable = get_variable(file)
    data_parameter = get_parameter(file)
    data_set = get_set(file)
    comments(file)
    st.plotly_chart(etat_RDE(data_variable,Z),use_container_width=True)

    with st.expander(label="Aide",expanded=False):
        st.markdown(
            '''
            Ce graphique permet de visualiser en fonction du temps l'??tat des r??servoirs et des pompes. L'??tat des r??servoir est d??crit par le volume dans les r??servoirs. L'??tat des pompe est d??crit par la consommation ??lectrique de chaque pompe.
            ''',
            unsafe_allow_html=True
        )

    st.plotly_chart(Pompe_RDE(data_variable,Z),use_container_width=True)

    with st.expander(label="Aide", expanded=False):
        st.markdown(
            '''
            Ce graphique d??taille l'??tat des pompes du r??seau dans le temps. Il montre le d??bit cumul?? des pompes. Il est ?? not?? que les pompes sont branch??es en parall??les, il n'y a donc qu'une seul charge possible au borne de ces pompes.<br>
            En th??orie, le d??bit des pompes d'un m??me type est identique. Cependant les relaxations convexes du mod??le peuvent conduire ?? des d??bits diff??rents pour des pompes du m??me type.
            ''',
            unsafe_allow_html=True
        )

    st.plotly_chart(Charge_RDE(data_variable,Z),use_container_width=True)

    with st.expander(label="Aide", expanded=False):
        st.markdown(
            '''
            Ce graphique d??taille la charge dans le temps de tous les noeuds du r??seau. Lorsqu'il n'y a pas de d??bit dans le r??seau, la charge dans le rseau est libre (le r??seau est ?? l'arr??t).
            ''',
            unsafe_allow_html=True
        )

    with st.expander('Donn??es',expanded=False):
        variable = st.selectbox("Variable",options=data_variable.keys())
        index = st.multiselect("Ligne",data_variable[variable].columns)
        column = st.multiselect("Colonne",data_variable[variable].columns)
        value = st.selectbox("Valeur",data_variable[variable].columns)
        # st.dataframe(data_variable[variable])
        try:
            st.dataframe(pd.pivot_table(data_variable[variable], values=value, index=index,columns=column, aggfunc=np.sum))
        except:
            st.text("Param??tres mal choisis")

    st.markdown('## Etat dans chaque r??servoir')
    with st.expander(label='Aide',expanded=False):
        st.markdown(
            '''
            Ci-dessous, chaque r??servoir a deux graphiques associ??s. Le premier donnee l'??volution des entr??es et des sorties d'eaux du r??servoir ainsi que l'??volution du volume d'eau (par rapport au volume minimum). En-dessous du premier graphique, un deuxi??me graphique montre pour le m??me r??servoir l'??volution de la charge dans le r??seau de la source jusqu'au r??servoir pour des instants fix??s. Ainsi que la hauteur dans chaque noeud de ce chemin (pour comparaison). La charge est n??cessairement d??croissante dans le chemin de la source au r??servoir. Une des contraintes est que la charge doit toujours ??tre sup??rieure ?? la hauteur.
            ''',
            unsafe_allow_html=True
        )
    liste_reservoir = data_set['r']['n']
    k = len(liste_reservoir)//4
    # st.text(f"{liste_reservoir[0:4]}")
    for s in range(k):
        print(s)
        liste_columns = st.columns(4)
        for i,reservoir in enumerate(liste_reservoir[s*4:(s+1)*4]):
            with liste_columns[i%4]:
                st.plotly_chart(Etat_reservoir(data_variable,data_set,data_parameter,reservoir),use_container_width=True)
                st.plotly_chart(Chemin_charge(data_parameter,data_variable,data_set,reservoir),use_container_width=True)