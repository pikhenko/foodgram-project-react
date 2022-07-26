from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscribe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .filters import IngredientSearchFilter, RecipeFilters
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          RegistrationSerializer, ShoppingCartSerializer,
                          SubscriptionSerializer, TagSerializer)


class CreateUserView(UserViewSet):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return User.objects.all()


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user, following=user)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe, user__id=user_id, following__id=author_id)
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_class = RecipeFilters
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipeSerializerPost


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientSearchFilter)
    pagination_class = None
    search_fields = ['^name', ]


class BaseFavoriteCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class ShoppingCartViewSet(BaseFavoriteCartViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart


class FavoriteViewSet(BaseFavoriteCartViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    model = Favorite


class DownloadShoppingCart(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'],)
    def download(self, request):
        final_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__shoppingcarts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )

        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('FreeSans', 'data/FreeSans.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.pdf"')
        page = canvas.Canvas(response)
        page.setFont('FreeSans', size=20)
        page.drawString(250, 800, 'Список покупок')
        page.setFont('FreeSans', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
