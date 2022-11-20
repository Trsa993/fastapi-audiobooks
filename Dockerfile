FROM python:3.9.15


WORKDIR /usr/src/app


COPY requirements.txt ./

# installing dependancies for pyaudio
RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y

RUN pip install --no-cache-dir -r requirements.txt


COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]