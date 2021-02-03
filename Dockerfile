FROM python:3

COPY . /api

WORKDIR /api

RUN pip install firebase_admin

RUN pip install flask_restplus

RUN pip install flask

RUN pip install werkzeug

RUN pip install pandas

RUN pip install pytest

EXPOSE 5001

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]