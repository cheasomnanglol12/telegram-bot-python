# Dockerfile

# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /app/

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Set environment variables (for production)
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Expose the port (if applicable, for HTTP-based bots)
# EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
