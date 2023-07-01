FROM python:3-alpine
 
# Create app directory
WORKDIR /app
 
# Install app dependencies
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
# Bundle app source
COPY . .
 
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:app"]
