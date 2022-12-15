# SRI-models

En este repo están implementados 3 sistemas de recuperacion de informacion, el modelo booleano, el vectorial y el análisis de semántica latente

Proyecto de Sistemas de Recuperación de Información
Modelo booleano, vectorial y ...

Kevin Talavera Diaz C-311

Facultad de Matemática y Computación
Universidad de La Habana
Curso 2021-2022

Instalar dependencias: pip install -r requirements.txt

Manual de usuario:

--La ejecución se inicia al es escribir: python main.py en la consola

Nota:
Para usar el Crawling es necesaio estar conectado a internet.
OJO: Si el firewall está activado hay que darle conección a:
 -vscode
 -navegador(chrome, firefox, opera, etc)

1- Modelos: Booleano, Vectorial, LSA.

2- Desea Crawlear: (Si ó no).

  2.1- Si se marcó “no” ir a paso (3).
  
  2.2- Si se marcó “si” ir a paso (2.3).
  
  2.3- Teclee tiempo límite: tiempo que desea que demore la ejecución del crawleado y si el modelo es el booleano ir al paso (5), sino ir al paso (7).

3- Desea usar base de datos de CRANFIELD: (Si ó no).

  3.1-    Si se marcó “no” ir al paso (4).
  
  3.2-    Si se marcó “si” ir al paso (3.3).
  
  3.3-    Desea usar consultas de CRANFIELD: (Si ó no):

    3.3.1-  Si se marcó “no” y se marcó modelo booleano ir al paso (5),     si no ir al paso (7).
    
    3.3.2-  Si se marcó “si” y se marcó modelo booleano ir al paso (6) y luego comienza la ejecución, en caso que sea otro modelo la ejecución comienza automáticamente.

4- Ingresar el path: Se tiene que poner una dirección válida de donde quiera realizar consultas en la PC. Si se marcó modelo booleano ir al paso (5), si no ir al paso (7).

5- Modos de Consulta: (Solo modelo booleano) Se implementaron 2, el casual y el experto: El casual es para usuarios no versados en el álgebra booleana y que puedan escribir consultas en lenguaje natural.
El experto es aquel que tiene al menos conocimientos básicos de lógica y puede escribir consultas con el formato de expresiones lógicas.

6- Tipo de coincidencia: (Solo modelo booleano) Se implementaron 2 tipos, la coincidencia parcial y la total.
Esto solo afecta a las consultas de usuarios casuales, ya que el algoritmo al recibir una consulta en lenguaje natural es incapaz de detectar signos de agrupación. Ej:
A y B o C puede ser interpretado como A y (B o C) ó (A y B) o C lo cual sería muy ambiguo.
La propuesta para hacer una consulta más amigable es que el usuario decida si quiere encontrar coincidencias exactas de los términos (coincidencia total) y esto en programa sería poner operadores AND entre los pares de términos, o si desea coincidencias parciales, es decir, cualquier término de la consulta que aparezca en un documento, es parte de los documentos recuperados, esto se lleva a cabo poniendo operadores OR entre todos los pares de términos de la consulta.

7- Teclear una consulta deseada en correspondencia con las opciones anteriores elegidas.

8- Se mostrarán los documentos recuperados.
