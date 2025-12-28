from django.db import models

# =============================================================================
# 1. BAHAN BAKU & NUTRISI (FONDASI)
# =============================================================================

class BahanBaku(models.Model):
    KATEGORI_CHOICES = [
        ('karbohidrat', 'Sumber Karbohidrat'),
        ('hewan', 'Protein Hewani'),
        ('nabati', 'Protein Nabati'),
        ('sayur', 'Sayur'),
        ('buah', 'Buah'),
        ('lemak', 'Sumber Lemak'),
        ('susu', 'Susu'),
        ('bumbu', 'Bumbu & Pelengkap'),
    ]

    SATUAN_CHOICES = [
        ('gr', 'Gram (g)'),
        ('kg', 'Kilogram (kg)'),
        ('ml', 'Mililiter (ml)'),
        ('liter', 'Liter (l)'),
        ('pcs', 'Pcs/Buah'),
        ('ikat', 'Ikat'),
        ('butir', 'Butir'),
        ('pack', 'Pack/Bungkus'),
        ('sisir', 'Sisir'),
    ]

    kode_bahan = models.CharField(max_length=20, unique=True, verbose_name="Kode Bahan")
    nama_bahan = models.CharField(max_length=100, verbose_name="Nama Bahan")
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, verbose_name="Kategori")
    satuan_dasar = models.CharField(max_length=20, choices=SATUAN_CHOICES, default='gr', verbose_name="Satuan Dasar")
    estimasi_harga = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Estimasi Harga")
    masa_simpan = models.IntegerField(default=0, verbose_name="Masa Simpan (Hari)")

    def __str__(self):
        return f"[{self.kode_bahan}] {self.nama_bahan}"

    class Meta:
        verbose_name = "Bahan Baku"
        verbose_name_plural = "Daftar Bahan Baku"


class KandunganGizi(models.Model):
    bahan_baku = models.OneToOneField(
        BahanBaku, 
        on_delete=models.CASCADE, 
        related_name='kandungan_gizi', 
        verbose_name="Bahan Baku"
    )
    energi = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Energi (Kkal)")
    protein = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Protein (g)")
    lemak = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Lemak (g)")
    karbohidrat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Karbohidrat (g)")
    persen_bdd = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Berat Dapat Dimakan (%)")

    def __str__(self):
        return f"Gizi - {self.bahan_baku.nama_bahan}"

    class Meta:
        verbose_name = "Kandungan Gizi"
        verbose_name_plural = "Daftar Kandungan Gizi"


class KonversiSatuan(models.Model):
    bahan_baku = models.ForeignKey(
        BahanBaku, 
        on_delete=models.CASCADE, 
        related_name='konversi_satuan', 
        verbose_name="Bahan Baku"
    )
    nama_satuan = models.CharField(max_length=50, verbose_name="Nama Satuan (Ikat/Pcs/Butir)")
    nilai_gram = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Nilai Gram per Satuan")

    def __str__(self):
        return f"{self.nama_satuan} ({self.nilai_gram}g) - {self.bahan_baku.nama_bahan}"

    class Meta:
        verbose_name = "Konversi Satuan"
        verbose_name_plural = "Daftar Konversi Satuan"


# =============================================================================
# 2. STANDAR GIZI (TARGET AKG)
# =============================================================================

class StandarGizi(models.Model):
    WAKTU_MAKAN_CHOICES = [
        ('pagi', 'Makan Pagi'),
        ('siang', 'Makan Siang'),
        ('kudapan', 'Makanan Tambahan/Kudapan'),
    ]

    kelompok_sasaran = models.CharField(max_length=100, verbose_name="Kelompok Sasaran")
    waktu_makan = models.CharField(max_length=50, choices=WAKTU_MAKAN_CHOICES, verbose_name="Waktu Makan")
    pagu_belanja = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Pagu Belanja Per-Porsi (Rp)")
    rujukan_akg = models.CharField(max_length=100, verbose_name="Rujukan AKG (%)")

    # Range Nutrisi (Target untuk Genetic Algorithm)
    energi_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Energi Minimal (Kkal)")
    energi_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Energi Maksimal (Kkal)")
    protein_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Protein Minimal (g)")
    protein_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Protein Maksimal (g)")
    lemak_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Lemak Minimal (g)")
    lemak_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Lemak Maksimal (g)")
    karbo_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Karbohidrat Minimal (g)")
    karbo_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Karbohidrat Maksimal (g)")

    def __str__(self):
        return f"{self.kelompok_sasaran} - {self.get_waktu_makan_display()}"

    class Meta:
        verbose_name = "Standar Gizi & Biaya"
        verbose_name_plural = "Standar Gizi & Biaya"
        unique_together = ['kelompok_sasaran', 'waktu_makan']


# =============================================================================
# 3. RESEP & KOMPOSISI BAHAN
# =============================================================================

class Resep(models.Model):
    KATEGORI_RESEP_CHOICES = [
        ('karbohidrat', 'Sumber Karbohidrat'),
        ('hewan', 'Protein Hewani'),
        ('nabati', 'Protein Nabati'),
        ('sayur', 'Sayur'),
        ('buah', 'Buah'),
        ('susu', 'Susu'),
    ]

    nama_masakan = models.CharField(max_length=100, verbose_name="Nama Masakan")
    kategori_masakan = models.CharField(
        max_length=50, 
        choices=KATEGORI_RESEP_CHOICES, 
        verbose_name="Kategori Masakan"
    )

    def __str__(self):
        return f"{self.nama_masakan} ({self.get_kategori_masakan_display()})"

    # --- PERHITUNGAN TOTAL GIZI OTOMATIS ---
    @property
    def total_energi(self):
        return sum(
            (item.get_berat_bersih() / 100) * item.bahan_baku.kandungan_gizi.energi 
            for item in self.komposisi.all() if hasattr(item.bahan_baku, 'kandungan_gizi')
        )

    @property
    def total_protein(self):
        return sum(
            (item.get_berat_bersih() / 100) * item.bahan_baku.kandungan_gizi.protein 
            for item in self.komposisi.all() if hasattr(item.bahan_baku, 'kandungan_gizi')
        )

    @property
    def total_lemak(self):
        return sum(
            (item.get_berat_bersih() / 100) * item.bahan_baku.kandungan_gizi.lemak 
            for item in self.komposisi.all() if hasattr(item.bahan_baku, 'kandungan_gizi')
        )

    @property
    def total_karbohidrat(self):
        return sum(
            (item.get_berat_bersih() / 100) * item.bahan_baku.kandungan_gizi.karbohidrat 
            for item in self.komposisi.all() if hasattr(item.bahan_baku, 'kandungan_gizi')
        )

    class Meta:
        verbose_name = "Resep Masakan"
        verbose_name_plural = "Daftar Resep Masakan"


class BahanResep(models.Model):
    resep = models.ForeignKey(
        Resep, 
        on_delete=models.CASCADE, 
        related_name='komposisi', 
        verbose_name="Resep"
    )
    bahan_baku = models.ForeignKey(
        BahanBaku, 
        on_delete=models.CASCADE, 
        verbose_name="Bahan Baku"
    )
    
    # Input Manual atau via Konversi
    berat_gram = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Berat Bersih (gr)"
    )
    
    # Kamus Konversi
    satuan_konversi = models.ForeignKey(
        KonversiSatuan, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Satuan Konversi"
    )
    jumlah_satuan = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Jumlah Satuan"
    )

    def get_berat_bersih(self):
        """Logic pengambilan berat akhir (Gram)"""
        if self.berat_gram:
            return self.berat_gram
        if self.satuan_konversi and self.jumlah_satuan:
            return self.jumlah_satuan * self.satuan_konversi.nilai_gram
        return 0

    def save(self, *args, **kwargs):
        """Otomatis hitung berat_gram jika input pakai satuan konversi"""
        if self.satuan_konversi and self.jumlah_satuan:
            self.berat_gram = self.jumlah_satuan * self.satuan_konversi.nilai_gram
        # Jika kolom konversi dihapus, berat_gram tetap manual atau 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bahan_baku.nama_bahan} ({self.berat_gram or 0}g)"

    class Meta:
        verbose_name = "Komposisi Bahan"
        verbose_name_plural = "Komposisi Bahan"


# =============================================================================
# 4. RENCANA MENU (HEADER-DETAIL)
# =============================================================================

class RencanaMenu(models.Model):
    tanggal = models.DateField(verbose_name="Tanggal Penyajian")
    standar_gizi = models.ForeignKey(
        StandarGizi, 
        on_delete=models.CASCADE, 
        verbose_name="Sasaran & Waktu Makan"
    )

    def __str__(self):
        return f"{self.tanggal} | {self.standar_gizi}"

    @property
    def total_energi(self):
        return sum(item.resep.total_energi for item in self.items.all())

    @property
    def total_protein(self):
        return sum(item.resep.total_protein for item in self.items.all())

    @property
    def total_lemak(self):
        return sum(item.resep.total_lemak for item in self.items.all())

    @property
    def total_karbohidrat(self):
        return sum(item.resep.total_karbohidrat for item in self.items.all())

    class Meta:
        verbose_name = "Rencana Menu Harian"
        verbose_name_plural = "Daftar Rencana Menu Harian"
        unique_together = ['tanggal', 'standar_gizi']


class RencanaMenuDetail(models.Model):
    rencana_menu = models.ForeignKey(
        RencanaMenu, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Rencana Menu"
    )
    resep = models.ForeignKey(
        Resep, 
        on_delete=models.CASCADE, 
        verbose_name="Nama Masakan"
    )

    def __str__(self):
        return self.resep.nama_masakan

    class Meta:
        verbose_name = "Isi Menu/Resep"
        verbose_name_plural = "Isi Menu/Resep"
