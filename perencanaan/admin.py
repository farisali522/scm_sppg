from django.contrib import admin
from .models import (
    BahanBaku, KandunganGizi, StandarGizi, 
    Resep, BahanResep, KonversiSatuan, 
    RencanaMenu, RencanaMenuDetail
)

# =============================================================================
# 1. BAHAN BAKU & NUTRISI (INLINES)
# =============================================================================

class KonversiSatuanInline(admin.TabularInline):
    model = KonversiSatuan
    extra = 1
    # Karena 1-to-1, kita batasi agar tidak bisa tambah banyak jika sudah ada
    max_num = 1 

class KandunganGiziInline(admin.StackedInline):
    model = KandunganGizi
    can_delete = False
    verbose_name_plural = 'Kandungan Gizi'

@admin.register(BahanBaku)
class BahanBakuAdmin(admin.ModelAdmin):
    list_display = ('kode_bahan', 'nama_bahan', 'kategori', 'satuan_dasar', 'estimasi_harga', 'masa_simpan')
    search_fields = ('kode_bahan', 'nama_bahan')
    list_filter = ('kategori', 'satuan_dasar', 'masa_simpan')
    inlines = (KonversiSatuanInline, KandunganGiziInline)


# =============================================================================
# 2. STANDAR GIZI (TARGET AKG)
# =============================================================================

@admin.register(StandarGizi)
class StandarGiziAdmin(admin.ModelAdmin):
    list_display = (
        'kelompok_sasaran', 'waktu_makan', 'rujukan_akg',
        'display_energi', 'display_protein', 'display_lemak', 'display_karbo', 
        'pagu_belanja'
    )
    search_fields = ('kelompok_sasaran',)
    list_filter = ('waktu_makan',)

    def display_energi(self, obj):
        return f"{obj.energi_min} - {obj.energi_max}"
    display_energi.short_description = 'Energi (Kkal)'

    def display_protein(self, obj):
        return f"{obj.protein_min} - {obj.protein_max}"
    display_protein.short_description = 'Protein (g)'

    def display_lemak(self, obj):
        return f"{obj.lemak_min} - {obj.lemak_max}"
    display_lemak.short_description = 'Lemak (g)'

    def display_karbo(self, obj):
        return f"{obj.karbo_min} - {obj.karbo_max}"
    display_karbo.short_description = 'Karbo (g)'


# =============================================================================
# 3. RESEP & KOMPOSISI
# =============================================================================

class BahanResepInline(admin.TabularInline):
    model = BahanResep
    fields = ['bahan_baku', 'satuan_konversi', 'jumlah_satuan', 'berat_gram']
    extra = 1
    autocomplete_fields = ['bahan_baku']

@admin.register(Resep)
class ResepAdmin(admin.ModelAdmin):
    list_display = ('nama_masakan', 'kategori_masakan', 'display_energi', 'display_protein', 'display_lemak', 'display_karbo')
    search_fields = ('nama_masakan',)
    list_filter = ('kategori_masakan',)
    inlines = [BahanResepInline]

    def display_energi(self, obj):
        return f"{obj.total_energi:.2f} Kkal"
    display_energi.short_description = 'Energi'

    def display_protein(self, obj):
        return f"{obj.total_protein:.2f} g"
    display_protein.short_description = 'Protein'

    def display_lemak(self, obj):
        return f"{obj.total_lemak:.2f} g"
    display_lemak.short_description = 'Lemak'

    def display_karbo(self, obj):
        return f"{obj.total_karbohidrat:.2f} g"
    display_karbo.short_description = 'Karbo'


# =============================================================================
# 4. RENCANA MENU (HEADER-DETAIL)
# =============================================================================

class RencanaMenuDetailInline(admin.TabularInline):
    model = RencanaMenuDetail
    extra = 5
    autocomplete_fields = ['resep']

@admin.register(RencanaMenu)
class RencanaMenuAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'standar_gizi', 'get_total_energi', 'get_total_protein')
    list_filter = ('tanggal', 'standar_gizi')
    search_fields = ('tanggal',)
    date_hierarchy = 'tanggal'
    inlines = [RencanaMenuDetailInline]

    def get_total_energi(self, obj):
        return f"{obj.total_energi:.2f} Kkal"
    get_total_energi.short_description = 'Energi porsi'

    def get_total_protein(self, obj):
        return f"{obj.total_protein:.2f} g"
    get_total_protein.short_description = 'Protein porsi'