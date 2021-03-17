FROM python:3.7
RUN mkdir -p /tmp
RUN chmod 0755 /tmp
COPY . /tmp/

WORKDIR /tmp
RUN pip install -U pip
RUN pip install -r  requirements.txt
EXPOSE PORT
RUN ls -l -a
ENTRYPOINT ["python"]
CMD ["runserver.py"]
