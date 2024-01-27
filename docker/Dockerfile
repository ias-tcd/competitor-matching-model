FROM python:3.11.7-alpine

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../requirements.txt /src/

RUN pip install -r requirements.txt

COPY .. /src/

# Sample command that should be changed once we add the application
CMD ["python", "main.py"]
