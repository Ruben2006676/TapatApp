Cas d’ús: Crear un personatge
Nom del cas d’ús:
Crear un personatge nou

Actor principal:
Usuari registrat (rol: jugador o game master)

Objectiu:
Permetre que l’usuari creï un nou personatge associat al seu compte, amb atributs bàsics com nom, raça, classe i història de fons.

Precondicions:

L’usuari ha d’estar autenticat (haver iniciat sessió).

Ha d’existir una connexió amb el servidor backend.

Descripció del flux principal:

L’usuari accedeix a la pestanya “Mis Personajes” des del menú principal.

Clica el botó “Crear Nuevo Personaje”.

S’obre una finestra amb un formulari dividit en dues pestanyes:

Informació bàsica: nom, raça i classe.

Història: descripció o biografia del personatge.

L’usuari omple els camps i prem el botó “Crear Personaje”.

El sistema valida les dades (per exemple, que cap camp obligatori estigui buit).

El frontend envia la petició al servidor (API REST: /characters).

El backend valida la raça i la classe, crea el personatge i retorna l’ID.

El frontend mostra un missatge d’èxit i actualitza la llista de personatges.

Postcondicions:

El nou personatge queda guardat a la base de dades.

L’usuari pot veure’l a la llista i accedir als seus detalls.

Excepcions:

Si manca algun camp obligatori → es mostra un missatge d’error.

Si falla la connexió amb el servidor → es mostra un error de xarxa.

Si la raça o classe no són vàlides → error validat pel backend.
