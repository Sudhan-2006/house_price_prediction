from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('predict/', views.predict_price, name='predict'),
    path('history/', views.history, name='history'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('upload/', views.upload_csv, name='upload'),
    path('report/pdf/', views.download_report, name='download_report'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('admin-dashboard/predictions/', views.admin_predictions, name='admin_predictions'),
    path('admin-dashboard/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-dashboard/models/', views.admin_models, name='admin_models'),
    path('admin-dashboard/dataset/', views.admin_dataset, name='admin_dataset'),
    path('admin-dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('admin-dashboard/csv-download/', views.admin_csv_download, name='admin_csv_download'),
    path(
    'admin-dashboard/pdf-report/',
    views.admin_pdf_report,
    name='admin_pdf_report'
),

path(
    'admin-dashboard/analytics-report/',
    views.analytics_pdf_report,
    name='analytics_pdf_report'
),
]