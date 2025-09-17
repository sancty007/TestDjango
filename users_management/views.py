
from rest_framework import viewsets, permissions, filters
from authentication.models import User
from .serializers import AdminUserSerializer
from rest_framework.pagination import PageNumberPagination

class AdminUserPagination(PageNumberPagination):
    page_size = 5

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    print("Filtering and ordering enabled" , filter_backends)
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    ordering_fields = ['id', 'username', 'email', 'role']
    ordering = ['id']

    def list(self, request, *args, **kwargs):
        self.pagination_class = AdminUserPagination
        return super().list(request, *args, **kwargs)