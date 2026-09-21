FROM python:3.10-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers python3-dev
COPY requirements.txt ./
ENV ENVIROMENT=Devops-Lab
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD  ["python", "app.py"]



