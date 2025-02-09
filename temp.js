fetch('http://localhost:8000/gallery/api/')
    .then(response => response.json())
    .then(data => {
        data.results.forEach(element => {
            console.log(element.id)
            console.log(element['urls'].full)
            console.log(element['urls'].thumb)
            
        });
    });