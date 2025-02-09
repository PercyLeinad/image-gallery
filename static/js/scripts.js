// document.addEventListener("DOMContentLoaded", function() {

//     fetch('http://127.0.0.1:8000/gallery/api/?per_page=18')
//         .then(response => response.json())
//         .then(data => {
//             data.results.forEach(element => {
//                 const main = document.getElementById('main')
//                 const itemdiv = document.createElement('div')
//                 itemdiv.classList = 'image-container'
//                 const img = document.createElement('img');
//                 img.src = element['urls'].full
//                 img.dataset.src = element['urls'].thumb
//                 img.classList = 'image'
//                 img.alt = 'Photo'
//                 itemdiv.appendChild(img)
//                 main.appendChild(itemdiv)      
//             })
//         })


// });

const imgsobserver = document.querySelectorAll('.image-container img')

const options = {
    threshold: 0.7,
    root: null
};

const observer = new IntersectionObserver(entries =>{
    entries.forEach(entry =>{
        if (entry.isIntersecting){
            const img = entry.target;
            img.src = img.dataset.src; 
            observer.unobserve(entry.target) 
        }

    });

},options);
imgsobserver.forEach(im =>{
observer.observe(im)
})


function openModal(imgSrc, fullImgSrc) {
    document.getElementById("modal").style.display = "block";
    document.body.classList.add("modal-open");
    document.getElementById("modal-img").src = imgSrc;
    document.getElementById("download-link").href = fullImgSrc;
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
    document.body.classList.remove('modal-open');
}