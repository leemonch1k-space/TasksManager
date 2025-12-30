class NextUrlMixin:
    default_next = "/"

    def get_next_url(self):
        hx_url = self.request.headers.get("HX-Current-URL")
        if hx_url:
            return hx_url

        return self.request.GET.get("next", self.default_next)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.get_next_url()
        return context
