from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin

from .models import ShortURL
from .serializers import ShortURLSerializer

'''
Uwagi:
1. Brakowało informacji o tym co dokładnie użytkownik podaje na wejściu: sam 'url' czy też nazwę/id/pk
pod jakim należałoby umieścić skrócony link. Na https://tinyurl.com/app sa dwie opcje: użytkownik sam podaje
skróconą i unikalną nazwę, lub dostaje automatycznie i losowo wygenerowany adres. w dokumentacji mam przykład
adresu `http://localhost:8000/shrt/`, ale nie wiem czy 'shrt' podaje użytkownik, czy jest to wygenerowane
przez api, czy może po slashu należy podać 'pk' do obiektu. Założyłem, że żeby utworzyć automatyczne i
losowe 'id' musiałbym zaimplementować jakiś algorytm hashujący. Skoro głównym założeniem było zrobienie
minimalistycznej aplikacji to tego nie robiłem. Z kolei użycie automatycznego id w formie 'int' mijałoby się 
z dobrymi praktykami na ekspozycję url. Dlatego z założenia user podaje 'short' czyli skróconą nazwę do adresu
ora docelowy url.

2a. Pierwszy działający kod zrobiłem w 15min, ale potem godzinami zastanawiałem się nad instrukcjami i zaleceniami
w dokumentacji. Bo "minimalizm" rozumiałem najpierw jako pełną "surowość" i użycie tylko najpotrzebniejszych
rozwiązań, i nic poza tym. Więc powstał widok oparty o generic i mixiny:

class CreateRetrieveShortURLView(CreateModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

2b. Potem uznałem, że skoro "Przez minimalizm rozumiemy nie robienie ręcznie czegoś co potrafi zrobić framework"
to może chodzi o to, żeby maksymalnie wykorzystać możliwości automatyzacji w Django, przy jak najmniejszej
ilości kodu. I wtedy zrobiłem widok oparty o ViewsSets oraz dołączony do tego kompleksowy router w urls:

class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'short'

2c. Na końcu uznałem, że skoro "Funkcjonalność ma być ekstremalnie minimalistyczna, nie chodzi o dodawanie super 
features (potraktuj to jako podpowiedź tu nie trzeba wiele kodować", to oznaczałoby, że niepotrzebne byłyby metody i 
akcje jak np. delete czy update. W takim razie zostałem przy concrete views i "tylko" tych funkcjonalności jakie są
niezbędne do stworzenia tego konkretnego "prostego api"

3. Nie jest jasne co dokładnie ma być zwrócone: brakuje określeń w stylu "tylko", "co najmniej", "również" lub "m.in.".
Docelowo widoki zwracają wszystkie swoje pola, a skoro jednym z nich jest docelowy/długi url a drugim skrócona nazwa
'short', to zarówno przy tworzeniu jak i wywołaniu oba te elementy są zwracane. Nie wiem czy mam zawężyć do "tylko"
krótkiego url, a potem "tylko" rozwinięcia długiego, czy to ma po prostu znaleźć się jako jedna ze zwracanych wartości.
Tak więc ostatecznie oba widoki zwracają długi adres, a widok tworzący nowego linka zwraca dodatkowo adres w takiej 
formie, w jakiej jest to podane w instrukcji.
'''


class CreateShortURLView(CreateAPIView):
    serializer_class = ShortURLSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['short_url'] = reverse('short-url', kwargs={'short': request.data['short']}, request=request)
        return response


class RetrieveShortURLView(RetrieveAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'short'
