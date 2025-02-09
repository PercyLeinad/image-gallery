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


function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDarkScheme ? 'dark' : 'light');
    }
}


const themeToggleBtn = document.getElementById('theme-toggle');

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
}

themeToggleBtn.addEventListener('click', toggleTheme);

// Apply the saved theme on initial load
applySavedTheme();