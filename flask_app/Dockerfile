FROM python:3.11.4-alpine3.17
LABEL maintainer="sana@uni.minerva.edu"

COPY requirements.txt .

# Install required libraries for your application
RUN apk update && \
    apk add python3 postgresql-libs && \
    apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

WORKDIR /app
ADD . /app

# Update this if your app runs on a different port
EXPOSE 5000

CMD ["python", "app.py"]
