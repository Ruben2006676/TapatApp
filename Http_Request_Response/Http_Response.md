# Resposta HTTP

Quan un servidor rep una petició HTTP (com un GET o POST), respon amb un missatge HTTP que informa el client sobre l'estat de la sol·licitud i, si escau, li retorna el recurs sol·licitat o una explicació de l'error.

## Components d'una resposta HTTP

### Línia d'estat (Status Line)

Conté informació bàsica sobre la resposta:

Protocol: Generalment HTTP/1.1 o HTTP/2.

Codi d'estat HTTP: Un número que indica si la petició ha tingut èxit o ha fallat (ex.: 200, 404, 500).

Descripció de l'estat: Explicació breu del codi, com "OK" o "Not Found".

### Capçaleres (Headers)

Metadades que proporcionen informació sobre la resposta, com:

Content-Type: Indica el format del contingut retornat (ex.: text/html, application/json).

Content-Length: Mida del contingut en bytes.

Date: Data i hora en què es va generar la resposta.

Server: Informació sobre el servidor que ha processat la sol·licitud.

Set-Cookie: Envia cookies al client per emmagatzemar informació.

### Cos de la resposta (Body)

Conté les dades enviades al client, com ara:

HTML: Quan el servidor retorna una pàgina web.

JSON: Format estructurat habitual en respostes d'APIs.

Binari: Per a imatges, documents o altres fitxers.

## Codis d'estat HTTP

Els codis d'estat indiquen el resultat de la petició i es classifiquen en cinc categories principals:

## 1xx - Informatius

100 Continue: El servidor ha rebut la petició i el client pot continuar.

## 2xx - Èxit

200 OK: La petició s'ha completat amb èxit.

201 Created: S'ha creat un nou recurs correctament.

## 3xx - Redirecció

301 Moved Permanently: El recurs s'ha traslladat permanentment a una nova URL.

302 Found: El recurs s'ha mogut temporalment.

## 4xx - Errors del client

400 Bad Request: La petició conté errors.

401 Unauthorized: Cal autenticació per accedir al recurs.

403 Forbidden: L'accés està denegat malgrat ser vàlid.

404 Not Found: El recurs no existeix.

## 5xx - Errors del servidor

500 Internal Server Error: Hi ha hagut un problema al servidor.

501 Not Implemented: La funcionalitat sol·licitada no està disponible.











