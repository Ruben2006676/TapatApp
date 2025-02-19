# TapatApp

Hola Mundo!!

## Descripción del proyecto

[Descripción del proyecto](DeskTop.md)

## Requeriments tècnics

[Requeriments tècnics](req.tècnics.md)

## Prototip 1

[Prototip 1](diagramaprototip1.mermaid)

## Model E-R

[Model E-R](Model_E-R.PNG)

## Http Request

[Http Request](Http_Request.md)

## Http Response

[Http Response](Http_Response.md)

## Definició dels EndPoints del Servei Web:

Què necessitem per cada End-point

Descripció: Obtenir dades de l'usuari

HOST: Domain port: 192.168.144.140

End-point (URL): 192.168.144.140:10050/tapatapp/getuser

Method: GET

Tipus de petició (headers): Accept: application/json
Content-Type: application/json

Parametres que necessita la petició: (identifica els paràmetres i posa exemples en el cas de peticions GET):
Es necessita l'ID, l'username, el password i el email.

Exemple: GET http://192.168.144.140:10050/tapatapp/getuser?name=rla8436&email=proven@email.cat


Resposta: 

Exitosa: (Amb Json)

Code Response Http: 200

{
    "id": 2,
    "username": "usuari2",
    "email": "usuari2@gmail.com",
    "password": "123"
}


Errònia: 

Code Response Http: 404

//Cas en que no es trobi l'usuari o no s'hagi introduit algun paràmetre.

{"error": "Usuari no trobat"  }

Code Response Http: 400

{"error": "Paràmetre no introduit"}

Code Response Http : 500

{"description": "Server Error"}


## Diagrames de Classes Prototip 1





