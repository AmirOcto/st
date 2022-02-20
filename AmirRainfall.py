from importlib.resources import path
from turtle import end_fill
from nbformat import write
import pandas as pd
import numpy as np
import streamlit as st

import plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

from pathlib import Path
import base64

# Initial page config

st.set_page_config(
     page_title='Streamlit India Rainfall Analysis',
     layout="wide",
     page_icon= ':droplet:',
     initial_sidebar_state="expanded",
)

def img_to_bytes(img_path):
    #to encode an image into a string
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=150 height=85>](https://www.aub.edu.lb/)'''.format(img_to_bytes("AUB.png")), 
                    unsafe_allow_html=True)

st.sidebar.header('Streamlit India Rainfall Analysis')

st.sidebar.markdown('''
<small>This [Dataset](https://www.kaggle.com/saisaran2/rainfall-data-from-1901-to-2017-for-india), was taken from [Kaggle](https://www.kaggle.com/).</small>
    ''', unsafe_allow_html=True)


menu = st.sidebar.selectbox(
    "Analysis Menu",
    ("Introduction", "Exploratory Analysis", "Interactive Map")
)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('Amir Bazzi | Msba 2022 \n\n arb11@mail.aub.edu ')

header = st.container()

#Rainfall Data from 1901 to 2017 for India
#This is the rainfall data with coordinates for India (by Sub-divison)
with header:
   st.write(""" # Rainfall Analysis in India :droplet: 
   In this project, I look into rainfall amounts across different cities in india over different months since 1901 till 2017.""")
   

df= pd.read_csv('Rainfall_Data_LL.csv')

#Create season features
df['Q1'] = df['DEC']+df['JAN']+df['FEB']
df['Q2'] = df['MAR']+df['APR']+df['MAY']
df['Q3'] = df['JUN']+df['JUL']+df['AUG']
df['Q4'] = df['SEP']+ df['OCT']+df['NOV']

#Drop unneccesary columns
to_drop = ['Jan-Feb','Mar-May','June-September', 'Oct-Dec']
df.drop(to_drop, axis=1, inplace=True )

#Rename Columns
df=df.rename(columns={"Name":"Index","SUBDIVISION": "Regions"})

df.columns = df.columns.str.capitalize()

#Create monthly average rain amount 
df["Month Average"] = df['Annual']/12

shape = df.shape
columns = df.columns

regions_number = df['Regions'].nunique() #36 unique region 
no_year = df['Year'].nunique() #117 year
final_year = df['Year'].max() #2017
start_year = df['Year'].min() #1901

if menu=='Introduction':
    st.subheader('Indian Climate Introduction')
    col1_1, col1_2 =st.columns([2,1])
    with col1_1:
        mark ='''
        <p> In this exercise we will dive into the different rainfall amounts across different cities in India using the The data is fetched from data.gov.in in order to validate its climate map. 
        This dataset lists all prize winners from the start of the prize in 1901 till 2016.</p>
        <p> India experiences a variety of climates ranging from tropical in the south to temperate and alpine in the Himalayan north. 
        The elevated areas receive sustained snowfall during winters. 
        The Himalayas and the Thar Desert strongly influence the climate of the country. 
        The Himalayas work as a barrier to the frigid katabatic winds, which blow down from Central Asia. 
        The Tropic of Cancer passes through the middle of the country, and this makes its climate more tropical. 
        India is a big tropical country and is famous for its diverse climatic features. (image to the right)</p>


        <p>Unless there are immediate and large-scale reductions in greenhouse gas emissions, 
        limiting global warming to close to 1.5 degrees Celsius or even 2 degrees Celsius over pre-industrial times will be beyond reach, 
        the latest report by the Intergovernmental Panel on Climate Change (IPCC), released earlier this week, has shown. 
        '''
        st.markdown(mark, unsafe_allow_html=True)
    
    with col1_2:
        st.image('Climate-zones-of-India.png',width=400, caption='Indian Climate Map')
if menu=='Exploratory Analysis':
    
    st.header('Exploratory Analysis')
    EDA = st.radio(
     "",
     ('Dataset Exploration', 'Data Visualization'))

    if EDA == 'Dataset Exploration':

        st.markdown('''### Data Preview''')
        total_rows = df.shape[0]
        n = st.slider('Choose the number of rows you would like to see from the data', 0, total_rows, 5)
        st.write(df.head(n))

        data_bool = st.checkbox("Show Dataset Specifications")
        if data_bool:
            st.write('Shape of dataset : ', shape)
            st.write('Number of Regions : ', regions_number)
            st.write('Number of years : ', no_year)
            st.write('First year recorded : ',start_year)
            st.write('Last year recorded : ',final_year)
            st.write('Fields of the data is below:', df.columns)
            
        RegionList = df.groupby('Regions').count().index
        st.header('Rain Distribution Across Cities Over The Quarters')
        st.markdown("### **Filter Rain Amount by Region:**")
        selection = st.selectbox('', RegionList)
        #Filter df based on selection
        Regiondf = df[ df['Regions'] == selection ]
        
        st.write('Variation of the annual rain amount in %s :' % selection)
        st.write(Regiondf[['Regions','Year','Annual']])

    if EDA == 'Data Visualization':

            menu2 = st.selectbox(
            "Select the visualization",
            ("Rain Distribution Across Cities Over The Quarters", 
            "Average Rain Per City",
            "Rain Amount Variation in Each Region"
            )
            )
            if menu2 == "Rain Distribution Across Cities Over The Quarters":
                st.header("Rain Distribution Across Cities Over The Quarters")

                year_to_filter = st.slider('year', 1901, 2017, 2015)
                filtered_data = df[df['Year'] == year_to_filter]

                Q1 = go.Bar(x=filtered_data.Regions,
                        y=filtered_data.Q1,
                        name='Q1',
                        marker=dict(color='#1830D2'))

                Q2 = go.Bar(x=filtered_data.Regions,
                        y=filtered_data.Q2,
                        name='Q2',
                        marker=dict(color='#A25E1A'))

                Q3 = go.Bar(x=filtered_data.Regions,
                        y=filtered_data.Q3,
                        name='Q3',
                        marker=dict(color='#1DCC10'))

                Q4 = go.Bar(x=filtered_data.Regions,
                        y=filtered_data.Q4,
                        name='Q4',
                        marker=dict(color='#EFEB12'))

                data = [Q1, Q2, Q3, Q4]

                layout = go.Layout(title="Rainfall Amount Per Quarter",
                        xaxis=dict(title='Regions'),
                        yaxis=dict(title='Rainfall'),
                        width=1200, height=700
                        )
                fig = go.Figure(data=data, layout=layout)
                st.write(fig)

            if menu2 =="Average Rain Per City":

                col1, col2 = st.columns(2)
                with col1:
                    st.header('Average Rain Amount Per City - Annualy')

                    regions_list = df.groupby('Regions')['Regions']
                    print(type(regions_list))

                    df["AnnualAverage"] = df['Annual']/12
                    AnnualAverage = df[["Regions","AnnualAverage"]].groupby("Regions").mean().reset_index()
                    print(AnnualAverage)
                    
                    fig = px.bar(AnnualAverage, x='Regions', y='AnnualAverage', color='AnnualAverage',
                            labels={'AnnualAverage':'Average Annual Rain'}, height=500, width= 600)

                    st.write(fig)

                with col2:
                    st.header('Average Rain Amount Per City - Monthly')

                    melt_df = df[ ['Regions','Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
                    melted_df = pd.melt(melt_df, id_vars=['Regions'], var_name='Month' ,value_name='Rain')
                    print(melted_df)

                    melted_grouped = melted_df.groupby('Month').mean()
                    melted_grouped_df = pd.DataFrame(melted_grouped)
                    melted_grouped_df = melted_grouped_df.reset_index()
                    print(melted_grouped_df)

                    melted_grouped_R_M = melted_df.groupby(['Regions','Month']).mean()
                    melted_grouped_R_M_df = melted_grouped_R_M_df = pd.DataFrame(melted_grouped_R_M)
                    melted_grouped_R_M_df = melted_grouped_R_M_df.reset_index()
                    melted_grouped_R_M_df = melted_grouped_R_M_df.sort_values('Month')
                    print(melted_grouped_R_M_df)

                    fig = px.line(melted_grouped_R_M_df, x="Month", y="Rain", color='Regions')
                    st.write(fig)

                    Top_months = melted_grouped_df.nlargest(4, 'Rain')
                    st.write("The top 4 months with the highest amount of rain are : " , Top_months)

            if menu2=="Rain Amount Variation in Each Region":

                    st.header('Rain Amount Variation in Each Region')
                    regions = df['Regions']
                    rain = df['Annual']
                    year = df['Year']

                    fig = px.bar(df, x=regions, y=rain, color=regions,
                    animation_frame=year, animation_group=regions, range_y=[0,10000],text_auto='.2s',
                                title="Rain Amount Variation in Each Region", width=1200, height=700)
                    st.write(fig)
                    
if menu=='Interactive Map':
    st.header('Rain Amount Distiribution Across Indian Cities')
    RegionList = df.groupby('Regions').count().index
    selection2 = st.selectbox('', RegionList)
    #Filter df based on selection
    Regiondf2 = df[ df['Regions'] == selection2 ]

    map_avg = Regiondf2.groupby('Regions').mean()
    map_df = pd.DataFrame(map_avg)
    map_df = map_df.reset_index()


    map_df_fig = map_df[['Regions', 'Annual']]
    map_df_fig[['Latitude', 'Longitude']] = map_df[['Latitude', 'Longitude']]
    

    px.set_mapbox_access_token(open("C:\\Users\\Amir\\Desktop\\Rainfall_data\\mapbox_token.txt").read())

    fig = px.scatter_mapbox(map_df_fig, lat="Latitude", lon="Longitude", size="Annual", color="Regions",
                            text = map_df_fig['Regions'], hover_name=map_df_fig['Regions'], color_continuous_scale=px.colors.cyclical.IceFire, 
                            size_max=50, 
                            center=dict(lat=20.5937, lon=78.9629), zoom =3
                            )

    fig.add_trace(go.Scattermapbox(
            lat=map_df_fig['Latitude'],
            lon=map_df_fig['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            hoverinfo='none'
        ))

    fig.update_layout(
        title='Indian Cities Average Rainfall 1901-2017',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        width=1200,
        height =700)

    st.write(fig)
