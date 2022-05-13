FROM python:3.7.5-slim
RUN mkdir -p /var/app/tringle
WORKDIR /var/app/tringle
COPY requirements.txt /var/app/tringle
RUN pip install --no-cache-dir -r requirements.txt
COPY . /var/app/tringle
ENV FLASK_APP ../app.py
CMD exec gunicorn -w 1 -b :5050 app:app --preload