FROM --platform=linux/amd64 python:3.10

RUN mkdir -p /usr/local/agent/config

COPY ./config /usr/local/agent/config

COPY main.py /usr/local/agent/

COPY agent.py /usr/local/agent/

COPY requirements.txt /usr/local/agent/

WORKDIR /usr/local/agent/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x main.py

EXPOSE 18080

ENTRYPOINT ["python", "main.py"]