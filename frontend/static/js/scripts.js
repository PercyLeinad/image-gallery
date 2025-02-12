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

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

function toggleTheme() {
    const currentTheme = localStorage.getItem('theme') || document.documentElement.getAttribute('data-theme') ||  (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); // Check current theme or fallback to system preference
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
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
themeToggleBtn.addEventListener('click', toggleTheme);

applySavedTheme(); // Call only once, after setting up the event listener