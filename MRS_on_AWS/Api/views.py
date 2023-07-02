from django.shortcuts import render
import pandas as pd
import pyarrow as pa
from ast import literal_eval

movies_data = pd.read_parquet("Data/movie_database.parquet")
titles = movies_data['title']
titles_list = titles.to_list()
#genres are connverted to byte string, so we need to convert it back to a list
movies_data['converted_genres'] = movies_data['genres'].apply(lambda x: literal_eval(x.decode("utf-8")))
movies_data['converted_genres'] = movies_data['converted_genres'].apply(lambda x: [item.lower() for item in x])
model = pa.parquet.read_table('Data/model.parquet').to_pandas()


#FUNCTIONS FOR RECOMMENDATIONS
def get_recommendations(movie_id_from_db,movie_db):

    try:
        sim_scores = list(enumerate(movie_db[movie_id_from_db]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:30] ## get top 30 Recommendations
        
        movie_indices = [i[0] for i in sim_scores]
        output = movies_data.iloc[movie_indices]
        output.reset_index(inplace=True, drop=True)

        response = []
        for i in range(len(output)):
            response.append({
                'movie_title':output['title'].iloc[i],
                'movie_release_date':output['release_date'].iloc[i],
                'movie_director':output['main_director'].iloc[i],
                'runtime':output['runtime'].iloc[i],
                'google_link':"https://www.google.com/search?q=" + '+'.join(output['title'].iloc[i].strip().split()) + " (" + output['release_date'].iloc[i].split("-")[0]+")"
            })
        return response
    except Exception as e:
        print("error: ",e)
        return []

#Fetch most popular movies for a genre
def get_genre(genre):
  try:
    genre_column = 'converted_genres'
    output =  movies_data[ movies_data[genre_column].apply(lambda x: genre in x)]
    response = []
    for i in range(len(output)):
      response.append({
                'movie_title':output['title'].iloc[i],
                'movie_release_date':output['release_date'].iloc[i],
                'movie_director':output['main_director'].iloc[i],
                'runtime':output['runtime'].iloc[i],
                'google_link':"https://www.google.com/search?q=" + '+'.join(output['title'].iloc[i].strip().split()) + " (" + output['release_date'].iloc[i].split("-")[0]+")"
            })
    return response
  except Exception as e:
        print("error: ",e)
        return []  




#FUNCTIONS TO RENDER PAGES
def main(request):

    global titles_list, model

    if request.method == 'GET':
        return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':''
                }
            )

    if request.method == 'POST':

        data = request.POST
        movie_name = data.get('movie_name') ## get movie name from the frontend input field

        if movie_name in titles_list:
            idx = titles_list.index(movie_name)
        else:
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':movie_name
                }
            )

        final_recommendations = get_recommendations(idx,model)
        if final_recommendations:
            return render(
                request,
                'recommender/result.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':final_recommendations,
                    'input_movie_name':movie_name
                }
            )
        else:
            return render(
                request,
                'recommender/index.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'',
                    'recomendation_found':'',
                    'recommended_movies':[],
                    'input_movie_name':movie_name
                }
            )

def thrillers(request):
    if request.method == 'GET':
        top_movies = get_genre('thriller')
        return render(
                request,
                'recommender/thriller.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def comedy(request):
    if request.method == 'GET':
        top_movies = get_genre('comedy')
        return render(
                request,
                'recommender/comedy.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def drama(request):
    if request.method == 'GET':
        top_movies = get_genre('drama')
        return render(
                request,
                'recommender/drama.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def animated(request):
    if request.method == 'GET':
        top_movies = get_genre('animation')
        return render(
                request,
                'recommender/animated.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def romance(request):
    if request.method == 'GET':
        top_movies = get_genre('romance')
        return render(
                request,
                'recommender/romance.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def action(request):
    if request.method == 'GET':
        top_movies = get_genre('action')
        return render(
                request,
                'recommender/action.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )

def horror(request):
    if request.method == 'GET':
        top_movies = get_genre('horror')
        return render(
                request,
                'recommender/horror.html',
                {
                    'all_movie_names':titles_list,
                    'input_provided':'yes',
                    'movie_found':'yes',
                    'recomendation_found':'yes',
                    'recommended_movies':top_movies,
                    'input_movie_name':''
                }
            )