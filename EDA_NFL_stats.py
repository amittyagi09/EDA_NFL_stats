import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("NFL PLayers Stats Data")
st.write("This web application perform NFL player stats data.")
st.write("**Python Libraries:** Pandas, Numpy, matplotlib, Seaborn")
st.write("**Data Source:** [Football-reference.com](https://www.pro-football-reference.com)")
st.write("***")


st.sidebar.header("User Input Features")
selected_year=st.sidebar.selectbox("Year", list(reversed(range(1995,2025))))

@st.cache_data
def load_data(year):
    url="https://www.pro-football-reference.com/years/{}/rushing.htm"
    html=url.format(2024)
    data=pd.read_html(html, header=1)
    data=data[0]
    final_data=data.fillna(0)
    final_data=final_data.drop("Rk", axis=1)
    return final_data

selected_data=load_data(selected_year)


selected_team=st.sidebar.multiselect("Team", selected_data["Team"].unique(), selected_data["Team"].unique())
selected_pos=st.sidebar.multiselect("Position", ["RB","QB","WR","FB","TE"], ["RB","QB","WR","FB","TE"])


df_data=selected_data[selected_data["Team"].isin(selected_team) & selected_data["Pos"].isin(selected_pos)]

st.header("Display stats of selected team")

st.write("**Data Dimensions:** "+str(df_data.shape[0])+" rows "+ str(df_data.shape[1])+" columns ")

st.dataframe(df_data)


if st.button("Heatmap"):
    st.header("Interrelation Heatmap")
    remove_columns=["Rk", "Player", "Pos", "Team", "Awards"]
    df_data=df_data.drop(columns=remove_columns, errors="ignore")
    df_data.to_csv("NFL_output.csv", index=False)
    data=pd.read_csv("NFL_output.csv")
    fig, ax=plt.subplots(figsize=(10,8))
    sns.heatmap(data.corr(), ax=ax, cmap="ocean", annot=True)    
    st.pyplot(fig)


