from sqlmodel import select
from app.api.deps import SessionDep
from app.api.models import Presentation, Room
from app.api.schemas.schedule import PresentationSchedule, RoomSchedule


def read_schedule(session: SessionDep):
    stmt = (
        select(Room, Presentation)
            .join(Presentation, Room.id == Presentation.room_id)  # inner join
            .order_by(Room.id, Presentation.time_start)
    )
    results = session.exec(stmt).all()

    print(results)

    grouped_results = {}  # key - id of room, value - room object and list of presentations
    for room, presentation in results:
        if room.id not in grouped_results:
            grouped_results[room.id] = {
                "room": room,
                "presentations": []
            }
        grouped_results[room.id]["presentations"].append(presentation)

    room_schedules = []
    for room_id, data in grouped_results.items():
        room = data["room"]
        presentations = data["presentations"]
        presentation_schedules = []
        for presentation in presentations:
            presentation_schedules.append(PresentationSchedule(**presentation.model_dump()))
        room_schedules.append(
            RoomSchedule(room_id=room.id, room_name=room.name, presentations=presentation_schedules)
        )

    return room_schedules
