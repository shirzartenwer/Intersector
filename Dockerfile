FROM python:3.9-slim

# Create vscode user and group
RUN groupadd --gid 1000 vscode && \
    useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ ./src/

# Use vscode user by default
USER vscode

# Command to run the application
CMD ["streamlit", "run", "./src/app.py"]

