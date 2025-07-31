## setup
- `python -m venv .venv`
- `.venv/bin/activate`
- `pip install -r requirements.txt`

## run

- `flask --app app run`


## test
- `python -m pytest`
  - https://flask.palletsprojects.com/en/stable/testing/
- /users
  - `curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "age": 30, "nickname": "Johnny"}' http://127.0.0.1:5000/users`