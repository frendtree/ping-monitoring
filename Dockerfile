FROM python:3.10
ADD ./src /src
WORKDIR /src
RUN pip install pings && \
    pip install pytz
CMD [ "python", "app.py" ]
