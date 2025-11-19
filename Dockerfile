FROM python:3.11

LABEL authors="玖渚智心"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 3001

CMD ["python", "main.py"]