FROM python:3.14-slim AS build

WORKDIR /app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install build dependencies and upgrade pip
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Copy project metadata first to take advantage of Docker layer caching
COPY pyproject.toml /app/

# Install dependencies defined in pyproject.toml without installing the editable root package
RUN pip install --no-cache-dir --no-root .

# Copy the rest of the Django project to the container
COPY . /app/

# Expose the Django port
EXPOSE 8000

# Run Django’s startup scripts and server
CMD ["/app/entrypoint.sh"]