from django.conf.urls.defaults import *
from django.views.generic import list_detail
from blog.models import Post, Category

urlpatterns = patterns('blog.views',
    (r'^$', list_detail.object_list, {'queryset': Post.objects.order_by('-created'),
                                    'template_name': 'display_posts.html',
                                    'template_object_name': 'post'}),
  
    (r'^add_post$', 'add_post'),
    (r'^add_author$', 'add_author'),
    (r'^add_category$', 'add_category'),
    (r'^edit_post/(?P<id>\d+)$', 'edit_post'),
    (r'^edit_category/(?P<id>\d+)$', 'edit_category'),
    (r'^edit_author/(?P<id>\d+)$', 'edit_author'),
    (r'^delete_post/(?P<id>\d+)', 'delete_post'),
    (r'^(?P<categories>[-a-zA-Z0-9]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-a-zA-Z0-9]+)/?$', 'get_post'),
    (r'^categories/(?P<slug>\w+)/?$', 'get_category'),
    (r'^users/(?P<id>\d+)/(?P<username>\w+)/?$', 'get_author'),
    (r'^delete_comment/(?P<id>\d+)', 'delete_comment'),
)