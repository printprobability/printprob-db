FROM python:3.9.12
RUN mkdir -p /vol/app
WORKDIR /vol/app
ADD ../requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt
EXPOSE 8000
