from database.database import ApartmentsDatabase

from database.models.group import Group
from database.models.user import User
from database.models.restriction import Restriction
from database.models.subscription import Subscription

import names
import random

def main():
    db = ApartmentsDatabase()
    
    query = """
        INSERT INTO labels (name) VALUES ('Acquisto'), ('Affitto');
    """
    db.session.execute(query)
    db.session.commit()

    query = """
        INSERT INTO cities (name) VALUES ('Bologna'), ('Modena'), ('Trani');
    """
    db.session.execute(query)
    db.session.commit()
    
    query = """
        INSERT INTO `publishers` (url, isActive, labelId, cityId) VALUES
        ('https://www.immobiliare.it/vendita-case/bologna/', 1, 1, 1),
        ('https://www.casa.it/vendita/residenziale/bologna/', 1, 1, 1),
        ('https://www.immobiliare.it/affitto-case/bologna/', 1, 2, 1),
        ('https://www.casa.it/affitto/residenziale/bologna/', 1, 2, 1),
        ('https://homepal.it/privati/vendita/case/Bologna/', 1, 1, 1),
        ('https://homepal.it/privati/affitto/case/Bologna/', 1, 2, 1),
        ('https://www.kijiji.it/case/vendita/annunci-bologna/', 1, 1, 1),
        ('https://www.kijiji.it/case/affitto/annunci-bologna/', 1, 2, 1),
        ('https://www.subito.it/annunci-emilia-romagna/vendita/appartamenti/bologna/bologna/', 1, 1, 1),
        ('https://www.subito.it/annunci-emilia-romagna/affitto/appartamenti/bologna/bologna/', 1, 2, 1),
        ('https://www.wikicasa.it/vendita-case/bologna/', 1, 1, 1),
        ('https://www.wikicasa.it/affitto-case/bologna/', 1, 2, 1),
        ('https://www.immobiliare.it/vendita-case/modena/', 1, 1, 2),
        ('https://www.casa.it/vendita/residenziale/modena/', 1, 1, 2),
        ('https://www.immobiliare.it/affitto-case/modena/', 1, 2, 2),
        ('https://www.casa.it/affitto/residenziale/modena/', 1, 2, 2),
        ('https://homepal.it/privati/vendita/case/Modena/', 1, 1, 2),
        ('https://homepal.it/privati/affitto/case/Modena/', 1, 2, 2),
        ('https://www.kijiji.it/case/vendita/annunci-modena/', 1, 1, 2),
        ('https://www.kijiji.it/case/affitto/annunci-modena/', 1, 2, 2),
        ('https://www.subito.it/annunci-emilia-romagna/vendita/appartamenti/modena/modena/', 1, 1, 2),
        ('https://www.subito.it/annunci-emilia-romagna/affitto/appartamenti/modena/modena/', 1, 2, 2),
        ('https://www.wikicasa.it/vendita-case/modena/', 1, 1, 2),
        ('https://www.wikicasa.it/affitto-case/modena/', 1, 2, 2),
        ('https://www.immobiliare.it/vendita-case/trani/', 1, 1, 3),
        ('https://www.casa.it/vendita/residenziale/trani/', 1, 1, 3),
        ('https://www.immobiliare.it/affitto-case/trani/', 1, 2, 3),
        ('https://www.casa.it/affitto/residenziale/trani/', 1, 2, 3),
        ('https://homepal.it/privati/vendita/case/Trani/', 1, 1, 3),
        ('https://homepal.it/privati/affitto/case/Trani/', 1, 2, 3),
        ('https://www.kijiji.it/case/vendita/annunci-trani/', 1, 1, 3),
        ('https://www.kijiji.it/case/affitto/annunci-trani/', 1, 2, 3),
        ('https://www.subito.it/annunci-emilia-romagna/vendita/appartamenti/trani/trani/', 1, 1, 3),
        ('https://www.subito.it/annunci-emilia-romagna/affitto/appartamenti/trani/trani/', 1, 2, 3),
        ('https://www.wikicasa.it/vendita-case/trani/', 1, 1, 3),
        ('https://www.wikicasa.it/affitto-case/trani/', 1, 2, 3);
    """
    db.session.execute(query)
    db.session.commit()

    query = """
        INSERT INTO parameters (name, value) VALUES ('MAX_LIMIT_SUBSCRIPTIONS', '100000');
    """
    db.session.execute(query)
    db.session.commit()

    db.session.close()

### Main ###########################
if __name__ == "__main__":
    main()