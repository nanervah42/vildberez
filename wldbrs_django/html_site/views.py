from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import MainBase

class HomeIndex(ListView):   # вместо index
    model = MainBase        # определяем модель откуда беруться все данные
    template_name = 'wldbrs_django/index.html'   # переопределяем дефолтное название шаблона
    context_object_name = 'wldbrs'        # переопределяемn дефолтное название объекта
    # paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)            # получаем контекст, который уже есть
        context['title'] = 'Главная страница'                   # дополняем его
        return context

    # def get_queryset(self):     # правим дефолтный запрос который ~ SELECT все поля FROM таблица, без всяких условий
        # return News.objects.filter(is_published=True).select_related('category')   # select_related для уменьшения sql запросов(тема в дебаг тулз)