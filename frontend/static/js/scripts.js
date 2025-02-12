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

function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDarkScheme ? 'dark' : 'light');
    }
}
applySavedTheme()

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