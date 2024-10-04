sudo docker build -t nielshuman/swingmachine ./
sudo docker run --volume "$(pwd)"/volume:/volume nielshuman/swingmachine