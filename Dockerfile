# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container at /app
COPY requirements.txt .

# 4. Install uv (optional, but faster) and then dependencies
# If you don't have/want uv, you can replace this with:
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir --system -r requirements.txt

# 5. Copy the rest of the application code into the container at /app
COPY app_streamlit.py .
COPY simulator.py .

# 6. Make port 8501 available to the world outside this container
EXPOSE 8501

# 7. Define environment variable for Streamlit configuration (optional but good practice)
# Tells Streamlit it's running headlessly, suitable for containers/servers
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 8. Run streamlit when the container launches
# Use CMD so it can be easily overridden if needed
CMD ["streamlit", "run", "app_streamlit.py"] 