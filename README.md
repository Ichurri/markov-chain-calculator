# Aplicación de Cálculo de Cadenas de Markov

Esta es una aplicación de interfaz gráfica (GUI) desarrollada en Python utilizando Tkinter. La aplicación permite calcular matrices de transición y distribuciones de probabilidad para cadenas de Markov.

## Requisitos

- Python 3.x
- Paquetes de Python: tkinter, numpy

Puedes instalar los paquetes necesarios ejecutando:
```sh
pip install numpy
```

## Uso

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local utilizando:

```sh
git clone https://github.com/Ichurri/markov-chain-queueing-calculator
cd tu_repositorio
```
### 2. Ejecutar la aplicación
Puedes ejecutar la aplicación directamente con Python:

```sh
python markov-chain-calculator.py
```
### 3. Crear un ejecutable (opcional)
Si deseas crear un archivo ejecutable para ejecutar la aplicación sin necesidad de un compilador de código, puedes utilizar PyInstaller. Primero, instala PyInstaller:

```sh
pip install pyinstaller
```
Luego creas el ejecutable:

```sh
pyinstaller --onefile --windowed markov-chain-calculator.py
```

El archivo ejecutable se generará en la carpeta dist.

### 4. Utilizar la aplicación
Al abrir la aplicación, verás una interfaz con el título "Cálculo de Cadenas de Markov".

Número de estados: Ingresa el número de estados de la cadena de Markov.

Haz clic en el botón "Establecer Matriz". Esto generará una matriz de entrada donde podrás ingresar las probabilidades de transición entre los estados.

Número de etapas (n): Ingresa el número de etapas para las cuales deseas calcular las probabilidades de estado.

Haz clic en el botón "Calcular" para obtener los resultados.

### 5. Resultados
La aplicación mostrará los siguientes resultados en el área de texto:

Matriz de transición de estado estacionario
Vector de distribución de probabilidad
Probabilidades de estado en la etapa especificada
Probabilidades de estado estable

## Ejemplo de uso
Ingresa "3" como el número de estados y haz clic en "Establecer Matriz".
Ingresa las probabilidades de transición en la matriz (asegúrate de que la suma de cada fila sea 1).
Ingresa "10" como el número de etapas (n).
Haz clic en "Calcular".

#### Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.##