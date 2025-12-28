from django.db import models

class BahanBaku(models.Model):
    kode = models.CharField(max_length=20, unique=True, verbose_name="Kode Bahan")
    nama = models.CharField(max_length=100, verbose_name="Nama Bahan")
    satuan = models.CharField(max_length=20, verbose_name="Satuan (kg, ltr, dll)")
    stok = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stok")
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Harga Satuan")

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    class Meta:
        verbose_name = "Bahan Baku"
        verbose_name_plural = "Daftar Bahan Baku"
