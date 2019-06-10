from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet

from registry.models import Registry, BlockRequest
from registry.serializers import BlockRequestSerializer
from registry.tools import get_client_ip
from .serializers import RegistrySerializer


class RegistryViewSet(ModelViewSet):
    """
    CREATE/LIST/RETREIVE actions on blocklist
    """
    http_method_names = ['get', 'post']
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = RegistrySerializer
    queryset = Registry.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlockRequestViewSet(ModelViewSet):
    """
    CREATE/LIST/RETREIVE actions on Block Requests
    """
    http_method_names = ['get', 'post']

    serializer_class = BlockRequestSerializer
    queryset = BlockRequest.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user_ip=get_client_ip(self.request))
