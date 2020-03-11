from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Purchase
from .serializers import PurchaseSerializer


class CurrentUserPurchaseList(generics.ListAPIView):
    """
    https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-current-user
    """
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Purchase.objects.filter(purchaser=user)


class PurchaseListByUsername(generics.ListAPIView):
    """
    https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
    """
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)


class PurchaseListByQueryString(generics.ListAPIView):
    """
    https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    """

    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Purchase.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset


class PurchaseListSearch(generics.ListAPIView):
    """
    https://www.django-rest-framework.org/api-guide/filtering/#searchfilter
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class PurchaseListOrder(generics.ListAPIView):
    """
    https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name', ]
    ordering = ['id']
