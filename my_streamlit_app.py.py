import numpy as np 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
import streamlit as st 
from PIL import Image

st.title("Car sales per continent and release year", anchor=None)

image = Image.open('car_example.jpg')
st.image(image)

link= "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
cars_df= pd.read_csv(link, sep=",")
cars_df["continent"]=cars_df["continent"].apply(lambda x: x.strip( " ").strip("."))
cols = cars_df.columns
re_ordered= ['continent','mpg', 'cylinders', 'cubicinches', 'hp', 'weightlbs', 'time-to-60', 'year'] #set "continent" as 1st column for button selection 
cars = cars_df[re_ordered]

#introduction txt
st.subheader('About this project, and the data it uses')
st.markdown("While studying data analytics at Wild Code School, we were requested to complete a streamlit quest. \
Streamlit is a Python Framework designed specifically for the purpose of sharing data and data visualisations. \
While relatively easy to start with, it is the first framework we'll be diving into and offer us a more elegant manner to share our work than colab or jupyter notebook.\
While approaching the near end of our data training at Wild Code School, it is great for us to be introduced to Streamlit. \n\n\
Please see below the dataframe we'll be working with.", unsafe_allow_html=False)

#visualisation 1 / dataframe filtré 
continent = st.multiselect("Select one or more continent to filter", options=cars["continent"].unique(), default=["Europe"],key=1) #bouton multiselect 
data = cars.set_index("continent").sort_values(by="year",ascending=True)
data.loc[continent,:]

#analyse de corrélation HEATMAPS
st.subheader('Correlation heatmap')
#1er paragraphe 
st.markdown("As requested in the assignment, se'll start with a correlation analysis to point out which features are related.\
What we can see from the heatmap below is", unsafe_allow_html=False)
select_box= st.selectbox('How would you like to be contacted?', options=cars["continent"].unique(),key=1)
heatmap_data= cars[cars["continent"]==select_box]
my_mask= np.triu(heatmap_data.corr())
heatmap = sns.heatmap(heatmap_data.corr(), annot=True, center=0, cmap = sns.color_palette("YlGnBu_r", as_cmap=True), mask=my_mask);
st.write(heatmap.figure) 
#widget TOP3 corrélations par continent 
st.subheader('TOP 3 correlations per continent')
#1er paragraphe 
st.markdown("Below are 3 widgets issued from an correlation heatmap that was turned into a dataframe.\
These widgets update with the select box selection, it is also possible to link the update of the widgets to the graphic above with little updates.", unsafe_allow_html=False)

select_box= st.selectbox('How would you like to be contacted?', options=cars["continent"].unique(), key=2)
heatmap_data= cars[cars["continent"]==select_box]
corr_unstacked = pd.DataFrame(heatmap_data.corr().unstack().reset_index())
top_corr = corr_unstacked[(corr_unstacked["level_0"] != corr_unstacked["level_1"])]\
    .sort_values(by=0,ascending=False)\
    .reset_index()\
    .drop(labels=[i for i in range(len(corr_unstacked[corr_unstacked["level_0"] != corr_unstacked["level_1"]])) if i%2 ==0])\
    .head(3)

top1 = top_corr.iloc[0,1] + " VS " + top_corr.iloc[0,2]
top2 = top_corr.iloc[1,1] + " VS " + top_corr.iloc[1,2]
top3 = top_corr.iloc[2,1] + " VS " + top_corr.iloc[2,2]

col1, col2, col3 = st.columns(3)
col1.metric(top1, round(top_corr.iloc[0,3],2))
col2.metric(top2, round(top_corr.iloc[1,3],2))
col3.metric(top3, round(top_corr.iloc[2,3],2))

#LINEPLOT filtré 
st.subheader('Line plot and related table for car sales per continent')
#1er paragraphe 
st.markdown("First we will be drawing a line plot to represent the evolution of car sales per release year. Default selection was set tot \'Europe\', \
to enable consulting the curve for that specific continent. Feel free to select/unselect continent, multiple continents may also be selected \
resulting in an overlap of curves (one color per continent).", unsafe_allow_html=False)

continent = st.multiselect("select one or more continent to update data", options=cars["continent"].unique(), default=["Europe"], key=2) #bouton multiselect 
data["continent1"]=data.index #colonne pour le groupby 
line_plot = data.loc[continent,:].groupby(["continent1", 'year']).count()[["cylinders"]]\
    .rename(columns={"cylinders":"number of cars"})\
    .unstack().fillna(0)\
    .T\
    .plot(kind="line", figsize=(20,8));
st.write(line_plot.figure)
#affichage du data lié au line plot 
#2ème paragraphe 
st.markdown("The update of the continent using the multiselect button updates both the graph here above and the table below.\
For all continents (single or multiple selections), we can easily read all car sales per release year in the table and see the trend in the graph.", unsafe_allow_html=False)
data_filtered = data.loc[continent,:].groupby(['continent1', 'year']).count()[["cylinders"]]\
    .rename(columns={"cylinders":""})\
    .fillna(0)\
    .unstack()
data_filtered

#single_bar_chart filtré 
st.subheader('Single bar chart for car sales per continent')
#1er paragraphe 
st.markdown("Below is an example of a bar chart with a single continent selection. Feel free to select another continent to update the graph.", unsafe_allow_html=False)

choice = st.radio("select a continent top update chart", options=cars["continent"].unique())
bar_chart = data.loc[choice,:].groupby(['continent1', 'year']).count()[["cylinders"]]\
    .rename(columns={"cylinders":"number of cars"})\
    .unstack().fillna(0)\
    .plot(kind="bar", title="Number of cars per release year", ylabel="number of cars sold", stacked=False, xlabel="",rot=0 , figsize=(15,8))
st.write(bar_chart.figure)

#stacked_bar_chart filtré 
st.subheader('Stacked bar chart for car sales per continent')
#1er paragraphe 
st.markdown("We can also draw a stacked barplot to represent car sales for one or more continents. \
Drawing this stacked barchart makes it easy to compare car sales per release year.", unsafe_allow_html=False)

continent = st.multiselect("select one or more continent to update data", options=cars["continent"].unique(), default=["Europe"], key=3) #bouton multiselect 
stacked_bar_chart = data.loc[continent,:].groupby(['continent1', 'year']).count()[["cylinders"]]\
    .sort_values(by=["continent1", "cylinders"], ascending=False)\
    .fillna(0)\
    .unstack()\
    .T\
    .plot(kind="bar",stacked=True,figsize=(20,8),xlabel="");
st.write(stacked_bar_chart.figure)
