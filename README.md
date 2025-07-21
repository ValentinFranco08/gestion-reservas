Gestión de Reservas de Salas de Reunión
Este proyecto es una aplicación web sencilla para gestionar reservas de salas de reunión, usuarios y las propias salas. Está construida con Flask (un microframework de Python), SQLAlchemy para la base de datos, y Tailwind CSS para un diseño moderno y responsivo. Incorpora un patrón de diseño Builder para la creación robusta de reservas y actualiza los estados de las reservas en tiempo real usando AJAX.

🚀 Características
CRUD Completo:

Usuarios: Añade, lista, edita y elimina usuarios.

Salas: Añade, lista, edita y elimina salas con su capacidad.

Reservas: Crea, lista, edita y elimina reservas de salas.

Validaciones Robustas de Reservas:

Verifica la disponibilidad de la sala para el horario seleccionado.

Evita reservas en el pasado.

Maneja conflictos al editar reservas existentes.

Actualizaciones en Tiempo Real: Los estados de las reservas (Próxima, Ocupada, Finalizada) se actualizan dinámicamente en la interfaz de usuario sin necesidad de recargar la página, gracias a peticiones AJAX periódicas.

Diseño Moderno: Interfaz de usuario limpia y funcional gracias a Tailwind CSS.

Patrones de Diseño:

Programación Orientada a Objetos (POO): La aplicación está estructurada con clases (User, Room, Booking) que modelan las entidades del dominio.

Patrón Builder: Implementado para la creación controlada y validada de objetos Booking, separando la lógica de construcción de la representación del objeto.

Filtros de Reservas: Permite filtrar las reservas por usuario o por sala.

Mensajes Flash: Notificaciones informativas para el usuario sobre el éxito o el error de las operaciones.

🛠️ Tecnologías Utilizadas
Backend:

Python 3.12+

Flask: Microframework web.

Flask-SQLAlchemy: ORM para interactuar con la base de datos.

SQLite: Base de datos ligera para desarrollo.

Frontend:

HTML

Tailwind CSS: Framework CSS de utilidad.

JavaScript (Vanilla JS): Para la interactividad y las actualizaciones en tiempo real.

Font Awesome: Para los íconos.

📂 Estructura del Proyecto
Gestion_Reservas/
├── instance/                 # Contiene la base de datos SQLite (generada automáticamente)
│   └── site.db
├── app/                      # Módulo principal de la aplicación Flask
│   ├── __init__.py           # Inicializa la aplicación Flask y la base de datos
│   ├── models/               # Clases que representan las tablas de la base de datos (POO)
│   │   ├── __init__.py
│   │   └── booking_model.py  # Modelos User, Room, Booking y lógica de validación
│   ├── routes/               # Define las rutas y la lógica de negocio de la aplicación
│   │   ├── __init__.py
│   │   └── web_routes.py     # Rutas para el CRUD de usuarios, salas y reservas, y API de estado
│   ├── patterns/             # Implementación de patrones de diseño
│   │   ├── __init__.py
│   │   └── booking_builder.py # Clase Builder para la creación de reservas
│   └── templates/            # Archivos HTML (Jinja2)
│       ├── base.html         # Plantilla base con Tailwind CSS y Font Awesome
│       ├── index.html        # Página principal con el listado de reservas y formulario de creación
│       ├── users.html        # Gestión de usuarios
│       ├── rooms.html        # Gestión de salas
│       ├── edit_user.html    # Formulario para editar usuario
│       ├── edit_room.html    # Formulario para editar sala
│       └── edit_booking.html # Formulario para editar reserva
├── config.py                 # Configuración de la aplicación (claves secretas, BD)
├── run.py                    # Script para iniciar la aplicación
└── requirements.txt          # Dependencias del proyecto

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

🧪 Uso de la Aplicación
Página Principal (/):

Verás un formulario para crear nuevas reservas.

Una tabla muestra todas las reservas existentes, con filtros por usuario y sala.

Los estados de las reservas se actualizan automáticamente cada 10 segundos.

Botones para editar y eliminar reservas.

Gestión de Usuarios (/users):

Añade nuevos usuarios.

Lista todos los usuarios registrados.

Edita y elimina usuarios existentes (con validación si tienen reservas activas o futuras).

Gestión de Salas (/rooms):

Añade nuevas salas con su nombre y capacidad.

Lista todas las salas disponibles.

Edita y elimina salas existentes (con validación si tienen reservas activas o futuras).

