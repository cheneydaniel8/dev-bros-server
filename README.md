# dev-bros-server


API endpoints:

GET
- Get list  (domain/api/get_entries)
- Get single item from list (domain/api/get_entry/{id})

POST
- Add to single entry to list (domain/api/add_entry)

DELETE
- Delete single item from list (domain/api/delete_entry/{id})
- Delete all (domain/api/delete_all)


Running Docker Container:
`docker build -t dev-bros-server .`
`docker run -p 8000:8000 dev-bros-server`
