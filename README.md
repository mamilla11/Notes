# Notes
This is a Flask application that allows you to manage your notes and view other people's notes

- To get access to all notes you have to be registered and logged in to the service
- You can create, update and delete notes
- You can not update or delete other users notes
- If you are an admin, you also can view all users and roles

At the start the default admin user is added with the following credentials:
- email: admin@mail.com
- password: qwerty

### Run

To start the app execute the following command from a root directory:

```bash
docker-compose up -d
```
Now REST API documentation is available at http://localhost:5000/api/v1/ui

### Test

To execute tests, navigate to `./tests` directory and execute the following command:

```bash
docker-compose -f docker-compose.test.yml up -d
```

This command starts 3 containers:
- `postgres` - ProsrgreSQL database
- `tests_app` - Flask App
- `tests_tests` - Tests

Go into `tests_tests` container:
```bash
docker exec -it <CONTAINER ID> /bin/ash
```

Execute tests:

```bash
pytest -v -s
```