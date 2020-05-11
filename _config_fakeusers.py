from database.database import ApartmentsDatabase

from database.models.group import Group
from database.models.user import User
from database.models.restriction import Restriction
from database.models.subscription import Subscription

import names
import random

def main():
    db = ApartmentsDatabase()

    for i in range(200):
        group = Group()
        group = db.groups.save(group)
        db.commit()

        user = User()
        user.name = names.get_first_name()
        user.surname = names.get_last_name()
        user.isActive = True
        user.groupId = group.id
        user = db.users.save(user)
        db.commit()

        restriction = Restriction()
        restriction.minSurface = random.randrange(40, 300, 8)
        restriction.minRooms = random.randrange(1, 8, 1)
        restriction.maxPrice = random.randrange(50000, 800000, 6000)
        restriction = db.restrictions.save(restriction)
        db.commit()

        subscription = Subscription()
        subscription.userId = user.id
        subscription.labelId = random.randrange(1, 2, 1)
        subscription.cityId = random.randrange(1, 3, 1)
        subscription.isActive = True
        subscription.restrictionId = restriction.id
        subscription = db.subscriptions.save(subscription)
        db.commit()

### Main ###########################
if __name__ == "__main__":
    main()