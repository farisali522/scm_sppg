from django.contrib import admin
from .models import BahanBaku

@admin.register(BahanBaku)
class BahanBakuAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama', 'satuan', 'stok', 'harga_satuan')
    search_fields = ('kode', 'nama')
    list_filter = ('satuan',)
