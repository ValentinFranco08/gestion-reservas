# app/routes/web_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify # Importar jsonify
from app import db
from app.models.booking_model import User, Room, Booking
from app.patterns.booking_builder import BookingBuilder
from datetime import datetime

bp = Blueprint('main', __name__)

# --- Rutas Principales y de Reservas ---
@bp.route('/')
def index():
    user_id_filter = request.args.get('user_id', type=int)
    room_id_filter = request.args.get('room_id', type=int)

    query = Booking.query

    if user_id_filter:
        query = query.filter_by(user_id=user_id_filter)
    if room_id_filter:
        query = query.filter_by(room_id=room_id_filter)

    bookings = query.order_by(Booking.start_time.desc()).all()
    
    users = User.query.all()
    rooms = Room.query.all()
    
    current_time = datetime.now()

    return render_template(
        'index.html', 
        users=users, 
        rooms=rooms, 
        bookings=bookings,
        current_time=current_time,
        user_id_filter=user_id_filter,
        room_id_filter=room_id_filter
    )

# --- Nueva ruta API para obtener el estado de las reservas ---
@bp.route('/api/bookings_status')
def get_bookings_status():
    user_id_filter = request.args.get('user_id', type=int)
    room_id_filter = request.args.get('room_id', type=int)

    query = Booking.query

    if user_id_filter:
        query = query.filter_by(user_id=user_id_filter)
    if room_id_filter:
        query = query.filter_by(room_id=room_id_filter)

    bookings = query.order_by(Booking.start_time.desc()).all()
    
    current_time = datetime.now()
    
    # Prepara los datos para ser enviados como JSON
    bookings_data = []
    for booking in bookings:
        status = ''
        if current_time > booking.end_time:
            status = 'Finalizada'
        elif current_time >= booking.start_time and current_time <= booking.end_time:
            status = 'Ocupada'
        else:
            status = 'Próxima'
        
        bookings_data.append({
            'id': booking.id,
            'user_name': booking.user.name,
            'room_name': booking.room.name,
            'start_time': booking.start_time.strftime('%d-%m-%y %H:%M'),
            'end_time': booking.end_time.strftime('%d-%m-%y %H:%M'),
            'purpose': booking.purpose,
            'status': status
        })
    
    return jsonify(bookings_data)


@bp.route('/book', methods=['POST'])
def create_booking():
    user_id = request.form.get('user_id')
    room_id = request.form.get('room_id')
    start_time_str = request.form.get('start_time')
    end_time_str = request.form.get('end_time')
    purpose = request.form.get('purpose')

    user = User.query.get(user_id)
    room = Room.query.get(room_id)

    if not all([user, room, start_time_str, end_time_str, purpose]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('main.index'))

    builder = BookingBuilder()
    booking = builder.set_user(user)\
                     .set_room(room)\
                     .set_schedule(start_time_str, end_time_str)\
                     .set_purpose(purpose)\
                     .build()

    if booking:
        db.session.add(booking)
        db.session.commit()
        flash('Reserva creada con éxito.', 'success')
    else:
        flash(f'Error al crear la reserva: {builder.get_error()}', 'error')
        
    return redirect(url_for('main.index'))

@bp.route('/bookings/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash('Reserva eliminada con éxito.', 'success')
    return redirect(url_for('main.index'))

# --- Rutas para ACTUALIZAR Reservas ---
@bp.route('/bookings/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    booking = Booking.query.get_or_404(id)
    users = User.query.all()
    rooms = Room.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        room_id = request.form.get('room_id')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        purpose = request.form.get('purpose')

        user = User.query.get(user_id)
        room = Room.query.get(room_id)

        if not all([user, room, start_time_str, end_time_str, purpose]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('main.edit_booking', id=id))
        
        try:
            new_start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            new_end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash("Formato de fecha y hora inválido. Asegúrate de que sea 'YYYY-MM-DDTHH:MM'.", 'error')
            return redirect(url_for('main.edit_booking', id=id))

        if new_start_time < datetime.now() and booking.start_time >= datetime.now():
            flash("No puedes cambiar la hora de inicio a una fecha pasada para una reserva futura.", 'error')
            return redirect(url_for('main.edit_booking', id=id))

        is_available, msg = Booking.is_time_slot_available(
            room_id=room.id,
            start_time=new_start_time,
            end_time=new_end_time,
            current_booking_id=booking.id
        )

        if not is_available:
            flash(f'Error al actualizar la reserva: {msg}', 'error')
            return redirect(url_for('main.edit_booking', id=id))

        booking.user_id = user.id
        booking.room_id = room.id
        booking.start_time = new_start_time
        booking.end_time = new_end_time
        booking.purpose = purpose
        
        db.session.commit()
        flash('Reserva actualizada con éxito.', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit_booking.html', booking=booking, users=users, rooms=rooms)


# --- Rutas para CRUD de Usuarios ---
@bp.route('/users')
def manage_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@bp.route('/users/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    if name and email:
        if not User.query.filter_by(email=email).first():
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario añadido con éxito.', 'success')
        else:
            flash('El correo electrónico ya existe. Por favor, usa otro.', 'error')
    else:
        flash('Nombre y correo son obligatorios para añadir un usuario.', 'error')
    return redirect(url_for('main.manage_users'))

@bp.route('/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    
    active_bookings = Booking.query.filter(
        Booking.user_id == id,
        Booking.end_time > datetime.now()
    ).first()

    if active_bookings:
        flash('No se puede eliminar el usuario porque tiene reservas activas o futuras. Elimina sus reservas primero.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Usuario eliminado con éxito.', 'success')
    return redirect(url_for('main.manage_users'))

# --- Rutas para ACTUALIZAR Usuarios ---
@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            existing_user_with_email = User.query.filter_by(email=email).first()
            if existing_user_with_email and existing_user_with_email.id != user.id:
                flash('El correo electrónico ya existe para otro usuario. Por favor, usa otro.', 'error')
            else:
                user.name = name
                user.email = email
                db.session.commit()
                flash('Usuario actualizado con éxito.', 'success')
                return redirect(url_for('main.manage_users'))
        else:
            flash('Nombre y correo son obligatorios para actualizar un usuario.', 'error')
    return render_template('edit_user.html', user=user)

# --- Rutas para CRUD de Salas ---
@bp.route('/rooms')
def manage_rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@bp.route('/rooms/add', methods=['POST'])
def add_room():
    name = request.form.get('name')
    capacity = request.form.get('capacity')
    if name and capacity:
        try:
            capacity_int = int(capacity)
            if capacity_int <= 0:
                flash('La capacidad debe ser un número positivo.', 'error')
                return redirect(url_for('main.manage_rooms'))

            if not Room.query.filter_by(name=name).first():
                new_room = Room(name=name, capacity=capacity_int)
                db.session.add(new_room)
                db.session.commit()
                flash('Sala añadida con éxito.', 'success')
            else:
                flash('El nombre de la sala ya existe. Por favor, usa otro.', 'error')
        except ValueError:
            flash('La capacidad debe ser un número entero.', 'error')
    else:
        flash('Nombre y capacidad son obligatorios para añadir una sala.', 'error')
    return redirect(url_for('main.manage_rooms'))

@bp.route('/rooms/delete/<int:id>', methods=['POST'])
def delete_room(id):
    room = Room.query.get_or_404(id)

    active_bookings = Booking.query.filter(
        Booking.room_id == id,
        Booking.end_time > datetime.now()
    ).first()

    if active_bookings:
        flash('No se puede eliminar la sala porque tiene reservas activas o futuras. Elimina sus reservas primero.', 'error')
    else:
        db.session.delete(room)
        db.session.commit()
        flash('Sala eliminada con éxito.', 'success')
    return redirect(url_for('main.manage_rooms'))

# --- Rutas para ACTUALIZAR Salas ---
@bp.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    room = Room.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = request.form.get('capacity')
        if name and capacity:
            try:
                capacity_int = int(capacity)
                if capacity_int <= 0:
                    flash('La capacidad debe ser un número positivo.', 'error')
                    return redirect(url_for('main.edit_room', id=id))
                
                existing_room_with_name = Room.query.filter_by(name=name).first()
                if existing_room_with_name and existing_room_with_name.id != room.id:
                    flash('El nombre de la sala ya existe. Por favor, usa otro.', 'error')
                else:
                    room.name = name
                    room.capacity = capacity_int
                    db.session.commit()
                    flash('Sala actualizada con éxito.', 'success')
                    return redirect(url_for('main.manage_rooms'))
            except ValueError:
                flash('La capacidad debe ser un número entero.', 'error')
        else:
            flash('Nombre y capacidad son obligatorios para actualizar una sala.', 'error')
    return render_template('edit_room.html', room=room)