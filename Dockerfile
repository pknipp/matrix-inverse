FROM nikolaik/python-nodejs:python3.8-nodejs14 as base

WORKDIR /var/www
COPY . .

# Install Python Dependencies
RUN ["pip", "install", "-r", "requirements.txt"]

# Setup Flask environment
ENV FLASK_APP=matrix_inverse
ENV FLASK_ENV=production

EXPOSE 8000

# Run flask environment
CMD gunicorn matrix_inverse:app
