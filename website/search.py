import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search(anime):

    df = pd.read_csv('anime2.csv')


    df = df.reset_index()
    df = df.drop('index',axis=1)



    df['Name'] = df['Name'].str.lower()
    df['Genres'] = df['Genres'].str.lower()

    df = df[['ID','Name', 'Score','Genres','Aired']]

    df['ID'] = df[df.columns[1:]].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1
 )



    vectorizer = CountVectorizer()
    vectorized = vectorizer.fit_transform(df['ID'])



    similarites = cosine_similarity(vectorized)

    df = pd.DataFrame(similarites, columns=df['Name'], index=df['Name']).reset_index()

    input_name = anime
    reccomendations = pd.DataFrame(df.nlargest(10,input_name)['Name'])
    reccomendations = reccomendations[reccomendations['Name']!= input_name]
    suggestions = reccomendations.to_numpy()
    shows =[]
    for i in suggestions:
        for j in i:
            shows.append([j][0])
    
    print(shows)
           
    

    return(shows)

search("nana")









