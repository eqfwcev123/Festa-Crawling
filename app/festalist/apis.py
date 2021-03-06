from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from festalist.models import FestaList
from festalist.serializers import FestaListSerializer, FestaListKeywordPostSerializer, FestaListKeywordSerializer, \
    FestaListKeywordDeleteSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = 30


class FestaListAPIView(APIView):
    pagination_class = BasicPagination
    serializer_class = FestaListSerializer

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        category = request.query_params.get('category')

        if category == 'pay':
            instance = FestaList.objects.filter(tickets__contains="₩").exclude(tickets__contains="무료")
        elif category == 'free':
            instance = FestaList.objects.filter(tickets__contains="무료").exclude(tickets__contains="₩")
        elif category == 'exterior':
            instance = FestaList.objects.filter(tickets="[]")
        else:
            instance = FestaList.objects.all()

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FestaListDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            festalist = FestaList.objects.get(pk=pk)
            serializer = FestaListSerializer(festalist)
            data = {
                'detail': serializer.data
            }
            return Response(data)
        except:
            return Response(data={"detail": "잘못된 이벤트 입니다"}, status=status.HTTP_204_NO_CONTENT)


class FestaListKeywordUpload(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = Token.objects.get(key=request.auth).user
            keywords = user.festalistkeyword_set.all()
            serializer = FestaListKeywordSerializer(keywords, many=True)
            data = {
                'keywords': serializer.data
            }
            return Response(data)
        except:
            return Response(data={"detail": "존재하지 않는 사용자입니다."}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        try:
            user = Token.objects.get(key=request.auth).user
            serializer = FestaListKeywordPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user.id)

                keywords = user.festalistkeyword_set.all()
                return_serializer = FestaListKeywordSerializer(keywords, many=True)
                data = {
                    'keywords': return_serializer.data
                }
                return Response(data)
            else:
                return Response(serializer.errors)
        except:
            return Response(data={"detail": "존재하지 않는 사용자입니다."}, status=status.HTTP_204_NO_CONTENT)


class FestaListKeywordDelete(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            user = Token.objects.get(key=request.auth).user
            keyword = user.festalistkeyword_set.get(id=pk)
            user.festalistkeyword_set.remove(keyword)
            keywords = user.festalistkeyword_set.all()
            serializer = FestaListKeywordDeleteSerializer(keywords, many=True)
            print(keyword)
            return Response(data={'keywords': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(data={"detail": "존재하지 않는 사용자입니다."}, status=status.HTTP_204_NO_CONTENT)

# 이메일발송 테스트용
# class FestaListOpenEventAPIView(APIView):
#     def post(self, request):
#         serializer = FestaListOpenEventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors)
