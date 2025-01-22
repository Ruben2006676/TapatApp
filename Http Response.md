# Http Response
Una HTTP Response (Resposta HTTP) és la resposta que el servidor envia al client després d'una petició HTTP (com ara una petició GET o POST). La resposta inclou informació sobre si la petició va ser procesada correctament o si va ocórrer un error.

Una resposta HTTP general es compon de tres parts principals:

Línia d'estat (Status Line)
Headers
Body

## Línia d'estat (Status Line)
El protocol de la resposta: Normalment HTTP/1.1 o HTTP/2.
El codi d'estat HTTP: Un número que indica l'estat de la petició (com 200, 404, 500, etc.).
La descripció de l'estat: Una breu explicació del codi d'estat (com "OK" o "Not Found").

## Headers
Els headers són metadades que proporcionen informació addicional sobre la resposta, com el tipus de contingut, la longitud del contingut, les cookies, i altres detalls de la comunicació.
Exemples de headers comuns:
Content-Type: Indica el tipus de contingut de la resposta (per exemple, text/html, application/json, image/jpeg).
Content-Length: Indica la mida del contingut en bytes.
Date: La data i hora en què es va generar la resposta.
Server: La informació sobre el servidor que ha generat la resposta.
Set-Cookie: Si s'han establert cookies al client.

## Body (cos de la resposta)
El body de la resposta conté les dades que el servidor vol enviar al client. El contingut del body depèn del tipus de petició i la resposta, i pot ser una pàgina web HTML, un document JSON, un fitxer d'imatge, etc.
HTML: En el cas de pàgines web, el cos serà el codi HTML.
JSON: Quan s'està treballant amb API RESTful, el cos sovint serà un objecte o array JSON.
binari: Quan es carrega un fitxer, el cos contindrà les dades binàries d'aquest fitxer (per exemple, una imatge o un document).

## Codis d’estat de Response Http
Els codis d'estat HTTP són respostes numèriques que el servidor envia al client per indicar l'estat de la petició. Aquests codis es poden agrupar en cinc categories, cada una amb una finalitat específica.


