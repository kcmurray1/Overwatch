FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 5001
RUN apt-get update && apt-get install -y openssh-client

ENTRYPOINT ["./entrypoint.sh"]