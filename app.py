# imported pandas for dataframe handling, streamlit for dashboard layout and styling, plotly.express for interactive and customised graphs
import pandas as pd
import streamlit as st
import plotly.express as px


# sets the top title and icon along with page layout; configures page   settings

st.set_page_config(page_title="Fish Dashboard", page_icon=":tropical_fish:", layout="centered")

# cache decorator is used in order to avoid loading of the dataset each and every time the page refreshes/re-renders

@st.cache
def get_data():
    data = pd.read_csv('Fish.csv')
    return data

# load data from dataset using the cached function
df = get_data()

# Place sidebar in the dashboard 
st.sidebar.title("Select filters")

# Set multiple multiselect / select options for dataset columns
species = st.sidebar.multiselect(
    "Select Species",
    options=df["Species"].unique(),
)

# sort function for presenting sorted list of options in selectboxes and unique function for including each value only once

length1 = df["Length1"].unique()
length1.sort()

length2 = df["Length2"].unique()
length2.sort()

length3 = df["Length3"].unique()
length3.sort()

verticalLength = st.sidebar.selectbox(
    "Minimum Vertical Length",
    length1,
)

diagonalLength = st.sidebar.selectbox(
    "Minimum Diagonal Length",
    length2,
)

crossLength = st.sidebar.selectbox(
    "Minimum Cross Length",
    length3,
)

# Initially set filtered data to be equal to original data; as a safety measure in case no filter is selected

filtered_data = df

# Filter dataset according to the applied filters one by one if available

if species:
    filtered_data = df.query("Species == @species")

if verticalLength:
    filtered_data = filtered_data.query("Length1 >= @verticalLength")

if diagonalLength:
    filtered_data = filtered_data.query("Length2 >= @diagonalLength")

if crossLength:
    filtered_data = filtered_data.query("Length3 >= @crossLength")

# Assign plotly chart objects to variable which will be rendered later below

weights = px.bar(
    filtered_data,
    y="Weight",
    color='Species',
)

heightVsWidth = px.scatter(
    filtered_data,
    x="Width",
    y="Height",
    color="Species",
    size="Weight",
)

# gives count of each unique value in dataset and their indexes respectively

spList = filtered_data["Species"].value_counts()
spIdx = spList.index.tolist()

speciesPie = px.pie(
    filtered_data,
    values=spList,
    names=spIdx,
    color_discrete_sequence=px.colors.qualitative.Prism
)

multiLine = px.line(
    filtered_data,
    x=filtered_data.index,
    y=["Length1","Length2","Length3"]
)

# update y axis label from default to custom according to need
multiLine.update_yaxes(title_text='Lengths')

# Render Page Heading/Title
st.title(':dolphin: Visualization Dashboard')

# Calculate averages of various columns to be displayed

avg_weight = filtered_data["Weight"].mean()

avg_len1 = filtered_data["Length1"].mean()
avg_len2 = filtered_data["Length2"].mean()
avg_len3 = filtered_data["Length3"].mean()

avg_height = filtered_data["Height"].mean()

avg_width = filtered_data["Width"].mean()

# Inserts containers on the page side by side as columns

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)
c5, c6 = st.columns(2)

# Display data within the column containers
with c1:
    st.code(f"Average Weight: {round(avg_weight)} gm")

with c2:
    st.code(f"Average Vertical Length: {round(avg_len1)} cm")

with c3:
    st.code(f"Average Diagonal Length: {round(avg_len2)} cm")

with c4:
    st.code(f"Average Cross Length: {round(avg_len3)} cm")

with c5:
    st.code(f"Average Height: {round(avg_height)} cm")

with c6:
    st.code(f"Average Width: {round(avg_width)} cm")

# Insert heading for the graphs and render graphs respectively in order

st.subheader('Species Distribution')
st.plotly_chart(speciesPie)

st.subheader('Comparison of Lengths')
st.plotly_chart(multiLine)

st.subheader("Weights")
st.plotly_chart(weights)

st.subheader("Height vs Width")
st.plotly_chart(heightVsWidth)

# Insert dataframe heading and display dataframe

st.subheader("Original/Filtered Dataset")
st.dataframe(filtered_data)

# set settings for removing menu, header and footer rendered automatically by streamlit

remove_st_preconfig = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """

# apply settings to remove preconfigured header, footer and menu
st.markdown(remove_st_preconfig, unsafe_allow_html=True)