from datetime import datetime
from app.models.booking_model import Booking # ¡Importación cambiada!

class BookingBuilder:
    def __init__(self):
        self.booking_data = {}
        self.error_message = None

    def set_user(self, user):
        self.booking_data['user'] = user
        return self

    def set_room(self, room):
        self.booking_data['room'] = room
        return self

    def set_schedule(self, start_time_str, end_time_str):
        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

            if start_time < datetime.now():
                self.error_message = "La fecha y hora de inicio no pueden ser en el pasado."
                return self

            is_available, msg = Booking.is_time_slot_available(
                room_id=self.booking_data['room'].id,
                start_time=start_time,
                end_time=end_time
            )

            if not is_available:
                self.error_message = msg
                return self

            self.booking_data['start_time'] = start_time
            self.booking_data['end_time'] = end_time
        except ValueError:
            self.error_message = "Formato de fecha y hora inválido. Asegúrate de que sea 'YYYY-MM-DDTHH:MM'."
        return self

    def set_purpose(self, purpose):
        self.booking_data['purpose'] = purpose
        return self

    def build(self):
        if self.error_message:
            return None
        
        required_fields = ['user', 'room', 'start_time', 'end_time', 'purpose']
        for field in required_fields:
            if field not in self.booking_data:
                self.error_message = f"Faltan datos para crear la reserva: {field}."
                return None

        return Booking(
            user=self.booking_data['user'],
            room=self.booking_data['room'],
            start_time=self.booking_data['start_time'],
            end_time=self.booking_data['end_time'],
            purpose=self.booking_data['purpose']
        )

    def get_error(self):
        return self.error_message