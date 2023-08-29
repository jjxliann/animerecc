function deleteAnime(animeId){
    fetch('/delete-anime',{
        method:'POST',
        body:JSON.stringify({animeId: animeId})
    }).then((_res)=>{
        window.location.href ="/";
    });
}