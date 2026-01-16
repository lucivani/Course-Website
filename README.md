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
   pip install Flask-WTF
   ```
4. Run the web by typing the following command ```flask run```. If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding ```--host=0.0.0.0``` to the command line (```flask run --host=0.0.0.0```)
5. Visit that URL in your browser to view the website
6. To quit the website, type CTRL+C to command prompt
