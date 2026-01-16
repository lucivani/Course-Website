# CSCB20 Course Website

## Setting Up Environment
1. Open 'CSCB20' folder to access file, then open 'app.py' file.
2. Use a virtual environment to access the website, by following these command on your terminal
    - Create an environment by creating a ```.venv``` folder within
      * On macOS/Linux
      ```
      $ cd /path/to/folder
      $ python3 -m venv .venv
      ```
      * On Windows
      ```
      > cd /path/to/folder
      > py -3 -m venv .venv
      ```
    - Activate the environment
      * On macOS/Linux
      ```
      $ . .venv/bin/activate
      ```
      * On Windows
      ```
      > .venv\Scripts\activate
      ```
3. Within the activated environment, use the following command to install all of Flask packages needed
   ```
   pip install Flask
   pip install Flask-SQLAlchemy
   pip install Flask-Bcrypt
   ```
4. Run the web by typing the following command ```flask run```. If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding ```--host=0.0.0.0``` to the command line (```flask run --host=0.0.0.0```)
5. Visit that URL in your browser to view the website
6. To quit the website, type CTRL+C to command prompt

## Notifications for Environment
- Secret key in the website is distinct when it comes to different devices. The user needs to change the string of the secret key. It should be a long random bytes or str. Copy the output of command ```python -c 'import secrets; print(secrets.token_hex())'``` to your config ```app.config['SECRET_KEY'] = 'output'``` gives the secret key needed.
- The database for each data has been created with the database model in Flask and can be accessed in instance folder.
- On subscription form pages, meal type and delivery days can be chosen more than one. To choose multiple item, press ```Command (⌘)``` + Click item for macOS or ```Ctrl``` + Click item.

## Setting Up Instructors and Students Account
1. There are 2 instructors accounts have been made. The first account using username and password ```instructor1```. The second account using username and password ```instructor2 ```. User can directly login to instructors account with these credentials and can add another one by redirecting to register page.
2. There are 2 students accounts have been made. The first account using username and password ```student1```. The second account using username and password ```student2 ```. User can directly login to students account with these credentials and can add another one by redirecting to register page.
