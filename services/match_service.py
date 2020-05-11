from core.services.service import Service

class MatchService(Service):

    def getPendingMatches(self):
        return self.db.matches.pendingMatches()

    def setNotified(self, match, flag):
        match.isNotified = flag
        self.db.matches.save(match)
        self.db.commit()

    def lock(self, batch, flag):
        batch.isLocked = flag
        self.db.batches.save(batch)
        self.db.commit()

    def updateBatch(self, batch):
        batch.isProcessed = True
        batch.isLocked = False
        self.db.batches.save(batch)
        self.db.commit()