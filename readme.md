```
git clone https://gitlab.light-it.tools/nazymok.dmitriy/social_app.git
cd social_app
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
Create .env file. Example you can find in same directory (.env-example)
``` 
python manage.py migrate
python manage.py runserver
```
