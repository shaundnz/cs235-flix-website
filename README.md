# CS235FLIX website
## Description
Web application to browse through all you favourite movies. Made using Python's Flask framework and libraries such 
as Jinja and WTForms. Design patterns and principles used include the repository pattern, dependency inversion and
single responsibility. The application uses Flask Blueprints to maintain a separation of concerns between application 
functions. Testing includes unit and end-to-end testing using the pytest tool.

## Setup
### Virtual Environment

###### Terminal:
Navigate to the directory containing website, then in the terminal, type:
```
py -3 -m venv venv
venv\Scripts\activate
```
###### PyCharm:
* Open the cloned git repository as a project.
* From here navigate to File -> Settings.
* Expand the project tab, and select 'Project Interpreter' and click the 3 dots on the right of the field showing the 
interpreter file path.
* Select 'Add' and chose to create or use an existing virtual environment

### Installing Dependencies
###### Terminal:
```
pip install -r requirements.txt
```
###### PyCharm:
Open `requirements.txt` in PyCharm, unsatisfied package requirements will be underlined and can be hovered over
to install. Alternatively, open any Python file and a notification bar will appear prompting for the install of
unsatisfied requirements. 
## Run Application
Once virtual environment has been created/activated and all dependencies has been installed, from the terminal in 
the project directory containing `wsgi.py`, start the application with:
```
flask run
```

## Configuration
The `.env` file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Testing 
Testing configuration set in `tests/conftest.py`. Test data stored in `tests/data` and is accessed via relative path
if this does not work change `TEST_DATA_PATH` to absolute path of `tests/data`. Use `os.path` when creating file paths
to ensure application is OS agonising and avoid any issues with path separators.

Run the tests from within PyCharm with a pytest configuration or from the terminal inside an activated virtual 
environment from the top level project directory (ie the directory containing `tests/`) with:
```
python -m pytest
```
######End
