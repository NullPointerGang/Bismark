FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "run.py"]
