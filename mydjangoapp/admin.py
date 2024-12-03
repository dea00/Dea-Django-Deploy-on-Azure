from django.contrib import admin
from .models import *

admin.site.register(Leagues)
admin.site.register(Teams)
admin.site.register(Drafts)
admin.site.register(Matches)
admin.site.register(Players)
admin.site.register(Playerstatistics)
admin.site.register(Trades)
admin.site.register(Waivers)

# Register your models here.
