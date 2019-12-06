FROM python:3.7.5
RUN mkdir -p /vol/app
WORKDIR /vol/app
ADD app/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
EXPOSE 8000