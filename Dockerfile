FROM python:3.11.5

RUN useradd -m app
WORKDIR /home/app
ENV PATH="/home/app/.local/bin:$PATH"
USER app

COPY Pipfile .
COPY Pipfile.lock .
COPY scrape-chase-activity.py .
COPY scrape scrape

RUN pip install --user pipenv; \
  pipenv sync

ENTRYPOINT ["pipenv", "run", "python3", "scrape-chase-activity.py"]
