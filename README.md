# Annotation Platform
## Getting Started

### Dependencies

* Requires Django 4.0, and Vue 3 in order to run both the backend server, and frontend UI
* Requires Pinia for Vue State Storage
* Uses Django's built-in SQL database for data storage

### Installing and Execution
##### Frontend (Vue)
Installing all packages. Navigate into the "frontend" and "label-app" folder. Make sure the package.json file is present.
```
npm install
```
Execution. Before attempting the below command, navigate into the "label-app" folder.
```
npm run serve
```
##### Backend (Django)
Installation. Navigate into the "backend" folder.
```
pip install -r requirements.txt
python manage.py migrate
```
Execution
Default execution uses localhost at a port of 8000. Changing the port here will require modification to the configuration settings.py file of the Django project folder.  Before attempting the below command, navigate into the "temporal_backend" folder.
```
python manage.py runserver 8000
```
