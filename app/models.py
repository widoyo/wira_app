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
        
KAS_BANK = 'Kas A;Kas B;Bank BCA;Bank OCBC'.split(';')
KAT_BIAYA = [
    'Iklan',
    'Gaji',
    'Bahan Bakar',
    'Listrik',
    'Komunikasi'
    'Supir',
    'Tol',
    'Vendor'
]

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
    asal = pw.CharField(max_length=35)
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
    name = pw.CharField(max_length=35)
    phone = pw.CharField(max_length=35)
    kapan = pw.DateTimeField()
    num_hari = pw.IntegerField(default=1)
    lokasi_jemput = pw.TextField(default='')
    kendaraan = pw.TextField('Reborn')
    harga = pw.IntegerField() # harga jadi / setelah nego
    kota = pw.CharField(max_length=50, default='Solo')
    acara = pw.TextField(null=True)
    status = pw.CharField(max_length=12, default='aktif')
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
    pemesan = pw.ForeignKeyField(Customer)
    jemput = pw.DateTimeField()
    lokasi_jemput = pw.CharField(max_length=100)
    est_tiba = pw.DateTimeField()
    booking = pw.ForeignKeyField(Booking, null=True)
    mobil = pw.ForeignKeyField(Mobil, null=True)
    supir = pw.ForeignKeyField(Driver, null=True)
    harga = pw.IntegerField(null=True)
    tujuan = pw.TextField(null=True)
    km_berangkat = pw.IntegerField(null=True)
    km_tiba = pw.IntegerField(null=True)
    bea_supir = pw.IntegerField(null=True)
    bea_tol = pw.IntegerField(null=True)
    bea_bensin = pw.IntegerField(null=True)
    bea_lain = pw.IntegerField(null=True)
    keterangan = pw.TextField(null=True)
    upgrade = pw.BooleanField(default=False)
    created = pw.DateTimeField(default=datetime.datetime.now)
    modified = pw.DateTimeField(null=True)
    c_by = pw.CharField(max_length=12)
    m_by = pw.CharField(max_length=12, null=True)


