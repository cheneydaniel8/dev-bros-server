FROM python:3
ADD server.py /
RUN pip install requests
EXPOSE 8000
CMD python server.py