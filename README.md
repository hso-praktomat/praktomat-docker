# Running Praktomat in a Docker container

```bash
docker build -t praktomat .
docker run -dp 8000:8000 praktomat
```

Open the CLI of the container and execute the following command to create a super user:
```bash
python3 Praktomat/src/manage-local.py createsuperuser
```

The application is accessible on http://localhost:8000.
