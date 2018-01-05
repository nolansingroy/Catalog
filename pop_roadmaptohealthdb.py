from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Organ, Medicine

engine = create_engine('sqlite:///roadmaptohealthwithusers.db')

Base.metadata.bind = engine

# create instance to establish communication to database
DBSession = sessionmaker(bind=engine)

# create session from instance
session = DBSession()


# Medicine for Digestive System
organ1 = Organ(name="Digestive System", user_id='1')
session.add(organ1)
session.commit()

medicine2 = Medicine(name='BPC-157', description='Healing peptide',
                     type='Peptide', gland='intestines', user_id='1', organ=organ1)
session.add(medicine2)
session.commit()

# Medicine3


# Medicine 4


# Medicine for Vascular System
# blood is circulated via heart, arteries, and veins delivering oxygen

organ1 = Organ(name="Vascular System", user_id='1')

session.add(organ1)
session.commit()

medicine1 = Medicine(name='Methylene Blue', description='commonly sold as blue dye, favorable electron donor, improves oxygen circulation',
                     type='Supplement', gland='arteries', user_id='1', organ=organ1)

session.add(medicine1)
session.commit()

# medicine2
medicine2 = Medicine(name='L-citrulline', description='amino-acid that acts on the Nitric Oxide System, will increase blood flow!',
                     type='Supplement', gland='arteries', user_id='1', organ=organ1)

session.add(medicine2)
session.commit()

# medicine3
medicine3 = Medicine(name='Burdock Root', description='purifies the blood, also aids in phase 2 liver detox!',
                     type='Traditional Chinese Medicine', gland='arteries', user_id='1', organ=organ1)
session.add(medicine3)
session.commit()

print "added Organ and Medicine"
