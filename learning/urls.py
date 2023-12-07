# from django.contrib import admin
# from django.urls import path
# from .views import ai_generate_view  # import your view

# # Function to append your custom URL
# def get_custom_admin_urls(urls):
#     custom_urls = [
#         path('problemset/AI-generate/', admin.site.admin_view(ai_generate_view), name='ai-generate')
#     ]
#     return custom_urls + urls

# # Extend the get_urls method of the admin site
# admin_site = admin.site
# admin_site.get_urls = get_custom_admin_urls(admin_site.get_urls())
