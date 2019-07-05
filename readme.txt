# Setting up the exercise converter behind an nginx server.

# Create a virtual environment

```
sudo apt install python3-venv
python3 -m venv env
```


# Activate the virtual environment

```
source env/bin/activate
```


# Install requirements


```
pip install -r requirements.txt
```

# Run program

```
gunicorn web_converter:app --log-file - -b 0.0.0.0:8000
```

# Set up on a suburl using nginx

Adjust the file `/etc/nginx/sites-available/example` to it also contains the following location rule.
```
    # Forward traffic to the gunicorn server, which is hosting the math-exercise-converter site.
    location /convert/ {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /convert;

    }
```


# Set up the system to run as a systemd service

Create a file specifying the properties of the service.
```
sudo vi /etc/systemd/system/MathExerciseConverter.service
```

The content of the file should be as follows.
```
[Unit]
Description=Gunicorn instance to serve the MathExerciseConverter application.
After=network.target


[Service]
User=hemi
Group=www-data
WorkingDirectory=/home/hemi/documents/math-exercise-webconverter
Environment="PATH=/home/hemi/documents/math-exercise-webconverter/env/bin"
ExecStart=/home/hemi/documents/math-exercise-webconverter/env/bin/gunicorn web_converter:app -b 0.0.0.0:8000 --log-level=DEBUG --log-file logfile.txt --capture-output


[Install]
WantedBy=multi-user.target
```

Enabled the service to launch on boot
```
sudo systemctl enable MathExerciseConverter.service
```
