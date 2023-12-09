# Start of league stat platform.
The goal isn't to compete with any of the established platforms. I plan on adding League of Legends support to [Carnival](https://github.com/zkxjzmswkwl/Carnival), and this platform aims to supplement that.

# Run
```
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Admin panel
Django ships with an admin panel out of the box. To create a superuser account, run `python manage.py createsuperuser` and follow the prompts. Once done, you can login at `localhost:8000/admin`

### Why not use one of the already-made LoL API libs?
Go use one. I want to see you suffer.