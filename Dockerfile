# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        libproj-dev \
        gdal-bin \
        postgis \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /code/

# Copy the entrypoint script into the container
COPY entrypoint.sh /code/entrypoint.sh

# Give execute permission to the entrypoint script
RUN chmod +x /code/entrypoint.sh

# Port to expose
EXPOSE 8000

# Command to run the entrypoint script
ENTRYPOINT ["/code/entrypoint.sh"]


# # Port to expose
# EXPOSE 8000

# # Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
