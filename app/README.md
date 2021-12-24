# DB

Restart in Ubuntu:
```commandline
sudo service postgresql restart
```

Create a user:
```commandline
export PYTHONPATH=$(pwd) # from inside sensorserver/app
python app/management/user.py --help
python app/management/device.py --help
python app/management/user.py --is-active --is-superuser --is-verified test@test.com test
```

```commandline
alembic revision --autogenerate -m "baseline"
alembic upgrade head
```

Create DB:
```commandline
sudo su - postgres
CREATE USER dev SUPERUSER;
ALTER USER dev WITH PASSWORD 'dev';
CREATE DATABASE sensor_server_dev WITH OWNER dev;
```

```commandline
poetry export -o requirements.txt
export PYTHONPATH=$(pwd)
```