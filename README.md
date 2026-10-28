# Lab 7 Python testing

This project uses the `lab5_api` package from the Lab 5 project. `test_user_Khaled_Kanawati.py` checks database startup, the five database operations, and the four required API methods. The API tests check status codes and returned JSON. Each test uses a temporary database, so the tests do not change the app database.

The app creates the users table and two sample users when a new database is first created. Starting the app again keeps the existing records.

The capitalization, wallet, and `/add` examples from the handout are included as separate files.

Install dependencies with `python -m pip install -r requirements.txt`, then run `python -m pytest` from this folder. Run the API with `python -m lab5_api.app`.
