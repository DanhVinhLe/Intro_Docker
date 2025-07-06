# Introduction to Docker, FastAPI

## Setup
Follow the steps below to set up and run the project:

1. Clone repo
```bash
git clone https://github.com/DanhVinhLe/Intro_Docker.git
```
2. Navigate to the project directory
```bash
cd Intro_Docker
```
3. Build Docker Image
```bash
docker build -t stable-diffusion-api .
```
4. Run the container (make sure your system has a GPU):
```bash
docker run --gpus all -p 8000:8000 stable-diffusion-api
```
Test API at link [http://localhost:8000/docs](http://localhost:8000/docs)

