# Requirements  

1. Install [Python 3.10](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)

```
apt update && sudo apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt install python3.10
```


2. Install [Pip 23.2.1](https://phoenixnap.com/kb/how-to-install-pip-on-ubuntu) for Python 3.10
```
sudo apt update
sudo apt install python3-pip
pip3 --version
```

4. Install virtualenv for Python3.10:
```
sudo apt install python3.10-venv -y
```
5. Install [PostgreSQL](https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04)
```
sudo apt install postgresql -y
```

# Configure the environment variables

```
cp .env.sample .env
```
Modify `.env` variable values to desired values.




# Configure PostgreSQL

```
sudo -u postgres psql -c "create database traffic_data"
sudo -u postgres psql -c "create user traffic_data_user"
sudo -u postgres psql -c "alter user traffic_data_user with encrypted password '1234'"
sudo -u postgres psql -c "alter user traffic_data_user CREATEDB"
sudo -u postgres psql -c "grant all privileges on database traffic_data to traffic_data_user"
```


# Initializing Python Virtual Environment
Hoping you are in the project directory
```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run the Migrations
```
python manage.py migrate
```

# Load the different cities sensors data in DB
A django command that will load different cities sensors data in DB. We just have to pass the city name as param of command.

```
python manage.py load_sensor_data --city="Lahore"
python manage.py load_sensor_data --city="Sydney"
python manage.py load_sensor_data --city="San Francisco"

```

# Change a specific sensor location
In-case you want to change the location of a specific sensor, you can call the below command with device name as param.

```
python manage.py change_sensor_location --vehicle_name="Lahore_vehicle_1"

```

# Run the Server
```
python manage.py runserver
```
