INSERT INTO apartments_dev.users (id, name, telegram)
SELECT id, name, telegram
FROM apartments.users;

-- labels
INSERT INTO apartments_dev.labels (name) VALUES ('VENDITA');
INSERT INTO apartments_dev.labels (name) VALUES ('AFFITTO');

-- publishers
INSERT INTO publishers (url, isActive, labelId) VALUES ('https://www.immobiliare.it/vendita-appartamenti/bologna/', 1, 1);
INSERT INTO publishers (url, isActive, labelId) VALUES ('https://www.casa.it/vendita/residenziale/bologna/', 1, 1);
INSERT INTO publishers (url, isActive, labelId) VALUES ('https://www.immobiliare.it/affitto-appartamenti/bologna/', 1, 2);
INSERT INTO publishers (url, isActive, labelId) VALUES ('https://www.casa.it/affitto/residenziale/bologna/', 1, 2);

-- restrictions
INSERT INTO apartments_dev.restrictions (id, maxPrice, minRooms, minSurface)
SELECT id, maxPrice, minRooms, minSurface
FROM apartments.restrictions;

-- 
INSERT INTO apartments_dev.subscriptions (restrictionId, labelId, userId) VALUES (1, 1, 1); -- giuseppe
INSERT INTO apartments_dev.subscriptions (restrictionId, labelId, userId) VALUES (2, 2, 2); -- lorenzo
INSERT INTO apartments_dev.subscriptions (restrictionId, labelId, userId) VALUES (2, 1, 3); -- simona

-- runs
INSERT INTO apartments_dev.runs (id, startedAt, finishedAt)
SELECT id, startedAt, finishedAt
FROM apartments.runs;

-- apartments
INSERT INTO apartments_dev.apartments (id, price, refNo, rooms, runId, title, subtitle, surface, url)
SELECT id, price, refNo, rooms, runId, title, subtitle, surface, url
FROM apartments.apartments;

-- matches
INSERT INTO apartments_dev.matches (apartmentId, id, runId, subscriptionId)
SELECT apartmentId, id, runId, (SELECT MAX(s.id) FROM subscriptions s INNER JOIN users u ON u.id = s.userId)
FROM apartments.matches;