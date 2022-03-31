FROM python:3-slim

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD script.py .
COPY rightmove_scraper/ ./rightmove_scraper

CMD [ "python", "script.py" ]
