
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const imageUrl = params.get("image");
    
    if (imageUrl) {
        const itemdiv = document.getElementById('item');
        const imgtag = document.createElement('img');
        imgtag.classList.add('image');
        imgtag.src = imageUrl;
        imgtag.alt = 'Photo';
        itemdiv.appendChild(imgtag);
        document.getElementById("download-link").href = imageUrl;
    }
});
