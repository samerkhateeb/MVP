# Welcome to MVP Project
it is me Samer, i am working as a FullStack developer, and i've developed this application using ReactJs-Context for the Frontend and Django-Postgresql for the Backend and containarize them with Docker.

```
This guide is for Mac Users
```



## Run the Backend

<img width="903" alt="image" src="https://user-images.githubusercontent.com/55295850/214182207-d8c8bd2d-d03b-486c-8783-3d4bb64a9de7.png">

To run the backend, you should have at least docker installed in your machine in the url: http://localhost:8000/admin , then navigate to the backend folder `server\mvp-docker`, and type the following commands:
1. Build the web:
```
docker compose build web
```
2. Assign the database
```
docker compose up -d database_default
```
3. Migrate the database
```
docker compose run web python manage.py migrate
```
4. create the super user
```
docker compose run web python manage.py createsuperuser
```
5. let the container waming up :)
```
docker compose up -d
```

** NOTE: ** you have to to stop postgresql in. your machine if it was installed, you can stop it by the following command: 
```
sudo -u postgres pg_ctl -D/Library/PostgreSQL/12/data stop
```

## Run The Fronend

After you clone the repository in your machine, go to the directory `client\mvp-reactjs-context`, then you have to install the packages using `yarn`, then after the packages are successfully installed, please type `yarn start`, this will activate the environment in your local machine in the URL:
http://localhost:3000/

<img width="764" alt="image" src="https://user-images.githubusercontent.com/55295850/214182445-eed661bd-e43b-434c-8f5a-1d632d7dec0c.png">


## Django Test Cases:


you can run the Test cases for Product CRUD, deposite as well as buy products API's, the test contains 14 test case for 7 API's,  you have to go go to the server folder `cd server` and run the following command on it:
```
docker compose run web python manage.py test
```
The result will be Ran 14 tests in 5.278s

OK !!!!

<img width="1525" alt="image" src="https://user-images.githubusercontent.com/55295850/214631898-4d145823-e1c1-4af6-897f-6195418e1b41.png">


:tada::tada: Super :tada::tada:

## Postman:
you can refer the file includes [Postman Collections](https://github.com/samerkhateeb/MVP/blob/master/MVP.postman_collection.json), it includes 10 methods to test the API's one by one, i put also test values on it, you can change it and try to send requests in your local machine.

<img width="1336" alt="image" src="https://user-images.githubusercontent.com/55295850/214180178-5eddf8c5-ff55-4e5c-aa0f-f30ec6039883.png">


:tada: Congratulations! You have launched the application successfully !! please refer to me for any concern related to the technical details :tada:

Thanks and Have a Good DAY :) ...
