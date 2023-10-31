# Use the official Python 3.11 image as a base image
FROM python:3.11-slim-buster

# Set the environment variable PYTHONUNBUFFERED to ensure that Python output is logged
ENV PYTHONUNBUFFERED 1

# Set the FLASK_ENV environment variable to development to enable debug mode
ENV FLASK_ENV=development

# Set the FLASK_APP environment variable to tell Flask which app to run
ENV FLASK_APP=app.web

# Set the working directory in the Docker container
WORKDIR /pdf-chat-bot-app

# Copy the local project directory (all files) into the container
COPY . .

# Install the Python packages specified in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the Flask app
EXPOSE 8000

# Run the Flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]
