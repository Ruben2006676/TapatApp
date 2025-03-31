## Què són els tests unitaris?
Els tests unitaris són una tècnica de programació que consisteix a provar petites unitats de codi de manera independent per assegurar-se que cada unitat (normalment una funció o mètode) funciona correctament. L'objectiu és identificar possibles errors en una fase primerenca del desenvolupament, millorant la qualitat del codi i facilitant el manteniment.
En un test unitari, es realitzen proves per comprovar que una funció retorna el valor esperat per una sèrie d'entrades definides. Els tests unitaris ajuden a detectar problemes i a garantir que els canvis futurs al codi no introdueixin errors imprevistos.

## Fes una recerca de llibreries de test amb Python.  Com funciona específicament la llibreria unittest de Python?

Python té diverses llibreries per a fer tests, entre les quals es destaca unittest, una llibreria nativa. A més, hi ha altres llibreries populars com pytest i nose.
unittest: És una llibreria integrada a Python que segueix el model de testing basat en classes. Les funcions de test es defineixen dins de classes que hereten de unittest.TestCase, i cada test és un mètode dins d'aquesta classe. Aquesta llibreria proporciona una sèrie d'assertions per verificar el comportament del codi, com per exemple assertEqual, assertTrue, assertFalse, etc.

 Com funciona unittest:


Es crea una classe que hereta de unittest.TestCase.


Es defineixen mètodes dins d'aquesta classe, cada mètode és un test.


Es fa ús d'assertions per verificar els resultats de les funcions o mètodes.


Per executar els tests, es fa servir unittest.main() per fer el llançament del conjunt de tests.

## Les assertions més importants en Unitest

Les assertions són les funcions que es fan servir per comprovar que el codi es comporta de la manera esperada en els tests. Algunes de les més comunes són:

assertEqual(a, b): Comprova que a sigui igual a b.

assertNotEqual(a, b): Comprova que a no sigui igual a b.

assertTrue(x): Comprova que x sigui True.

assertFalse(x): Comprova que x sigui False.

assertIsNone(x): Comprova que x sigui None.

assertIsNotNone(x): Comprova que x no sigui None.

assertIn(a, b): Comprova que a es troba dins de b (p. ex. si una llista conté un element).

assertNotIn(a, b): Comprova que a no es troba dins de b.

assertRaises(exception, func, *args, **kwargs): Comprova que s'aixeca una excepció en cridar func amb els arguments proporcionats.

Aquesta funcionalitat és fonamental per comprovar les condicions del codi de manera rigorosa i automatitzada.
