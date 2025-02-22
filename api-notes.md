# Ways of querying the api

http://localhost:8000/api/

### By default the api outputs a json file as;

{
"total": 229,
"total_pages": 12,
"per_page": 20,
"results": [
{
"id": "Caption 19",
"caption": "Caption 19",
"urls": {
"original": "/static/photos/original/Caption 19.jpg",
"thumb": "/static/photos/thumbnails/Caption 19.webp",
"hd": "/static/photos/hd/Caption 19.webp"
},
more ....
]
}

- The api is has an upper limit of 20 images per page and minimum of 1

- You can run a query to the api using per_page and page

eg.http://localhost:8000/api/?per_page=5

- will output pages=46,per_page=5
