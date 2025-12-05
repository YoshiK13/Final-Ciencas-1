# Sistema de Gestión de Estudiantes con Árboles AVL

## Integrantes del Proyecto

- **Davidson Esfleider Sanchez Gordillo** - 20231020183
- **Diego Felipe Diaz Roa** - 20201020147
- **Dania Lizeth Guzmán Triviño** - 20221020061
- **Joshoa Alarcon Sanchez** - 20221020013

---

## Descripción General

Sistema de gestión de base de datos no relacional que permite almacenar, consultar, actualizar y eliminar información de estudiantes universitarios. El sistema utiliza **árboles AVL autobalanceados** para la indexación y búsqueda eficiente por clave principal (ID de estudiante), con persistencia de datos en archivos **JSON**.

---

## Estructura del Proyecto

```
Final-Ciencas-1/
├── Archivos/
│   ├── estudiantes_ejemplo.json  # Archivo de ejemplo
|   └── estudiantes.json          # Archivo de persistencia
├── Logica/
│   ├── __init__.py               # Inicializador del paquete
│   ├── Arboles.py                # Implementación de nodos y Árboles AVL
│   ├── Estudiante.py             # Clase Estudiante
│   └── Gestor.py                 # Gestor principal del sistema
├── Visual/
    └── App.py                    # Interfaz de consola
├── Main.py                       # Inicializar y ejecutar el programa
```

---

## Funcionalidades del Sistema

###  1. Agregar Nuevo Estudiante

Permite registrar un nuevo estudiante en el sistema.

**Datos requeridos**:
- ID del estudiante (único, numérico)
- Nombre completo (texto)
- Edad (número entre 15 y 100)
- Carrera (texto)
- Semestre (número entre 1 y 12)

**Proceso**:
1. El sistema valida que el ID no exista previamente
2. Valida rangos de edad y semestre
3. Inserta el estudiante en el árbol AVL (complejidad O(log n))
4. Guarda automáticamente en el archivo JSON

**Ejemplo de uso**:
```
ID del estudiante: 1001
Nombre completo: Juan Pérez
Edad: 20
Carrera: Ingeniería de Sistemas
Semestre: 5
```

---

###  2. Buscar Estudiante por ID

Búsqueda rápida utilizando el árbol AVL.

**Complejidad**: O(log n)

**Entrada**: ID del estudiante (numérico)

**Salida**: Detalles completos del estudiante si existe, mensaje de error si no se encuentra.

---

###  3. Buscar Estudiantes por Nombre

Búsqueda parcial por nombre (no requiere coincidencia exacta).

**Complejidad**: O(n) - búsqueda lineal

**Entrada**: Nombre o parte del nombre (texto)

**Salida**: Lista de todos los estudiantes cuyo nombre contenga el texto ingresado.

**Ejemplo**:
- Búsqueda: "Juan"
- Encuentra: "Juan Pérez", "María Juana González", "Juanita López"

---

###  4. Buscar Estudiantes por Carrera

Filtra estudiantes por carrera académica.

**Complejidad**: O(n) - búsqueda lineal

**Entrada**: Nombre de la carrera (búsqueda parcial)

**Salida**: Lista de estudiantes en la carrera especificada.

---

###  5. Actualizar Información de Estudiante

Modifica los datos de un estudiante existente.

**Campos actualizables**:
- Nombre
- Edad
- Carrera
- Semestre

**Nota**: El ID no se puede modificar (es la clave principal).

**Proceso**:
1. Busca el estudiante por ID
2. Muestra los datos actuales
3. Solicita nuevos valores (presionar ENTER mantiene el valor actual)
4. Actualiza los campos modificados
5. Guarda automáticamente en JSON

---

###  6. Eliminar Estudiante

Elimina un estudiante del sistema con confirmación de seguridad.

**Proceso**:
1. Busca el estudiante por ID
2. Muestra los datos del estudiante
3. Solicita confirmación (s/n)
4. Elimina del árbol AVL manteniendo el balance

**Seguridad**: Requiere confirmación explícita antes de eliminar.

---

###  7. Listar Todos los Estudiantes

Muestra todos los estudiantes registrados en orden ascendente por ID.

**Formato de salida**: Tabla ASCII con columnas:
- ID
- Nombre
- Edad
- Carrera
- Semestre

**Orden**: Recorrido in-order del árbol AVL (estudiantes ordenados por ID).

---

###  8. Ver Estadísticas

Genera un reporte estadístico del sistema.

**Información mostrada**:
- Total de estudiantes registrados
- Edad promedio de los estudiantes
- Distribución de estudiantes por carrera (con gráfico de barras ASCII)
- Porcentajes por carrera

---

## Restricciones y Validaciones

### Restricciones de Datos

| Campo | Tipo | Restricción |
|-------|------|-------------|
| **ID Estudiante** | Entero | Único, no puede repetirse |
| **Nombre** | Texto | No puede estar vacío |
| **Edad** | Entero | Rango: 15 - 100 años |
| **Carrera** | Texto | No puede estar vacío |
| **Semestre** | Entero | Rango: 1 - 12 |

### Validaciones Automáticas

**Al agregar**:
- Verifica que el ID no exista previamente
- Valida rangos de edad y semestre
- Verifica que los campos de texto no estén vacíos

**Al actualizar**:
- Verifica que el estudiante exista
- Valida nuevos valores si se proporcionan
- Permite mantener valores actuales (presionando ENTER)

**Al eliminar**:
- Verifica que el estudiante exista
- Requiere confirmación explícita

**Al limpiar datos**:
- Requiere escribir "CONFIRMAR" en mayúsculas
- Muestra advertencia clara sobre irreversibilidad

---

### Restricciones Técnicas

- **No se pueden usar IDs duplicados**: El sistema rechazará cualquier intento de agregar un estudiante con un ID existente.
- **No se puede modificar el ID**: Una vez creado, el ID es inmutable (es la clave principal del árbol AVL).
- **Persistencia obligatoria**: Todas las operaciones de modificación guardan automáticamente en JSON (no se puede desactivar).
- **Formato JSON estricto**: El archivo debe mantener la estructura definida.

---

## Formato de Persistencia (JSON)

### Estructura del Archivo **estudiantes.json**

```json
{
    "total_estudiantes": 12,
    "estudiantes": [
        {
            "id_estudiante": 5,
            "nombre": "Carlos",
            "edad": 17,
            "carrera": "Administracion",
            "semestre": 1
        },
        {
            "id_estudiante": 10,
            "nombre": "Luis",
            "edad": 18,
            "carrera": "Ingenieria en Sistemas",
            "semestre": 3
        },
        {
            "id_estudiante": 15,
            "nombre": "Sofia",
            "edad": 18,
            "carrera": "Diseño Grafico",
            "semestre": 2
        }, ........
    ]
}
```

---

## Arquitectura del Sistema

### Módulo **Arboles.py**

**Clases implementadas**:

1. **Nodo**: Clase base para los árboles
2. **NodoBinario**: Nodo de árbol binario de búsqueda
3. **NodoAVL**: Nodo de árbol AVL con balanceo automático

**Métodos principales**:
- **agregar_hijo()**: Inserción con balanceo
- **buscar_nodo()**: Búsqueda O(log n)
- **eliminar_nodo()**: Eliminación con rebalanceo
- **rotar_derecha()** / **rotar_izquierda()**: Rotaciones de balanceo
- **balancear()**: Verifica y aplica rotaciones necesarias

### Módulo **Estudiante.py**

**Clase Estudiante**:

Representa la entidad de un estudiante universitario.

**Atributos**:
- **id_estudiante**: Llave principal del estudiante (int)
- **nombre**: Nombre completo (str)
- **edad**: Edad en años (int)
- **carrera**: Carrera académica (str)
- **semestre**: Semestre actual (int)

**Métodos**:
- **__repr__()**: Representación legible
- **to_dict()**: Conversión a diccionario para JSON

### Módulo **Gestor.py**

**Clase GestorEstudiantes**:

Controlador principal del sistema.

**Atributos**:
- **raiz**: Raíz del árbol AVL
- **archivo_json**: Ruta del archivo de persistencia
- **total_estudiantes**: Contador de estudiantes

**Métodos principales**:
- **agregar_estudiante()**: Crea al estudiante
- **buscar_estudiante()**: Busca al estudiante por ID
- **actualizar_estudiante()**: Actualiza la información del estudiante
- **eliminar_estudiante()**: Eliminar al estudiante
- **listar_estudiantes()**: Listar todos los estudiantes
- **buscar_por_nombre()**: Búsqueda por nombre del estudiante
- **buscar_por_carrera()**: Búsqueda por carrera del estudiante
- **guardar_en_json()**: Almacena la información del estudiante en un archivo .JSON
- **cargar_desde_json()**: Carga la información del archivo .JSON
- **obtener_estadisticas()**: Análisis de datos de la lista.

---

### Módulo **App.py**

**Clase App**:

Interfaz de usuario de consola.

**Características**:
- Menú interactivo con 12 opciones
- Validaciones de entrada
- Mensajes de error descriptivos
- Confirmaciones de seguridad
- Tablas ASCII formateadas

---

## Licencia

Este proyecto es de uso académico y educativo.
