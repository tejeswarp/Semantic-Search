# Use an official lightweight Python image
FROM python:3.11-slim

USER root
# Set the working directory in the container
WORKDIR /Semantic-Search

COPY ./dist/Semantic-Search* .

RUN unzip Semantic-Search*.zip
RUN mv */* .
RUN rm -rf Semantic-Search*.zip
RUN rm -rf Semantic-Search*

ENV http_proxy=''
ENV https_proxy=''

# Expose the application port
EXPOSE 8080

ENV VIRTUAL_ENV=/home/appusr/Semantic-Search/env

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# install dependencies

RUN pip3 install --no-cache-dir -r ./requirements.txt

WORKDIR /Semantic-Search/src

# Run the application
ENTRYPOINT ["sh", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port 8080"]
