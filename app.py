import streamlit as st
import pandas as pd
from scipy import sparse
import requests
from sklearn.metrics.pairwise import cosine_similarity

movies_info=pd.read_csv('movies_info_final.csv')
movies_data=sparse.load_npz('final_df.npz')
API_KEY='260675a3aa8e259a0663a56d53615ceb'
preds=None

def get_poster(imdb_id):
    url='https://api.themoviedb.org/3/find/'+str(imdb_id)+'?api_key='+API_KEY+'&external_source=imdb_id'
    response=requests.get(url)
    data=response.json()
    poster_id=data['movie_results'][0]['poster_path']
    return "http://image.tmdb.org/t/p/w500"+poster_id

def make_recommandations(movies):
    if movies==[]:
        pass
    else:
        input_data=0
        for movie in movies:
            input_data+=movies_data[movies_info.title==movie]
        similarities=pd.DataFrame(cosine_similarity(movies_data, input_data), columns=['similarity'])
        df_with_similarities=pd.concat([movies_info, similarities], axis=1)
        df_with_similarities=df_with_similarities[['title', 'imdb_link', 'similarity']].sort_values(by='similarity', ascending=False)
        return df_with_similarities

st.set_page_config(page_title='Movie Recommender', layout='wide')
st.title("Movie Recommender :movie_camera:")

col1, col2 = st.columns(2)

with col1:
    movie=st.multiselect('Select your favourite movies (up to 3)', list(movies_info.title.sort_values()), max_selections=3, key='movies_input', placeholder='Choose a movie')
    if movie==[]:
        st.write("")
    else:
        st.header("Selected movies")
        for title in movie:
            imdb_link=movies_info[movies_info.title==title]['imdb_link'].values[0]
            st.write(title, imdb_link)
        st.write("Posters of selected movies:")
        with st.empty():
            images=[]
            titles=[]
            for title in movie:
                try:
                    imdb_id=movies_info[movies_info.title==title]['imdb_id'].values[0]
                    poster_link=get_poster(imdb_id)
                    images.append(poster_link)
                    titles.append(title)
                except:
                    st.write(title)
                st.image(images, caption=titles, width=150)
        is_clicked=st.button(label="Recommend")
        if is_clicked:
            preds=make_recommandations(movie)

with col2:
    st.header("Recommandations:")
    if preds is not None:
        st.dataframe(preds, hide_index=True, use_container_width=True)
    else:
        st.write("Click recommend button after selecting movies")