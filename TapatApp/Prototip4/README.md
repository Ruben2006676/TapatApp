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

[Diagrama Backend P1](./BackendP1/BackEnd.mermaid)

[Diagrama Frontend P1](./FrontendP1/FrontEnd.mermaid)

## Implementació Python Backend i Frontend P1

[Backend P1](./BackendP1/Backend.py)

[Frontend P1](./FrontendP1/FrontEnd.py)

# PROTOTIP 2 

## WIREFRAMES

[Wireframes](./Wireframes/Wireframes.mermaid)

Inici:

Atributs: Pantalla de benvinguda, probablement amb un missatge introductori i opcions de navegació cap al login o registre.

Login:

Atributs:
Camps per introduir usuari i contrasenya.

Opcions per accedir al registre o recuperar la contrasenya.
Registre:

Atributs:

Camps per introduir nom, cognom, email, i contrasenya.

Opció per crear un nou compte d'usuari.

Recuperar Contrasenya:

Atributs:

Camp per introduir email i codi de recuperació.

Opció per recuperar la contrasenya en cas d'oblidar-se'n.

Usuari:

Atributs:

Nom, cognom i email de l'usuari.

Opcions per gestionar i editar la informació personal de l'usuari.

Es mostra la llista de nens associats al perfil de l'usuari.

Veure Perfil:

Atributs:

Mostra la informació de l'usuari: nom, cognom, email i altres dades addicionals.

Opcions per editar o afegir més informació, o gestionar els nens associats al perfil.

Informació Nen:

Atributs:

Nom, edat i data de naixement del nen.

Informació mèdica del nen (possiblement al·lèrgies, condicions prèvies, etc.).

Historial del Tapat:

Atributs:

Mostra l'historial del nen amb:

Data i hora de cada registre.

Estat de cada intervenció.

Total d'hores dedicades o temps transcorregut.

Llista de Nens:

Atributs:

Mostra una llista dels nens associats al perfil de l'usuari.

Informació bàsica de cada nen, com nom, edat i data de naixement.

Afegir Nen:

Atributs:

Permet a l'usuari afegir un nou nen al perfil.

Camps per introduir nom, edat i data de naixement.

## Descripció del Prototip 2 (Descripció de que volem implementar al prototip 2)

El Prototip 2 es basa en la creació d'una plataforma senzilla i intuïtiva per a la gestió d'usuaris i nens, pensada per a facilitar el registre, la gestió del perfil d'usuari i la informació dels nens, així com la possibilitat de visualitzar històrics d'intervencions o seguiment de la salut dels nens. A continuació es detallen les funcions clau que es volen implementar, basant-se en els wireframes creats.

### Pantalla de Benvinguda (Inici)
Objectiu: Aquesta pantalla donarà la benvinguda als usuaris i els oferirà les opcions de login o registre.

Funcionalitat: Un cop l'usuari obre l'aplicació, serà rebut per una pantalla inicial amb un missatge de benvinguda i dues opcions clares: iniciar sessió si ja té un compte o crear-ne un de nou.

### Pantalla de Login

Objectiu: Permetre que els usuaris accedeixin a la seva compte personal mitjançant usuari i contrasenya.

Funcionalitat: Els usuaris hauran de proporcionar les seves credencials per entrar al sistema. A més, es proporcionaran enllaços per a poder recuperar la contrasenya o accedir al registre si no tenen compte.

### Pantalla de Registre

Objectiu: Facilitar la creació d'un compte nou per a l'usuari amb els camps bàsics necessaris.

Funcionalitat: Els nous usuaris hauran d'emplenar camps amb el seu nom, cognom, email i contrasenya per crear un compte. Un cop completat el registre, l'usuari accedirà al seu perfil personal.

### Pantalla de Recuperació de Contrasenya

Objectiu: Permetre als usuaris recuperar la seva contrasenya en cas que l'hagin oblidat.

Funcionalitat: Els usuaris hauran d'introduir el seu email i un codi de recuperació enviat prèviament per correu electrònic per poder restablir la seva contrasenya.

### Pantalla d'Usuari

Objectiu: Mostrar la informació personal de l'usuari i la llista de nens associats al seu compte.

Funcionalitat: Els usuaris podran veure i editar les seves dades personals (nom, cognom, email) i consultar la llista de nens associats a ells. També hi haurà opcions per modificar o actualitzar la seva informació.

### Pantalla de Veure Perfil

Objectiu: Mostrar més detalladament les dades del perfil de l'usuari.

Funcionalitat: Els usuaris podran veure la seva informació personal detallada (nom, cognom, email) i editar o afegir més dades, com la informació de contacte o preferències. També es podrà gestionar la relació amb els nens (afegir nous nens, editar els existents).

### Pantalla d'Informació Nen
Objectiu: Permetre als usuaris veure i gestionar la informació dels nens.

Funcionalitat: Els usuaris podran consultar i editar les dades bàsiques de cada nen, com nom, edat, data de naixement i informació mèdica. Aquesta funcionalitat és important per mantenir actualitzada la informació dels nens i facilitar la gestió dels seus seguiments o historial.

### Pantalla d'Historial del Tapat

Objectiu: Mostrar l'historial de seguiment de cada nen.

Funcionalitat: Es mostrarà un registre de totes les intervencions, amb informació sobre la data, hora, estat de cada tasca realitzada i total d'hores dedicades a cada nen. Aquesta funció permet a l'usuari tenir un registre clar i detallat de les activitats realitzades.

### Pantalla de Llista de Nens

Objectiu: Mostrar tots els nens associats al compte de l'usuari.

Funcionalitat: Els usuaris podran veure una llista amb els noms, edats i dates de naixement dels nens associats al seu perfil. Aquesta vista permetrà accedir fàcilment a cada nen per veure’n més informació o modificar les dades si cal.

### Pantalla d'Afegir Nen

Objectiu: Permetre als usuaris afegir un nou nen a la seva llista de nens.

Funcionalitat: Els usuaris podran afegir un nou nen a través d'un formulari on hauran de proporcionar el nom, edat i data de naixement. Aquesta funcionalitat facilitarà l'actualització de la llista de nens associats a cada usuari.

## Diagrames de Classes Prototip 2

[Diagrama Backend P2](./Prototip2/Backend/BackendP2.mermaid)

[Diagrama Frontend P2](./Prototip2/Frontend/FrontendP2.mermaid)

## Implementació Python Backend i Frontend P2

[Backend P2](./Prototip2/Backend/BackendP2.py)

[Frontend P2](./Prototip2/Frontend/FrontendP2.py)

## Descripció prototip

[Descripció Prototip2](./Prototip2/Descripció%20de%20que%20volem%20implementar%20al%20prototip%202.md)

## Diagrames arquitectura-Backend i Frontend

[Diagrama arquitectura Backend P2](./Prototip2/Backend/BackendP2Arquitectura.mermaid)

[Diagrama arquitectura Frontend P2](./Prototip2/Frontend/FrontendP2Arquitectura.mermaid)

## Implementació Python Backend i Frontend P3

[Backend P3](./Prototip3/BackendP3/BackendP3.py)

[Frontend P3](./Prototip3/FrontendP3/FrontendP3.py)

## Diagrames Prototip 3

[Diagrama Casos d'Ús](./Prototip3/DiagramaCasosUs.puml)

[Diagrama Login](./Prototip3/DiagramaLogin.mermaid)

[Diagrama Login Token](./Prototip3/DiagramaLoginToken.mermaid)

## Prototip 4

[Prototip 4](./Prototip4/)

[Activitat Test Backend P3- Tests Unitaris](./Prototip4/ActivitatTestBackendP3/)






