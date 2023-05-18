## Steps to install dependencies in a virtual environment

1. Clone this repository to local computer

2. Rename the directory to reflect the new project name

3. Create a new virtual environment

   - Windows: `python -m venv ./venv`
   - Mac: `python3 -m venv ./venv`

4. Activate the new virtual environment

   - Windows: `.\venv\Scripts\activate`
   - Mac: `source ./venv/bin/activate`

5. Install the dependencies `pip install -r requirements.txt`

6. Install node modules `npm install`

   -Or this: `command line npm install -g npm`

## Best practices to maintain dependencies

- After adding a new python dependency run the freeze script at the .\ProfileUserEngine level to update the requirements.txt

      pip freeze > requirements.txt

- Run python files at the root level to avoid installing multiple `.venv` folders
  Example to run app.py:
  `C:Users\user\Sequoia\ProfileUserEngine> python .\backend\app.py`

## Run the repo

- Select start.bat file in Windows explorer
- Alternatively run python .\backend\app.py

## Test the repo

- Use `**repr**' to return variables for every class - EXTREMELY helpful for testing
