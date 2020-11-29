FROM python:3-onbuild

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /usr/src/login/requirements.txt

WORKDIR /usr/src/login

RUN pip install -r requirements.txt

COPY . /usr/src/login

CMD ["python", "app.py"]