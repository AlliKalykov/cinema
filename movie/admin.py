from django.contrib import admin
from .models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'long_time', 'start_date', 'end_date', 'company', 'is_active')
    list_filter = ('start_date', 'end_date', 'company')
    search_fields = ('name', 'company')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Room)
admin.site.register(Job)
admin.site.register(Employee)
admin.site.register(Ticket)
admin.site.register(Session)
admin.site.register(Seat)
admin.site.register(Sector)
admin.site.register(TicketPrice)
admin.site.register(MovingTicket)
