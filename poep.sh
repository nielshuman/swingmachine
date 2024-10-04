sudo docker build -t swingmachine ./
sudo docker run --volume "$(pwd)"/volume:/volume swingmachine