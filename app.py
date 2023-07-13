import pickle
import datetime
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
   page_title="Movie Recommender System App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
# d = st.date_input(
#     "When\'s your birthday",
#     datetime.date(2019, 7, 6))
# st.write('Your birthday is:', d)

st.title('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame (movies_dict)

hide = """
<style>
div[data-testid="stConnectionStatus"] {
    display: none !important;
</style>
"""

st.markdown(hide, unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=263cccc7902c444e5a0231f11b54d71f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']== movie ].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse = True,key= lambda x:x[1])[1:11]
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API 
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

selected_movie_name = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.image(posters[0])
        st.info(names[0])
    with c2:
        st.image(posters[1])
        st.info(names[1])
    with c3:
        st.image(posters[2])
        st.info(names[2])
    with c4:
        st.image(posters[3])
        st.info(names[3])
    with c5:
        st.image(posters[4])
        st.info(names[4])

    st.header("Some other Movies")
    c6, c7, c8, c9, c10 = st.columns(5)
    with c6:
        st.image(posters[5])
        st.info(names[5])
    with c7:
        st.image(posters[6])
        st.info(names[6])
    with c8:
        st.image(posters[7])
        st.info(names[7])
    with c9:
        st.image(posters[8])
        st.info(names[8])
    with c10:
        st.image(posters[9])
        st.info(names[9])
