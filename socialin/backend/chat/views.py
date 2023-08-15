from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from .models import Conversation, Message
from user.models import CustomUser as User
from .serializers import ConversationListSerializer, ConversationSerializer, ConversationSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['chat'])
class StartConversationView(generics.GenericAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        receiver = data.pop('receiver')
        try:
            participant = User.objects.get(username=receiver['username'])
        except User.DoesNotExist:
            return Response({'message': 'You cannot chat with a non-existent user'})

        conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                                   Q(initiator=participant, receiver=request.user))
        if conversation.exists():
            return redirect('get_conversation', id=conversation[0].id) 
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            serializer = ConversationSerializer(instance=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['chat'])
class GetConversationView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def set_messages_read(self, conversation_id, user):
        messages = Message.objects.filter(conversation_id=conversation_id).exclude(sender=user)
        messages.update(is_read=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.set_messages_read(instance.id, request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['chat'])
class ConversationsListView(generics.ListAPIView):
    serializer_class = ConversationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(Q(initiator=self.request.user) |
                                           Q(receiver=self.request.user))
