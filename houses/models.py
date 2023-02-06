from django.db import models

from cities_light.models import Country, Region, SubRegion

from users.models import User

# Create your models here.

BUILDING_TYPES = [
    ('Bungalow', 'Bungalow'),
    ('duplex', 'Duplex'),
    ('1-story', '1 Story Building'),
    ('2-story-building', '2 Story Building'),
    ('3-story-building', '3 Story Building'),
    ('4-story-building', '4 Story Building'),
    ('5-story-building', '5 Story Building'),
    ('6-story-building', '6 Story Building'),
    ('2-story-building-plaza', '2 Story Building Plaza'),
    ('3-story-building-plaza', '3 Story Building Plaza'),
    ('4-story-building-plaza', '4 Story Building Plaza'),
    ('5-story-building-plaza', '5 Story Building Plaza'),
    ('6-story-building-plaza', '6 Story Building Plaza'),
    
]


Plaza = [
    ('2-story-building-plaza', '2 Story Building Plaza'),
    ('3-story-building-plaza', '3 Story Building Plaza'),
    ('4-story-building-plaza', '4 Story Building Plaza'),
    ('5-story-building-plaza', '5 Story Building Plaza'),
    ('6-story-building-plaza', '6 Story Building Plaza'),
]

ACCOMMODATION_TYPES = [
    ('self_con', 'Self Contain'),
    ('a room_parlor', 'A Room And Parlor'),
    ('2-rooms-flat', '2 BedRooms Flat'),
    ('3-rooms-flat', '3 BedRooms Flat'),
    ('1-room', '1 Room'),
    ('shop', 'Shop'),
    ('hall', 'Hall'),
    ('mall', 'Mall'),
    ('warehouse', 'Warehouse'),
]

FLOOR_TYPE = [
    ('ground-floor', 'Ground Floor'),
    ('first-floor', 'First Floor'),
    ('second-floor', 'Second Floor'),
    ('third-floor', 'Third Floor'),
    ('fourth-floor', 'Fourth Floor'),
    ('fifth-floor', 'Fifth Floor'),
    ('sixth-floor', 'Sixth Floor'),
    ('seven-floor', 'Seventh Floor'),
]

    
class HouseModel(models.Model):
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
    exterior_image = models.ImageField('Exterior Image', upload_to='BuildingExterior/', blank=True, null=True)
    c_of_o = models.FileField('Certificate Of Occupancy', upload_to="doucments/CofOs/", null=True, blank=True)
    d_of_a = models.FileField('Deed Of Assignment', upload_to="doucments/DofAs/", null=True, blank=True)
    tenant_agreement = models.FileField('Tenant Agreement', upload_to="doucments/TAs/", null=True, blank=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.name + ' - ' + self.address
    
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.building_type + ' located at ' + self.address
        super().save(*args, **kwargs)
       
    def get_image(self):
        return self.image.url


class FlatModel(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, related_name="flats", null=True, blank=True)
    floor = models.CharField(max_length=50, choices=FLOOR_TYPE)
    side = models.CharField(max_length=50, choices=[('right', 'Right'), ('left', 'Left')])
    taken = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accommodation_type = models.CharField('Accommodation Type', max_length=50, choices=ACCOMMODATION_TYPES)
    bedroom = models.ImageField(upload_to="BuildingInterior/bedroom")
    kitchen = models.ImageField(upload_to="BuildingInterior/kitchen")
    sittingroom = models.ImageField(upload_to="BuildingInterior/livingroom")
    convience = models.ImageField(upload_to="BuildingInterior/convience")
    
    def __str__(self):
        return self.floor + " " + self.side
    



class SpaceModel(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE)
    floor = models.CharField(max_length=50, choices=FLOOR_TYPE)
    spacename = models.CharField(max_length=50)
    taken = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    accommodation_type = models.CharField('Accommodation Type', max_length=50, choices=ACCOMMODATION_TYPES, null=True, blank=True)
    image = models.ImageField(upload_to="BuildingInterior/space", null=True, blank=True)
    
    def __str__(self):
        return self.floor + ' ' + self.spacename
    
    
    def save(self, *args, **kwargs):
        b_typ = self.house.building_type
        if b_typ not in Plaza:
            raise ValueError('This Building Can Accept Spaces Try Flat')
        else:
            super().save(*args, **kwargs)