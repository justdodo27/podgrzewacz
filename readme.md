# Quick guide for installation

1) Create virtual environment

    ```
    python -m venv venv
    ```
    On linux:
    ```
    source venv/bin/activate
    ```
    On windows (cmd):
    ```
    venv\Scripts\activate.bat
    ```
2) Install prerequisites
   ```
   pip install -r requirements.txt
   ```
3) Run flask
   > On linux and Mac
    ```
    export FLASK_APP=run.py
    export FLASK_ENV=development # optional for development mode
    flask run
    ```
   > On Windows (cmd)
   ```
    set FLASK_APP=run.py
    set FLASK_ENV=development # optional for development mode
    flask run
    ```
4) To check your application go to [localhost](http://127.0.0.1:5000/)