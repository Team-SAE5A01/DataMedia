# Use the official Python 3.11 image as a base
FROM python:3.11.8

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose the port on which the app will run (for example, port 8000)
EXPOSE 8000

# Command to run the application with a binding to 0.0.0.0 (access from outside the container)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
