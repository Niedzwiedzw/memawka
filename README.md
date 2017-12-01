# Memawka

Memawka backend + frontend

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing backend

0. Clone this project and go into project directory
1. Create and activate a fresh virtualenv
```bash
python3.6 -m virtualenv .venv_memawka

```

2. Get the required python modules
```
pip install -r requirements.txt
```
3. `python manage.py migrate`
4. `python manage.py runserver`
## Installing frontend

0. Navigate into `memawka/clientapp/memawka-client`
1. run
 ```npm install```
 this will get the required javascript modules
3. To run the project 
```
npm run dev
```