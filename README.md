# Sharp Benders Academy Database

Web application to manage data for a school system. Created using Python, Flask, MySQL




## Getting started

- CD to directory on flip servers, then clone git repo
- Install python virtual environment module
```bash
pip3 install --user virtualenv
```
- Create virtual environment, then activate
```bash
python3 -m venv ./venv
```
```bash
source ./venv/bin/activate
```
- Install dependencies
```bash
pip3 install -r requirements.txt
```
- Create .env file in root directory with below credentials for database access
```text
340DBHOST=classmysql.engr.oregonstate.edu
340DBUSER=cs340_lastnamef
340DBPW=maybea4digitnumber
340DB=cs340_lastnamef
```
- Change port number on app.py
```python
if __name__ == "__main__":
    app.run(port=XXXX, debug=True)
```
- Run gunicorn (replacing XXXX with port number you chose)
```bash
gunicorn -b 0.0.0.0:XXXX -D app:app
```