# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all your files into the container
COPY . .

# Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run uses port 8080 by default, so we tell Gradio to use it
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
