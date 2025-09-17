# Intersector App Built in Python

This branch hosts an OOP design of this software.

```
Intersector
.
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── src
    ├── app.py
    ├── config.py
    ├── Core
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── exceptions.py
    │   ├── models.py
    │   ├── Tests
    │   └── two_collection_intersector.py
    └── Tests
        └── test_app.py
```

## To run the app

First clone the git repository

```
git clone git@github.com:shirzartenwer/Intersector.git
cd OptravisHomework
```

### first option

Then to run the app, they easiest option is to 
```
docker compose up
```
### second option
If you have VScode, then do:

```
code .
```

Then `ctrl/cmd + shift + P` and open this repo in `devcontainer`. 
Then do 
```
streamlit run src/app.py
``` 
to run the app. 



## Run tests and see test coverage
Open this code repo in `devcontainer` in VScode. Then run 
```
pytest
```

To see the test coverage run: 

```
pytest --cov=src 
```
