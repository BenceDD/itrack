# Tutorial

Ez a dokumentum összefoglalja a [Django tutorialt](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

## 1) Projekt beüzemelése:

Az alábbi paranccsal kell létrehozni egy új projektet:

        django-admin startproject mysite

Ez létrehozza a projektet. A projekt az appok és konfigurációk összessége amikből egy weblap felépül.

A projekt mindenféle műveletét, (pl. a szerver elindítása) a `manage.py` program végzi el.

## 2) App létrehozása a projekten belül.

Webalkalmazást az alábbi paranccsal hozunk létre:

        python3 manage.py startapp <alkalmazás neve>

Ez létrehozza az <alkalmazás neve> mappát amiben az alkalmazásunk forráskódját tároljuk.

Projekt létrehozásakor alapértelmezetten létrejön egy alkalmazás, aminek a neve megegyezik a projektével.

## 3) App elkészítése

A djangoban egy weblapot több webalkalmazásból állítunk össze. A projekt alapértelmezetten létrehoz egy a projektnévvel azonos nevű webalkalmazást.

A django lényege, hogy minden weblapot egy függvény állít elő, amelynek a paramétere egy HTTP request, a kimenete pedig egy HTTP válasz.

Ehhez nyissuk meg az újonnan létrehozott alkalmazás `views.py` fájlját!

        # Igy nez ki a vilag legegyszerubb views.py-ja.
        from django.http import HttpResponse
        
        # Create your views here.
        
        def index(request):
            return HttpResponse("Szercsy Lávcsy")

Ezt a függvényt beregisztráljuk egy URL mögé. Ezt az urls.py fájlban tehetjük meg. Ha még nincs ilyenünk, hozzuk létre!

        # Ez a vilag legegyszerubb url beregisztralasa.
        from django.conf.urls import url
        
        from . import views
    
        # Itt tortenik a regisztracio
        urlpatterns = [
            url(r'^$',views.index,name = 'index'),
        ]

Ha kész a webalkalmazásunk akkor be kell regisztrálni az alapértelmezett alkalmazás url-jei közé. Nyissuk meg az alapértelmezett alkalmazás url.py-ját!

        
        from django.conf.urls import include, url # Alapertelmezetten az include nincs beimportolva.
        from django.contrib import admin
        
        urlpatterns = [
            url(r'^tutorial/', include('tutorial_app.urls')), # Itt regisztraltuk be a webalkalmazasunkat.
            url(r'^admin/', admin.site.urls),
        ]

Ha most megnyitjuk az elso parameterben megadott url-t, bejön a weblap, örülünk. Megjelenik a Szercsy Lávcsy egy HTTP response-ban.