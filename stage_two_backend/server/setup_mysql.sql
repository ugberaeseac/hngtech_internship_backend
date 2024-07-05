reate a test database
-- This script prepares a dev database for the HNG stage-two backend project task
CREATE DATABASE IF NOT EXISTS hng_test_db;
CREATE USER IF NOT EXISTS 'hng_test'@'localhost' IDENTIFIED BY 'hng_test_pwd';
GRANT ALL PRIVILEGES ON hng_test_db.* TO 'hng_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hng_test'@'localhost';
