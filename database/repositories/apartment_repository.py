from core.database.repository import Repository
from database.models.apartment import Apartment

class ApartmentRepository(Repository):

    def exists(self, entity, fieldName):
        if fieldName == 'refNo':
            apartment = self.session.query(Apartment).filter(Apartment.refNo == entity.refNo).first()
        if fieldName == 'url':
            apartment = self.session.query(Apartment).filter(Apartment.url == entity.url).first()

        return apartment is not None

    def all(self):
        return self.session.query(Apartment).all()

    def placeMatches(self, apartment, run, batchId):
        try:
            conditions = """"""
            if apartment.rooms is not None:
                conditions += """ AND (COALESCE(r.minRooms, 0) <= """ + str(apartment.rooms) + """ AND COALESCE(r.maxRooms, 9999) >= """ + str(apartment.rooms) + """)"""

            if apartment.surface is not None:
                conditions += """ AND (COALESCE(r.minSurface, 0) <= """ + str(apartment.surface) + """ AND COALESCE(r.maxSurface, 9999) >= """ + str(apartment.surface) + """)"""

            if apartment.price is not None:
                conditions += """ AND (COALESCE(r.minPrice, 0) <= """ + str(apartment.price) + """ AND COALESCE(r.maxPrice, 999999) >= """ + str(apartment.price) + """)"""

            query = """
            INSERT INTO matches (runId, subscriptionId, apartmentId, isNotified, batchId)
            SELECT """ + str(run.id) + """, s.id, '""" + str(apartment.id) + """', false, '""" + str(batchId) + """'
            FROM users u
            INNER JOIN subscriptions s ON u.id = s.userId
            INNER JOIN restrictions r ON s.restrictionId = r.id
            WHERE 1 = 1
            """ + conditions + """
            ON DUPLICATE KEY
            UPDATE 
            runId = """ + str(run.id) + """, subscriptionId = s.id, isNotified = false, batchId = '""" + batchId + """'"""

            self.session.execute(query)
            self.session.commit()
        except:
            self.session.rollback()
            self.placeMatches(apartment, run, batchId)