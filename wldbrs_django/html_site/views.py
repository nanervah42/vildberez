from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView
from .models import wb_base


class HomeIndex(ListView):  # вместо index
    model = wb_base  # определяем модель откуда беруться все данные
    template_name = 'wldbrs_django/index.html'  # переопределяем дефолтное название шаблона
    context_object_name = 'wldbrs'  # переопределяем дефолтное название объекта
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)  # получаем контекст, который уже есть
        context['title'] = 'Главная страница'  # дополняем его
        context['products'] = wb_base.objects.values('product_type', 'product_type_name').order_by('product_type_name',
                                                                                    ).distinct()
        return context

    def get_queryset(self):  # правим дефолтный запрос который ~ SELECT все поля FROM таблица, без всяких условий
        return wb_base.objects.all().order_by('-updated_time')


class Category(ListView):
    model = wb_base
    template_name = 'wldbrs_django/index.html'
    context_object_name = 'wldbrs'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)  # получаем контекст, который уже есть
        context['title'] = 'Главная страница'  # дополняем его
        context['products'] = wb_base.objects.values('product_type', 'product_type_name').order_by('product_type_name',
                                                                                    ).distinct()
        return context

    def get_queryset(self):  # правим дефолтный запрос который ~ SELECT все поля FROM таблица, без всяких условий
        return wb_base.objects.filter(product_type=self.kwargs['product_type']).order_by('-updated_time')


# class Telegram(ListView):
#     model = wb_base
#     template_name = 'wldbrs_django/telegram.html'
#     context_object_name = 'wldbrs'
#     paginate_by = 3
#
#     def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
#         context = super().get_context_data(**kwargs)  # получаем контекст, который уже есть
#         context['title'] = 'Главная страница'  # дополняем его
#
#         return context


class Telegram(TemplateView):
    template_name = 'wldbrs_django/telegram.html'

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)  # получаем контекст, который уже есть
        context['title'] = 'Телеграм'  # дополняем его

        return context


class About(TemplateView):
    template_name = 'wldbrs_django/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)  # получаем контекст, который уже есть
        context['title'] = 'О Проекте'  # дополняем его

        return context