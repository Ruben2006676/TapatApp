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

Descripció: Ens diu si existeix un usuari segons el nom i l'email que li pasem.

HOST: Domain port: 192.168.144.140

End-point (URL): 192.168.144.140:10050/tapatapp/getuser

Method: GET

Tipus de petició (headers): Accept: application/json
Content-Type: application/json

Parametres que necessita la petició: (identifica els paràmetres i posa exemples en el cas de peticions GET):
Es necessita l'ID, l'username, el password i el email.

Exemple: GET http://192.168.144.140:10050/tapatapp/getuser?name=rla8436&email=proven@email.cat


Resposta: 

Exitosa: 

{
  "message": "Hello World: Nom:rla8436 :email = proven@email.cat"
}


Errònia: 

{
  "error": "Usuari no trobat"
}

