FROM ubuntu:18.04

ADD app.py app.py
ADD judge.py judge.py

RUN mkdir templates
ADD templates/ templates/
RUN mkdir static
ADD static/ static/


RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 python3-pip g++ -y
RUN pip3 install --upgrade pip
RUN pip3 install flask timeout_decorator

# EXPOSE 5000

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
CMD ["python3", "app.py"]