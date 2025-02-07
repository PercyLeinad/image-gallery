const imgsobserver = document.querySelectorAll('.lazyload')

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
    document.getElementById("modal-img").src = imgSrc;
    document.getElementById("download-link").href = fullImgSrc;
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}