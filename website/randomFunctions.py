from jikanpy import Jikan

jikan = Jikan()

global animeName
anime  = jikan.random(type='anime')
def randomAnime():
    names = anime["data"]["titles"]
    names = names[0]["title"]
    return(names)


def animeImage():
    img = anime["data"]["images"]["jpg"]["large_image_url"]
    return(img)



def animeSynopsis():
    synopsis = anime["data"]["synopsis"]
    return(synopsis)






"""print(names)
print(names[0]['title'])"""
