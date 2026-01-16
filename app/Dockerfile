FROM python:3.14

WORKDIR /usr/src/app

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

COPY app/entrypoint.sh .
RUN chmod +x ./app/entrypoint.sh

EXPOSE 5000

# This is better than putting it in 'command' in docker-compose
ENTRYPOINT ["./entrypoint.sh"]