from django.db import models

from cities_light.models import Country, Region, SubRegion

from users.models import User

# Create your models here.

BUILDING_TYPES = [
    ('Bungalow', 'Bungalow'),
    ('Duplex', 'Duplex'),
    ('1 Story Building Apartment', '1 Story Building Apartment'),
    ('2 Story Building Apartment', '2 Story Building Apartment'),
    ('3 Story Building Apartment', '3 Story Building Apartment'),
    ('2 Story Building Apartment', '4 Story Building Apartment'),
    ('5 Story Building Apartment', '5 Story Building Apartment'),
    ('6 Story Building Apartment', '6 Story Building Apartment'),
    ('2 Story Building Plaza', '2 Story Building Plaza'),
    ('3 Story Building Plaza', '3 Story Building Plaza'),
    ('4 Story Building Plaza', '4 Story Building Plaza'),
    ('5 Story Building Plaza', '5 Story Building Plaza'),
    ('6 Story Building Plaza', '6 Story Building Plaza'),
    
]


Plaza = [
    '2 Story Building Plaza',
    '3 Story Building Plaza', 
    '4 Story Building Plaza', 
    '5 Story Building Plaza', 
    '6 Story Building Plaza', 
]


ACCOMMODATION_TYPES = [
    ('1 Room', '1 Room'),
    ('Self Contain', 'Self Contain'),
    ('A Room And Parlor', 'A Room And Parlor'),
    ('2 Bedrooms', '2 BedRooms'),
    ('3 Bedrooms', '3 BedRooms'),
    ('4 Bedrooms', '4 BedRooms'),
    ('5 Bedrooms', '5 BedRooms'),
    ('6 Bedrooms', '6 BedRooms'),
    ('Shop', 'Shop'),
    ('Office', 'Office'),
    ('Hall', 'Hall'),
    ('Mall', 'Mall'),
    ('Warehouse', 'Warehouse'),
]


FLOOR_TYPE = [
    ('Ground Floor', 'Ground Floor'),
    ('First Floor', 'First Floor'),
    ('Second Floor', 'Second Floor'),
    ('Third Floor', 'Third Floor'),
    ('Fourth Floor', 'Fourth Floor'),
    ('Fifth Floor', 'Fifth Floor'),
    ('Sixth Floor', 'Sixth Floor'),
    ('Seventh Floor', 'Seventh Floor'),
]

    # air_conditioning = models.BooleanField(default=False)
    # tv_cable = models.BooleanField(default=False)
    # refigerator = models.BooleanField(default=False)
    # wifi = models.BooleanField(default=False)
    # dryer = models.BooleanField(default=False)
    # washer = models.BooleanField(default=False)
    # microwave = models.BooleanField(default=False)
    # swimming_pool = models.BooleanField(default=False)
    # gym = models.BooleanField(default=False)
    # furnitures = models.BooleanField(default=False)
class AmenitiesModels(models.Model):
    feature = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.feature


"""
    Use a uuid for every item in the database and track the item paid for by it.
    Meaning that the flat, space and building models should have a unique id
"""

class HouseModel(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField('Building Name', max_length=100, blank=True, null=True)
    address = models.CharField('Building Address', max_length=150)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True) # default=165
    state = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True, )
    city = models.ForeignKey(SubRegion, on_delete=models.PROTECT, null=True, blank=True, )
    building_type = models.CharField('Building Type', max_length=50, choices=BUILDING_TYPES)
    accommodation_type = models.CharField('Accommodation Type', max_length=50, choices=ACCOMMODATION_TYPES)
    total_number_of_accommodation_space = models.PositiveIntegerField('Total Number Of Accodation Space')
    available_number_accommodation_space = models.PositiveIntegerField('Number Of Accodation Space Available')
    house_price = models.DecimalField('Building Price', max_digits=11, decimal_places=2, null=True, blank=True)
    electricity = models.BooleanField(default=True)
    water = models.BooleanField(default=False)
    newly_built = models.BooleanField('Newly Built', default=False)
    sale = models.BooleanField('For Sale', default=False)
    exterior_image = models.ImageField('Exterior Image Main', upload_to='BuildingExterior/', blank=True, null=True)
    exterior_image_side1 = models.ImageField('Exterior Image Side A', upload_to='BuildingExterior/', blank=True, null=True)
    exterior_image_side2 = models.ImageField('Exterior Image Side B', upload_to='BuildingExterior/', blank=True, null=True)
    vid_file = models.FileField(upload_to="BuildingInterior/video/building/", blank=True, null=True)
    c_of_o = models.FileField('Certificate Of Occupancy', upload_to="doucments/CofOs/", null=True, blank=True)
    d_of_a = models.FileField('Deed Of Assignment', upload_to="doucments/DofAs/", null=True, blank=True)
    tenant_agreement = models.FileField('Tenant Agreement', upload_to="doucments/TAs/", null=True, blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    verified = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    features = models.ManyToManyField(AmenitiesModels,  help_text='You can select more than one by hold the Ctrl key')
    
    def __str__(self):
        return self.name + ' - ' + self.address
    
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.building_type + ' located at ' + self.address
        super().save(*args, **kwargs)
       
    def get_image(self):
        return self.image.url


class FlatModel(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, related_name="flats", null=True)
    floor = models.CharField(max_length=50, choices=FLOOR_TYPE)
    side = models.CharField(max_length=50, choices=[('Right', 'Right'), ('Left', 'Left')])
    taken = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accommodation_type = models.CharField('Accommodation Type', max_length=50, choices=ACCOMMODATION_TYPES)
    description = models.TextField('Description', max_length=600, blank=True, null=True)
    bedroom = models.ImageField(upload_to="BuildingInterior/bedroom")
    bedroom_master = models.ImageField(upload_to="BuildingInterior/bedroom")
    kitchen = models.ImageField(upload_to="BuildingInterior/kitchen")
    sittingroom = models.ImageField(upload_to="BuildingInterior/livingroom")
    convience = models.ImageField(upload_to="BuildingInterior/convience")
    vid_file = models.FileField(upload_to="BuildingInterior/video/flat")
    features = models.ManyToManyField(AmenitiesModels, help_text='You can select more than one by hold the Ctrl key')
        
    def __str__(self):
        return self.floor + " " + self.side
    

class SpaceModel(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, related_name='space')
    floor = models.CharField(max_length=50, choices=FLOOR_TYPE)
    side = models.CharField(max_length=50, choices=[('right', 'Right'), ('left', 'Left')])
    spacename = models.CharField(max_length=50)
    taken = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accommodation_type = models.CharField('Accommodation Type', max_length=50, choices=ACCOMMODATION_TYPES, null=True, blank=True)
    image = models.ImageField(upload_to="BuildingInterior/space", null=True, blank=True)
    features = models.ManyToManyField(AmenitiesModels, help_text='You can select more than one by hold the Ctrl key')
    
    def __str__(self):
        return self.floor + ' ' + self.spacename
    
    def save(self, *args, **kwargs):
        b_typ = self.house.building_type
        print(b_typ)
        if b_typ in Plaza:
           super().save(*args, **kwargs)
        else:
            raise ValueError('This Building Cann\'t Accept Spaces Try Flat')
        
        
        
