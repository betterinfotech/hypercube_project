# Use the official lightweight Python 3.12 base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies from requirements.txt
# --no-cache-dir keeps the image smaller by not caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Default command: run the ETL pipeline
CMD ["python", "run.py"]
