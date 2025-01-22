Una resposta HTTP és el missatge que un servidor retorna al client després de rebre una petició HTTP (com una petició GET o POST). Aquesta resposta informa el client sobre si la petició s'ha processat correctament o si ha ocorregut un error.

En general, una resposta HTTP es divideix en tres components principals:

Línia d'estat (Status Line)

Capçaleres (Headers)

Cos de la resposta (Body)


## Línia d'estat (Status Line)

La línia d'estat inclou:

Protocol de la resposta: Sovint HTTP/1.1 o HTTP/2.

Codi d'estat HTTP: Un número que descriu el resultat de la petició (exemples: 200, 404, 500).

Descripció de l'estat: Un text breu que explica el codi d'estat, com "OK" o "Not Found".

## Capçaleres (Headers)

Les capçaleres són metadades que ofereixen informació addicional sobre la resposta, com ara el tipus de contingut, la mida o les cookies associades. Alguns exemples comuns són:

Content-Type: Especifica el format del contingut retornat (ex.: text/html, application/json).
Content-Length: Indica la mida del contingut en bytes.
Date: Registra la data i l'hora en què es va generar la resposta.
Server: Proporciona informació sobre el servidor que ha processat la sol·licitud.
Set-Cookie: Utilitzat per enviar cookies al client.

## Cos de la resposta (Body)

El cos conté les dades que el servidor envia al client. El tipus de contingut depèn de la petició i la resposta, i pot incloure:

HTML: Quan el servidor retorna una pàgina web.

JSON: Sovint utilitzat en respostes d'APIs per enviar dades estructurades.

Binari: Per fitxers com imatges o documents.

## Codis d’estat HTTP
Els codis d'estat són números que el servidor utilitza per indicar el resultat de la petició. Es classifiquen en cinc categories:

### 1xx - Informatius

Aquests codis indiquen que la petició s'està processant. Normalment no són visibles per als usuaris finals.

100 Continue: El servidor ha rebut la petició inicial, i el client pot continuar.

### 2xx - Èxit

Els codis d’aquesta categoria assenyalen que la petició ha estat processada amb èxit.

200 OK: La petició ha estat satisfactòria i el contingut sol·licitat s'ha retornat.

201 Created: La petició ha creat un nou recurs.

202 Accepted: La petició s'ha acceptat, però encara no s'ha completat.

### 3xx - Redirecció

Indiquen que el client necessita realitzar una acció addicional per accedir al recurs.

301 Moved Permanently: El recurs s'ha traslladat de forma permanent a una nova URL.

302 Found: El recurs es troba temporalment en una altra ubicació.

303 See Other: El client ha de fer una nova petició GET a una altra URL.

### 4xx - Errors del client

Aquests codis reflecteixen problemes amb la petició enviada pel client.

400 Bad Request: La petició és incorrecta o té errors.

401 Unauthorized: Calen credencials vàlides per accedir al recurs.

403 Forbidden: El servidor rebutja la petició malgrat ser comprensible.

404 Not Found: El recurs sol·licitat no existeix.

### 5xx - Errors del servidor

Aquests codis indiquen que el servidor ha tingut un problema en processar la petició.

500 Internal Server Error: Un error general que impedeix completar la petició.

501 Not Implemented: El servidor no admet la funcionalitat requerida per completar la petició.











