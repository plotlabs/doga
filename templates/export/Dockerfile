FROM python:3.7
COPY . /tmp/
RUN pip install -U pip
RUN pip install -r  /tmp/requirements.txt
EXPOSE PORT
CMD ["python", "-u",  "/tmp/runserver.py"]
