## Levantamos el servidor con el comando  

`fastapi dev main.py` 

## Si lo probas localmente: url + nombre del endpoint (hola)
`http://127.0.0.1:8000/hola`
Ahi te devuelve el mensaje


## Desde un google si pones:
`http://127.0.0.1:8000/payments`




Te devuelve el contenido de ese archivo


## Desde la terminar en Windows el comando es: 
`curl.exe -X GET "http://127.0.0.1:8000/files"`

`curl.exe -X 'GET' 'http://127.0.0.1:8000/files/prueba45.txt'`

`curl.exe -X 'POST' 'http://127.0.0.1:8000/files' -H 'Content-Type: application/json' -d '{"name": "test.txt", "content": "Este es un archivo de prueba"}' `

## Para crear el requirements.txt
`pip list`

`pip freeze > requirements.txt`

 ## Para la parte de render logré deployear en:
 https://apifast-m5ay.onrender.com
