from rest_framework import viewsets, status
from .models import Meal,Rating
from .serializers import MealSerializer,RatingSerializer,UserSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                'token': token.key,},
                status=status.HTTP_201_CREATED)
    def list(self, request, *args, **kwargs):
        return Response({'message': 'Not allowed'},
                        status=status.HTTP_400_BAD_REQUEST)
    
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        meal = self.get_object()
        stars = request.data.get('stars')

        if stars is None:
            return Response({'message': 'stars not provided'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            stars = int(stars)
        except (TypeError, ValueError):
            return Response({'message': 'stars must be an integer'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not 1 <= stars <= 5:
            return Response({'message': 'stars must be between 1 and 5'},
                            status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            user=request.user, meal=meal, defaults={'stars': stars}
        )
        return Response(
            {
                'message': 'Meal Rate Created' if created else 'Meal Rate Updated',
                'result': RatingSerializer(rating).data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way To create or update'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create (self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way To create or update'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    