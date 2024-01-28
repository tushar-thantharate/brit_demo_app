from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum

from products.models import Products


class AuthorizedDashboardView(TemplateView):
    template_name = "auth_dashboard.html"

    @method_decorator(
        login_required
    )  # Ensures that the user must be logged in to access this view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetches all products and the count of products for the authorized user
        context["products"] = Products.objects.filter(user=self.request.user)
        context["products_count"] = Products.objects.filter(user=self.request.user).count()
        return context


class SummaryPageView(TemplateView):
    template_name = "summary_page.html"

    @method_decorator(
        login_required
    )  # Ensures that the user must be logged in to access this view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculates the total price of all products for the authorized user
        context["products_count"] = Products.objects.filter(user=self.request.user).aggregate(
            total_price=Sum("price")
        )["total_price"]

        return context
