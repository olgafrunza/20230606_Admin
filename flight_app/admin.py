from django.contrib import admin
from .models import Flight, Reservation, Passenger
from django.utils.timezone import now
# Register your models here.

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class FlightRecource(resources.ModelResource):
    class Meta:
        model = Flight

class FlightAdmin2(ImportExportModelAdmin):
    resource_class = FlightRecource

    list_display = ("flight_number", "airlines", "departure_city", "arrival_city", "date", "time", "remaining_days")
    # list_editable = ("date",)
    list_filter = ("airlines", "departure_city", "arrival_city")
    ordering = ("-date","time")
    search_fields = ("departure_city", "arrival_city")
    list_per_page = 10
    date_hierarchy = "date"

    fieldsets = (
        ("Main", { "fields" : ("flight_number", "airlines")}),
        ("Places", {
            "classes": ("collapse", ), 
            "fields": ( ("departure_city", "arrival_city"),)}),
        ("Dates", {"fields": ("date", "time")})
    )

    def remaining_days(self, item):
        return (item.date - now().date()).days


class PassengerInline(admin.TabularInline):
    model = Reservation
    extra = 5

class FlightAdmin(admin.ModelAdmin):
    # inlines = (PassengerInline, )
    list_display = ("flight_number", "airlines", "departure_city", "arrival_city", "date", "time", "remaining_days")
    # list_editable = ("date",)
    list_filter = ("airlines", "departure_city", "arrival_city")
    ordering = ("-date","time")
    search_fields = ("departure_city", "arrival_city")
    list_per_page = 10
    date_hierarchy = "date"

    fieldsets = (
        ("Main", { "fields" : ("flight_number", "airlines")}),
        ("Places", {
            "classes": ("collapse", ), 
            "fields": ( ("departure_city", "arrival_city"),)}),
        ("Dates", {"fields": ("date", "time")})
    )

    def remaining_days(self, item):
        return (item.date - now().date()).days

class PassengerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("flight",)
    raw_id_fields = ("flight", "passenger")


# admin.site.register((Flight, Reservation, Passenger))
# admin.site.register(Flight, FlightAdmin)
admin.site.register(Flight, FlightAdmin2)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Passenger, PassengerAdmin)

admin.site.site_title = "Clarusway Fligth App"
admin.site.site_header = "Clarusway Fligth App"
admin.site.index_title = "Welcome to Admin Portal"

