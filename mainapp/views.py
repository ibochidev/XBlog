from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from .models import Post



class MainIndex(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):

        list = Post.objects.order_by("-added_at").all()

        kwargs['list'] = list

        return super().get_context_data(**kwargs)



class PostCreate(CreateView):

    model = Post
    fields = ['subject', 'content', 'image']
    template_name = 'main/post_form.html'
    success_url = '/'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        request.title = 'Saqlash'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('main.add_post'):
            raise PermissionDenied()
        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect('name:index')
