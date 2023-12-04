from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializer import RoomSerializer

@api_view(['GET'])
def get_routes(response):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def get_rooms(response):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(["GET"])
def get_room_by_id(response, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
