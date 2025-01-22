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
Els codis d'estat HTTP són respostes numèriques que el servidor envia al client per indicar l'estat de la petició. Aquests codis es poden agrupar en cinc categories, cada una amb una finalitat específica:

Aquí hi han alguns exemples: 

### Codi d'estat 1xx - Informatius
Els codis d'estat de la categoria 1xx indiquen que el servidor ha rebut la petició i que s'està processant. Són codis informatius, que normalment no s'utilitzen en la comunicació entre el navegador i el servidor.
100 Continue: El servidor ha rebut la primera part de la petició i el client pot continuar enviant la resta.

### Codi d'estat 2xx - OK
Els codis de la categoria 2xx indiquen que la petició s'ha processat correctament i que el servidor ha retornat una resposta satisfactòria.
200 OK: La petició ha estat exitosa. El cos de la resposta conté els resultats sol·licitats.
201 Created: La petició ha estat exitosa i ha creat un nou recurs (com en una petició POST per afegir un element).
202 Accepted: La petició ha estat acceptada, però encara no s'ha processat.

### Codi d'estat 3xx - Redirecció
Els codis de la categoria 3xx indiquen que el client ha de realitzar una altra acció per completar la petició. En general, aquests codis impliquen que el client ha de ser redirigit a una altra URL.
301 Moved Permanently: El recurs sol·licitat ha estat mogut de manera permanent a una nova URL.
302 Found (anteriorment anomenat "Moved Temporarily"): El recurs sol·licitat es troba temporalment en una URL diferent.
303 See Other: El client ha de realitzar una petició GET a una altra URL per obtenir el recurs.

### Codi d'estat 4xx - Errors del client
Els codis de la categoria 4xx indiquen que hi ha un problema amb la petició del client. Potser falta informació o hi ha errors en la sol·licitud.
400 Bad Request: La petició és mal formada o conté dades incorrectes.
401 Unauthorized: El client no ha proporcionat les credencials correctes per accedir a un recurs protegit.
403 Forbidden: El servidor entén la petició, però es nega a autoritzar-la. Potser el client no té permisos.
404 Not Found: El recurs sol·licitat no es troba al servidor.

### Codi d'estat 5xx - Errors del servidor
Els codis de la categoria 5xx indiquen que hi ha un problema amb el servidor que impedeix processar la petició, fins i tot si la petició era vàlida.
500 Internal Server Error: Error general del servidor. El servidor no ha pogut completar la petició per una raó desconeguda.
501 Not Implemented: El servidor no suporta la funció necessària per processar la petició.




