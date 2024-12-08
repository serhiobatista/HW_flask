Метод get /send/{currency} позволяет получить текущий курс биткойна. В поле currency нужно указать, какая конкретно нужна валюта: либо доллар (USD), либо евро (EUR).
Метод /data возвращает из базы данных последний актуальный курс биткойна.


1. docker-compose up -d
2. python serve.py
3. faststream run rabbit.subscriber:app
4. curl -X 'GET' 'http://localhost:5000/bitcoin/send/USD' -H 'accept: application/json'
5. curl -X 'GET' 'http://localhost:5000/bitcoin/data'
