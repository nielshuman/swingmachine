FROM python:2.7.18-buster

# Install FFMPEG
RUN apt-get update && apt-get install -y ffmpeg lame soundstretch shntool && rm -rf /var/lib/apt/lists/*

# Install remix dependencies
RUN python -m pip install numpy mutagen pyyaml
RUN ln -s $(which ffmpeg) /usr/local/bin/en-ffmpeg

# Install remix
RUN git clone https://github.com/echonest/remix.git \
    && cd remix \
    && git clone https://github.com/echonest/pyechonest pyechonest 
RUN cd remix && python setup.py install \
    && cd ..
    # && rm -rf remix/

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "main.py"]
# WORKDIR /
# CMD ["python", "remix/examples/swinger/swinger.py"]