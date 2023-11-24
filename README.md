#Manual de uso del lenguaje
###Antes de empezar
Además del código del compilador, es necesario tener instalado el lenguaje Python y las siguientes librerías, que están disponibles tanto en conda como pip:
matplotlib.pyplot
numpy
Las otras librerías requeridas para el proyecto, como statistics o sys, ya están incluidas en la instalación o se incluyen directamente en el proyecto, como PLY.
Archivo de entrada
El compilador de MyRLanguage soporta cualquier tipo de terminación, pero se recomienda hacer uso de archivos .txt
Estructura general del programa
Lo primero que se debe hacer para la creación del programa, es indicar que es un programa con la palabra reservada “program” y posteriormente darle un nombre al mismo. Después de eso, se crea el main, todo en la siguiente estructura:
'''
program helloWorld;
main(){
    write("Hello World");
}
'''
###Comentarios
Estas son líneas que serán ignoradas, se usan para poner mensajes que facilitan la legibilidad del código. Se indica que una línea es comentario usando el carácter “%”
'''
program helloWorld;
main(){
    %este es un comentario!
    write("Hello World");
}
'''
Declaración de variables globales
El lenguaje soporta variables de tipo int, float y char. Se tiene que escribir la palabra reservada “vars” primero, y después de eso, se pueden declarar múltiples variables del mismo tipo en la misma línea. Las variables vendrán pre inicializadas, con valores dependiendo de su tipo: 0 para int, 0.0 para float, y ‘ ‘ para char. Estas variables se podrán usar en cualquier parte del código, y la declaración se tiene que hacer justo después del programa:

program varGlob;
vars
int i, j;
float n, m;
char a, b;

main(){
    write("Hello World");
}
Declaración de variables locales
Estas variables son en la mayoría de los casos iguales a las globales, pero éstas se declaran en una función, y a diferencia de las globales, sólo estarán activas en esa función.

program varLoc;
vars
int a, b;

function void print()
vars 
int i, j;
{
    write(i, " ", a);
    write(j, " ", b);
}
    
main(){
    print();
}

Declaración y acceso a Arreglos
El lenguaje de programación también soporta el uso de arreglos tanto globales como locales, de los mismos tipos que las variables. Para hacerlo, sólo hace falta agregar un número entero que indique el tamaño del arreglo, contenido entre “[ ]”  después del nombre de la variable. Para acceder a algún dato contenido en el arreglo, se pone una expresión entre “[ ]”. Nótese que si la expresión no es de tipo int, o si tiene un valor menor a 0, o mayor al tamaño del arreglo, esto causará un error.

program arreglos;
vars
int i, j[5];
float n[3], m;
char a, b[100];

main(){
    n[2] = 5.8;
    write(n[2]);
}
Entrada y Salida
Para recibir datos de la consola, se usa la palabra reservada “read”, seguida de la variable en la que se va a guardar el dato. Para escribir a consola, se usa “write”, y despliega en la misma línea los valores que contenga.

program manzanas;
vars
int cantidad;
main(){
    write("Cuantas manzanas quieres?");
    read(cantidad);
    write("Entregar ", cantidad, " manzana(s)");
}
Operadores lógicos, aritméticos y booleanos
El lenguaje soporta las siguientes operaciones aritméticas haciendo uso de los operadores indicados entre paréntesis: resta(-), suma(+), multiplicación(*), división(/), restante(%); así como los siguientes operadores lógicos: menor que (<), mayor a(>) , menor o igual (<=), mayor o igual (>=), igual (==), diferente de (<>); y los siguientes operadores booleanos: y (&), o (|). Para usarlos, sólo es necesario ponerlos entre dos expresiones.

program operadores;
main(){
    write(4 * 5 + 6);
    write(3 < 1 & 4 > 2);
}
Asignación
Para asignarle un valor a una variable, se usa el operador “=”. Este permite asignarle el valor de una expresión o de una llamada a función.

program asignacion;
vars
int cantidad;

function int squared(int i){
    i = i * i;
    return(i);
}
main(){
    cantidad = 4 * 5 + 6;
    write(cantidad);
    cantidad = squared(cantidad);
    write(cantidad);
}
Ciclos
El lenguaje soporta el uso de while y for. While sirve para repetir un segmento de código mientras una condición sea cierta, y for permite repetir un segmento de código un número contado de veces, sumando uno a uno a la variable de control:

program ciclos;
vars
int i;

main(){
    while (i < 5) do {
        write(i);
        i = i + 1;
    }
    for i = 0 to 5 do {
        write(i);
    }
}
Funciones, returns y llamadas
Si se va a repetir un pedazo de código muchas veces, se puede utilizar una función para evitar escribir lo mismo múltiples veces, y sólo llamar a la función cada que se quiera ejecutar ese pedazo de código. Estas funciones pueden ser de tipo void, int, float o char, pueden recibir constantes, variables o arreglos como parámetros, pueden llamarse a sí mismas u a otras funciones, y se declaran de la siguiente manera:

program funciones;
vars
int array[5], i;
float prom;

function void print(int a[5]){
    for i = 0 to 4 do {
        write("indice ",i , " = ", a[i]);
    }
}

function float promedio(int a[5])
vars float total, aux;
{
    for i = 0 to 4 do {
        aux = float(a[i]);
        total = total + aux;
    }
    total = total / 5;
    return(total);
}
    
main(){
    for i = 0 to 4 do {
        read(array[i]);
    }

    print(array);

    prom = promedio(array);
    write("el promedio es ", prom);
}
Funciones especiales:
El programa también contiene unas funciones especiales precargadas, estas se llaman igual a cualquier otra función y a continuación se presentan sus entradas, salidas y uso:

int(x) = Recibe un valor float y trunca los decimales para regresar un int
float(x) = Recibe un valor int y regresa el valor convertido a float
pow(x,y) = Recibe dos valores int o float y regresa el valor de x elevado a y.
rand() = Regresa un valor float aleatorio entre 0 y 1.
med(array) = Recibe un arreglo de valores int o float y regresa un float con la media de los valores contenidos en el arreglo
moda(array) = Recibe un arreglo de valores int o float y regresa un float con la moda de los valores contenidos en el arreglo, en caso de algún empate, regresa el primer valor de entre los valores.
var(array)  = Recibe un arreglo de valores int o float y regresa un float con la varianza de los valores contenidos en el arreglo
reg(array) = Recibe un arreglo de valores int o float, despliega una ventana con un gráfico de la regresión lineal de los valores contenidos en el arreglo, pausando la ejecución del código hasta que se cierre.
plot(array) = Recibe un arreglo de valores int o float, despliega una ventana con un gráfico de línea de los valores contenidos en el arreglo, pausando la ejecución del código hasta que se cierre.
Ejecución de código
Para ejecutar el programa, sólo se tiene que escribir en la consola “python MyRparse.py”, seguido del nombre del archivo que contiene nuestro programa. Por defecto no se muestran las operaciones internas de la ejecución del código, pero se pueden mostrar agregando cualquier carácter a la consola después del nombre del archivo. Las líneas a introducir a la consola se verían así:

python MyRparse.py nombreArchivo.txt

python MyRparse.py nombreArchivo.txt 0
