# Start from a clean, standard base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy dependency manifest first (optimization)
COPY requirements_modern.txt .

# Install dependencies (Factor 2)
RUN pip install --no-cache-dir -r requirements_modern.txt

# Copy the application code
COPY . .

# Define the default command
CMD ["python", "modern-app.py"]