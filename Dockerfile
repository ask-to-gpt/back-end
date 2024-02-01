FROM python:3.11

WORKDIR /app/src

# 타임존 설정
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezoneRUN 

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
