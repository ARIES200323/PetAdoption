-- Pet Adoption Database Setup
-- This file creates the database, tables, relationships, and seed data

-- Create the database
CREATE DATABASE IF NOT EXISTS pet_adoption_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pet_adoption_db;

-- Create pet table
CREATE TABLE adoption_pet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100),
    age INT UNSIGNED NOT NULL,
    description LONGTEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create adoption_request table
CREATE TABLE adoption_adoptionrequest (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    adopter_name VARCHAR(100) NOT NULL,
    adopter_email VARCHAR(254) NOT NULL,
    request_date DATETIME(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES adoption_pet(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_pet_status ON adoption_pet(status);
CREATE INDEX idx_pet_species ON adoption_pet(species);
CREATE INDEX idx_adoption_request_pet_id ON adoption_adoptionrequest(pet_id);
CREATE INDEX idx_adoption_request_date ON adoption_adoptionrequest(request_date);

-- Insert sample seed data
INSERT INTO adoption_pet (name, species, breed, age, description, status, image) VALUES
('Buddy', 'Dog', 'Golden Retriever', 3, 'Friendly and energetic golden retriever looking for a loving home.', 'available', 'https://example.com/images/buddy.jpg'),
('Whiskers', 'Cat', 'Siamese', 2, 'Elegant Siamese cat with beautiful blue eyes.', 'available', 'https://example.com/images/whiskers.jpg'),
('Max', 'Dog', 'German Shepherd', 4, 'Loyal and protective German Shepherd, great with families.', 'available', 'https://example.com/images/max.jpg'),
('Luna', 'Cat', 'Persian', 1, 'Fluffy Persian cat, very affectionate and calm.', 'adopted', 'https://example.com/images/luna.jpg'),
('Charlie', 'Dog', 'Beagle', 2, 'Playful beagle with lots of energy and love for walks.', 'available', 'https://example.com/images/charlie.jpg');

INSERT INTO adoption_adoptionrequest (pet_id, adopter_name, adopter_email, request_date) VALUES
(1, 'John Doe', 'john.doe@example.com', '2024-01-15 10:30:00.000000'),
(2, 'Jane Smith', 'jane.smith@example.com', '2024-01-16 14:20:00.000000'),
(4, 'Bob Johnson', 'bob.johnson@example.com', '2024-01-17 09:15:00.000000');