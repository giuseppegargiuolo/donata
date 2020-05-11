DROP VIEW GIUSEPPEGARGIUOLO_VALID;
CREATE VIEW GIUSEPPEGARGIUOLO_VALID AS
	SELECT m.createdAt AS matchesAt, a.*
    FROM apartments a 
    INNER JOIN matches m ON a.id = m.apartmentId
    INNER JOIN subscriptions s ON s.id = m.subscriptionId
    INNER JOIN users u ON s.userId = u.id
    WHERE u.name = 'Giuseppe Gargiuolo'
	AND a.runId >= (SELECT MAX(id) from runs where id < (SELECT MAX(id) FROM runs WHERE finishedAt IS NULL));