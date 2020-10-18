SELECT sensorID,timestamp,sensorField1,sensorField2 
FROM sensorTable s1
WHERE timestamp = (SELECT MAX(timestamp) FROM sensorTable s2 WHERE s1.sensorID = s2.sensorID)
ORDER BY sensorID, timestamp;

SELECT timestamp, drink_sum, hookah_sum 
FROM Purchase 
ORDER BY timestamp ASC
LIMIT 5

