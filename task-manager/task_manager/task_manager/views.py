from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def index(self, **kwargs):
        context = super().index(**kwargs)
        context["who"] = "World"
        return context