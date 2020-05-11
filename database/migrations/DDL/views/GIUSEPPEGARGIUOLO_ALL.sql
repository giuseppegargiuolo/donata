DROP VIEW GIUSEPPEGARGIUOLO_ALL;
CREATE VIEW GIUSEPPEGARGIUOLO_ALL AS
	SELECT m.createdAt AS matchesAt, a.*
    FROM apartments a 
    INNER JOIN matches m ON a.id = m.apartmentId
    INNER JOIN subscriptions s ON s.id = m.subscriptionId
    INNER JOIN users u ON s.userId = u.id
    WHERE u.name = 'Giuseppe Gargiuolo';