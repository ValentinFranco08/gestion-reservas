# 🗓️ Gestión de Reservas de Salas de Reunión

Este proyecto es una aplicación web sencilla para gestionar reservas de salas de reunión, usuarios y las propias salas. Está construida con **Flask**, **SQLAlchemy** y **Tailwind CSS**, e implementa el patrón de diseño **Builder** para la creación robusta de reservas. También incorpora actualizaciones en tiempo real mediante **AJAX**.

## 🚀 Características

### CRUD Completo

- **Usuarios**: Añade, lista, edita y elimina usuarios.
- **Salas**: Añade, lista, edita y elimina salas con su capacidad.
- **Reservas**: Crea, lista, edita y elimina reservas de salas.

### Validaciones Robustas de Reservas

- Verifica la disponibilidad de la sala para el horario seleccionado.
- Evita reservas en el pasado.
- Maneja conflictos al editar reservas existentes.

### Actualizaciones en Tiempo Real

- Los estados de las reservas (*Próxima, Ocupada, Finalizada*) se actualizan dinámicamente sin recargar la página usando peticiones AJAX periódicas.

### Diseño Moderno

- Interfaz de usuario limpia y responsiva gracias a **Tailwind CSS**.

### Patrones de Diseño

- **Programación Orientada a Objetos (POO)**: Clases `User`, `Room`, `Booking` modelan las entidades del dominio.
- **Builder**: Clase Builder que controla la creación y validación de objetos `Booking`.

### Funcionalidades Adicionales

- Filtros de reservas por usuario o por sala.
- Mensajes flash informativos sobre el éxito o error de las operaciones.

---

## 🛠️ Tecnologías Utilizadas

### Backend

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- SQLite

### Frontend

- HTML
- Tailwind CSS
- JavaScript (Vanilla)
- Font Awesome

---

⚙️ Instalación y Ejecución
Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

Prerrequisitos
Python 3.12 o superior instalado.

1. Clona el Repositorio
git clone <url_del_repositorio>
cd Gestion_Reservas

2. Crea y Activa un Entorno Virtual
Es una buena práctica para gestionar las dependencias del proyecto.

python3 -m venv venv
source venv/bin/activate  # En Linux/macOS
# o en Windows: venv\Scripts\activate

3. Instala las Dependencias
pip install -r requirements.txt

4. Configura la Aplicación
Asegúrate de que el archivo config.py exista en la raíz de tu proyecto (al mismo nivel que run.py) 

5. Inicializa la Base de Datos
La base de datos SQLite (site.db) se creará automáticamente la primera vez que inicies la aplicación en la carpeta instance/.

6. Ejecuta la Aplicación
python3 run.py

La aplicación se ejecutará en http://127.0.0.1:5000/. Abre esta URL en tu navegador web.

