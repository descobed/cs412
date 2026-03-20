from pathlib import Path

from django.db import models

# Create your models here.


class Voter(models.Model):
    """voters of Newton, model"""
    
    last_name = models.TextField()
    first_name = models.TextField()
    
    residential_address_street_number = models.TextField()
    residential_address_street_name = models.TextField()
    residential_address_apartment_number = models.TextField()
    residential_address_zip_code = models.TextField()

    dob = models.DateField()
    dor = models.DateField()

    party_affiliation = models.CharField(max_length=2)
    precinct_num = models.IntegerField()

    v20state = models.TextField()
    v21city = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    '''Loads data from CSV file'''

    Voter.objects.all().delete() 

    filename = '/mnt/c/Users/diego/django/newton_voters.csv'
    

    f = open(filename, 'r')
    f.readline() 

    for line in f:
        fields = line.split(',')
        
        try:
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                residential_address_street_number=fields[3],
                residential_address_street_name=fields[4],
                residential_address_apartment_number=fields[5],
                residential_address_zip_code=fields[6],
                dob=fields[7],
                dor=fields[8],
                party_affiliation=fields[9],
                precinct_num=fields[10],
                v20state=fields[11],
                v21city=fields[12],
                v21primary=fields[13],
                v22general=fields[14],
                v23town=fields[15],
                voter_score=fields[16]
            )
            voter.save()
            print(f"Created voter: {voter}")
        
        except:
            print(f"Error processing line: {line}")
            
    print(f"Done; Created {len(Voter.objects.all())} voters")