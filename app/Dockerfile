FROM alpine
RUN mkdir /app 
RUN apk add --no-cache python3 py3-pip; pip3 install flask psycopg2-binary python-dotenv --break-system-packages
WORKDIR /app
COPY data/* .
RUN mkdir templates;mv index.html templates/.
EXPOSE 5000
CMD ["python", "app.py"]
