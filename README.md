# Welcome to the pandemic-model repository!

## 1. Install Dependencies

### Front-end dependencies
- Node (download LTS): https://nodejs.org/en/ (this download should also includes npm)

Check that you have both node and npm installed. In your terminal run:
```
node -v
npm -v
````

### Back-end dependencies
- Python (must be above v3): https://www.python.org/downloads/

To check your Python version, run:
```
python --version
````

Inside a terminal, run:
```
pip install Flask
pip install Flask-Cors
pip install pandas
pip install numpy
pip3 install pymysql
pip3 install sqlalchemy
````

### Clone this repository
Inside your terminal:
```
git clone https://github.com/daniellou2000/pandemicModel.git
````

If you don't have git installed: 
- Download from: https://git-scm.com/downloads

To check that git is installed, you should see a version when you run:
```
git --version
````


## 2. Run the code

### Front end - React app
Navigate to the cloned repository, and cd into the `client` directory. Then run:
- npm install
- npm start

And you should see the application running on http://localhost:3000/. You only need to run `npm install` the first time you download the repository, or anytime there are new changees. 

### Back end - Python Flask server
Open another terminal tab. Navigate to the `backend` directory in your terminal. 

Follow the instructions here for starting up the application: https://flask.palletsprojects.com/en/2.0.x/quickstart/. If you didn't read it, below is the command for using a powershell terminal. If using other terminals, check the website for your specific commands. 
```
$env:FLASK_APP = "server"
python -m flask run

Now both the front end and back end should be running, and you can access the app at http://localhost:3000/. 
