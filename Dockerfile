FROM python:3
ADD server.py /
EXPOSE 8000
CMD python server.py