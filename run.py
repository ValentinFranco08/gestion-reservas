import os
from app import create_app, db

app = create_app()

# Este bloque se asegura de que todo esté listo para la base de datos
with app.app_context():
    # Obtenemos la ruta absoluta a la carpeta 'instance'
    # Flask guarda la ruta en app.instance_path
    instance_path = app.instance_path

    # Verificamos si la carpeta 'instance' no existe y la creamos si es necesario
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print("📂 Carpeta 'instance' creada.")

    # create_all() es seguro de ejecutar. Solo creará las tablas si no existen.
    db.create_all()
    print("✅ Base de datos y tablas verificadas.")

if __name__ == '__main__':
    app.run(debug=True)