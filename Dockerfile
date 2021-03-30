FROM python:3

COPY . /api

WORKDIR /api

RUN pip install firebase_admin

RUN pip install flask_restplus

RUN pip install flask

RUN pip install werkzeug

RUN pip install pandas

RUN pip install pytest

RUN pip install pytest-cov

RUN pip install authorizenet

RUN pip install requests[security]

RUN pip install -U flask-cors

RUN pip install python-dotenv

RUN openssl enc -aes-256-cbc -d -in serviceAccountDocker.json.enc -out serviceAccount.json -k mcmasterpw

RUN openssl enc -aes-256-cbc -d -in .env.enc -out .env -k PASS

EXPOSE 5001

CMD ["python", "-u", "app.py"]