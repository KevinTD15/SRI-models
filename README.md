# SRI-models
En este repo se implementarán 3 sistemas de recuperacion de informacion, por ahora solo estará el modelo booleano

Proyecto de Sistemas de Recuperación de Información
Modelo Booleano

Kevin Talavera Diaz C-311

Facultad de Matemática y Computación
Universidad de La Habana
Curso 2021-2022

Resumen.  Pre-entrega del proyecto final de Sistemas de Recuperación de Información. Modelo Booleano implementado en Python. Este está compuesto por 3 módulos: Procesamiento de Texto, Modelado del SRI y el módulo principal donde se realizan las consultas en consola

Manual de usuario:

1-Comienzo de la ejecución: en la consola teclear python main.py


2-Path de donde se van a leer los documentos: en la consola teclear el path


3-Tipo de consulta( 1-Casual, 2-Experto ): 

  Casual: teclear consulta en lenguaje natural
  
  Experto: teclear consulta usando operadores lógicos:
  
      & - and (el lenguaje también reconoce como and las palabras -y-, -de-)
      
      | - or (el lenguaje también reconoce como or la letra -o-)
      
      ~ - not (el lenguaje también reconoce como not la palabra -no-)
      
      
4-Tipo de coincidencia(1-Total, 2-Parcial)(Esta opcién solo se verá si la consulta es Casual):
  
  Total: Solo busca coincidencias exactas de los términos de la consulta con los de los coumentos (equivalente a hacer AND entre todos los términos de la consulta)
  
  Parcial: Busca coincidencias de cualqiuera de los términos de la consulta con los de los documentos (equivalente a hacer OR entre todos los términos de la         consulta)


5-Ingresar consulta: Escribir la consulta en correspondencia con las opciones anteriormente seleccionadas


6-Visualización de los resultados


7-Final de la ejecucion(1-Final, 2- Hacer otra consulta):
  
  Final: Termina la ejecución del programa
  
  Hacer otra consulta: Permite hacer una nueva consulta comenzando el ciclo nuevamente
