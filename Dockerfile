# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y libsndfile1

# Install pip requirements
COPY app/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY app /app

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
