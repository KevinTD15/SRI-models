# SRI-models
En este repo se implementarán 3 sistemas de recuperacion de informacion, por ahora solo estará el modelo booleano

Proyecto de Sistemas de Recuperación de Información
Modelo Booleano



Kevin Talavera Diaz C-311

Facultad de Matemática y Computación
Universidad de La Habana
Curso 2021-2022

Link: https://github.com/KevinTD15/SRI-models.git

Resumen.  Pre-entrega del proyecto final de Sistemas de Recuperación de Indormación. Modelo Booleano implementado en Python. Este está compuesto por 3 módulos: Procesamiento de Texto, Modelado del SRI y el módulo principal donde se realizan las consultas en consola

Keywords: path: dirección


Requerimientos de Software:
	python 3.10.7
	numpy 1.23.4
	sympy 1.11.1
	nltk 3.7

	Introducción
El modelo booleano constituye el primer modelo teórico empleado para establecer el subconjunto de documentos relevantes, en relación a una consulta específica realizada a una colección de documentos sean estos páginas disponibles en la web o en una biblioteca digital. Está basado en el álgebra de Boole, por lo que se considera como un modelo simple y fácil de implementar, por lo que fue el preferido en los Sistemas de Recuperación tempranos

	Módulo Principal

En este módulo es donde se muestran las opciones disponibles para el uso del modelo. Este cuenta con 4 etapas:

--La ejecución se inicia al es escribir: python main.py en la consola

	Ingresar el path: Se tiene que poner una direccion valida de donde quiera realizar consultas en la PC
	Modos de Consulta: Se implementaron 2 modos, el casual y el experto: El casual es para usuarios no versados en el álgebra booleano y que puedan escribir consultas en lenguaje natural.
El experto es aquel que tiene al menos conocimientos basicos de logica y puede escribir consultas con el formato de expresiones logicas
	Tipo de coincidencia: Tiene 2 tipos, la coincidencia parcial y la total. Esto solo afecta a las consultas de usuarios casuales, ya que el algoritmo al recibir una consulta en lenguaje natural es incapaz de detectar signos de agrupacion. Ej:
A y B o C puede ser interpretado como A y (B o C) ó
(A y B) o C lo cual sería muy ambiguo. 
La propuesta para hacer una consulta mas amigable es que el usuario decida si quiere encontrar coincidencias exactas de los terminos(coincidencia total) y esto en programa sería poner operadores AND entre los pares de términos, o si desea coincidencias parciales, es decir, cualquier término de la consulta que aparezca en un documento, ese documento es parte de lo recuperado, esto se lleva a cabo poniendo operadores OR entre todos los pares de terminos de la consulta
	Teclear una consulta deseada en correspondencia con las opciones anteriores elegidas
	Se mostrarán los documentos recuperados



	Procesamiento de texto
Para poder implementar mecanismos de recuperación sobre una colección de documentos de textos es necesario obtener una representación de los mismos. Con el objetivo de lograr dicha representación se utilizó una bibliotecla de python llamada nltk ya que esta nos modifica los textos de forma tal que solo queden palabras que no carezcan de significado, por ejemplo: sustantivos, adjetivos, entre otras.
La forma de trabajo con esta biblioteca, que se ve reflejado en el módulo tokenizer.py del proyecto fue la siguiente:
	Se recibe el conjunto de documentos
	Se itera por cada uno de estos
	Sea d_i el documento correspondiente a la iteracion i-ésima de estos:
3.1- Todos los terminos de d_i son llevados a minúscula
3.2- Haciendo uso de la función stopwords de nltk son eliminados los articulos, preposiciones y otros terminos no deseados
	Al finalizar con todos los documentos, estas transformaciones son devueltas al módulo model.py



	Modelación
De manera general, en este punto se recibe tanto el conjunto de documentos como la consulta, y otros 2 parametros que se explicaran mas en detalle cuando se comente acerca de las funcionalidades implementadas. 
	El conjunto de documentos es procesado mediante el módulo tokenizer.py previamente explicado 
	Se crea una matriz en la cual las filas son los documentos y las columnas los terminos.
	 La consulta puede procesarse de 2 formas, primeramente si es escrita en lenguaje natural se hace de igual forma que los documentos, la otra forma es que si ya es escrita en forma de álgebra booleana nos saltamos ese paso de procesamiento ya que no es necesario.
	Haciendo uso de la biblioteca sympy cada termino de la consulta se vuelve un símbolo, el cual esta biblioteca reconoce como una varablie con la que se pueden hacer operaciones booleanas. 
	Mediante la funcion to_dnf del propio sympy la consulta ya reconocida como epresión booleana es llevada a FND (Forma Normal Disyuntiva) 
	Cada una de las componentes conjuntivas de esta es buscada en la matriz de ocurrencia previamente mencionada y los q se correspondan son documentos a ser devueltos
Referencias:
	Expresiones booleanas con sympy: 
https://omz-software.com/pythonista/sympy/modules/logic.html
	Listar archivos de un directorio:
https://j2logo.com/python/listar-directorio-en-python/#:~:text=Para%20listar%20o%20recorrer%20un,archivos%20y%20carpetas%20que%20contiene.
	Uso de numpy:
https://numpy.org/doc/stable/user/index.html#user
	Procesamiento de texto con nltk
https://www.nltk.org/
