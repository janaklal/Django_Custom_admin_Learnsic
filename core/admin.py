from typing import Any
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.urls import path
from django.urls.resolvers import URLResolver


def admin_statistics_view(request):
    return render(request, "admin/stats.html", {"title": "Statistics"})


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, _=None):
        app_list = super().get_app_list(request)
        app_list += [{
            "name": "My Charts",
            "app_label": "my_charts",
            "models": [{
                "name": "Statistics",
                "object_name": "statistics",
                "admin_url": "/primeuser/statistics",
                "view_only": True
            }],
        }]

        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [path("statistics/", admin_statistics_view,
                      name="admin-statistics")]
        return urls
