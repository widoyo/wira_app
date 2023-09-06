import datetime
import peewee as pw
from bcrypt import checkpw, hashpw, gensalt
from playhouse.flask_utils import FlaskDB
from playhouse.shortcuts import model_to_dict
from flask_login import UserMixin

DATABASE = 'sqlite://myshipping.db'

db_wrapper = FlaskDB()

class BaseModel(db_wrapper.Model):
    pass
        
KAS_BANK = '111 Kas A;112 Kas B;115 Bank BCA;116 Bank OCBC'.split(';')
'''
COA:
  1 Aktiva
  111 Kas A
  112 Kas B
  115 Bank BCA
  116 Bank OCBC
  2 Kewajiban
  201 Utang Usaha
  3 Ekuitas / Modal
  301 Modal
  302 Prive
  4 Pendapatan
  401 Hasil Sewa
  402 Lain-lain
  5 Biaya
  501 Gaji
  502 Honor
  503 Bahan Bakar
  504 Listrik
  505 Iklan
  506 Sopir
  507 Vendor 
'''
KAT_BIAYA = [
    '505 Iklan',
    '501 Gaji',
    '503 Bahan Bakar',
    '504 Listrik',
    '505 Komunikasi'
    '506 Supir',
    '508 Tol',
    '507 Vendor'
]
JASA_CHOICES = 'DropOff;6 jam;12 jam;24 jam'.split(';')

class User(UserMixin, BaseModel):
    '''User Authentication'''
    username = pw.CharField(unique=True)
    password = pw.TextField()
    role = pw.CharField(max_length=1, default='0')
    is_active = pw.BooleanField(default=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)

    def check_password(self, password):
        return checkpw(password.encode(), self.password.encode())
    
    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt())
    
    
class Driver(BaseModel):
    name = pw.CharField(max_length=35, unique=True)
    phone = pw.CharField(max_length=35, null=True)
    ktp = pw.CharField(max_length=35, null=True)
    addr1 = pw.TextField(null=True)
    addr2 = pw.TextField(null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    

class Customer(BaseModel):
    '''Custimer who ship goods'''
    name = pw.CharField(max_length=35, unique=True)
    phone = pw.CharField(max_length=35, null=True)
    addr1 = pw.TextField(null=True)
    addr2 = pw.TextField(null=True)
    city = pw.CharField(max_length=50, null=True)
    zip = pw.CharField(max_length=5, null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    
    def to_dict(self):
        data = model_to_dict(self)
        data.pop('created')
        data.pop('modified')
        return data
    
class Jurnal(BaseModel):
    tanggal = pw.DateField()
    keterangan = pw.TextField()
    sumber = pw.CharField(max_length=35)
    tujuan = pw.CharField(max_length=35)
    nilai = pw.IntegerField()
    is_masuk = pw.BooleanField(default=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    

class Kas(BaseModel):
    name = pw.CharField(max_length=35, unique=True)
    saldo = pw.IntegerField()
    tanggal = pw.DateTimeField()
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
        

class Booking(BaseModel):
    pemesan = pw.ForeignKeyField(Customer)
    waktu_jemput = pw.DateTimeField()
    lokasi_jemput = pw.TextField(default='')
    kota = pw.CharField(max_length=50, default='Solo')
    num_hari = pw.IntegerField(default=1)
    kendaraan = pw.TextField('Reborn')
    harga = pw.IntegerField() # harga jadi / setelah nego
    status = pw.CharField(max_length=12, default='aktif')
    jasa = pw.CharField(max_length=50, null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    
    
class Vendor(BaseModel):
    '''Vendor Vehicle'''
    name = pw.CharField(max_length=35, unique=True)
    address = pw.TextField(null=True)
    pic_name = pw.CharField(max_length=35, null=True)
    pic_hp = pw.CharField(max_length=20, null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)


class Mobil(BaseModel):
    nopol = pw.CharField(unique=True)
    merk = pw.CharField()
    model = pw.CharField()
    vin = pw.CharField(max_length=50, null=True)
    warna = pw.CharField(max_length=35, null=True)
    akhir_stnk = pw.CharField(null=True)
    vendor = pw.ForeignKeyField(Vendor, null=True)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    
class Sewa(BaseModel):
    booking = pw.ForeignKeyField(Booking, null=True)
    waktu_jemput = pw.DateTimeField()
    lokasi_jemput = pw.CharField(max_length=100)
    kota = pw.CharField(max_length=50, null=True)
    jasa = pw.CharField(max_length=50, null=True)
    num_hari = pw.IntegerField(default=1)
    est_tiba = pw.DateTimeField(null=True)
    act_tiba = pw.DateTimeField(null=True)
    mobil = pw.ForeignKeyField(Mobil, null=True)
    driver = pw.ForeignKeyField(Driver, null=True)
    harga = pw.IntegerField(null=True)
    km_berangkat = pw.IntegerField(null=True)
    km_tiba = pw.IntegerField(null=True)
    bea_supir = pw.IntegerField(null=True)
    bea_tol = pw.IntegerField(null=True)
    bea_bensin = pw.IntegerField(null=True)
    bea_lain = pw.IntegerField(null=True)
    acara = pw.TextField(null=True)
    upgrade = pw.BooleanField(default=False)
    keterangan = pw.TextField(null=True)
    upgrade = pw.BooleanField(default=False)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    
    @property
    def is_lunas(self):
        return sum([b.nilai for b in self.bayaransewa_set]) == self.harga


class BayaranSewa(BaseModel):
    sewa = pw.ForeignKeyField(Sewa)
    tanggal = pw.DateField()
    nilai = pw.IntegerField(default=0)
    is_journaled = pw.BooleanField(default=False)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)
    