from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # User routes
    path('', views.guest_page, name='guest'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='home_page'),
    path('delete/', views.delete_user, name='delete_user'),
    path('report_issue/', views.report_issue, name='report_issue'),
    path('success/', views.success_view, name='success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('all-complaints/', views.all_complaints, name='all_complaints'),

    # Admin and management
    path('admin/', admin.site.urls),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-complaints/', views.admin_complaints, name='admin_complaints'),
    path('admin-feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin-complaints/update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('admin-complaint/delete/<int:complaint_id>/',views.delete_complaint,name='delete_complaint'),




    # Feedback management
    path('admin-feedback/toggle/<int:feedback_id>/', views.toggle_feedback, name='toggle_feedback'),
    path('admin-feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
]

# Static/media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
