INSERT INTO "User" (name, email, usertype, password)
VALUES
('John Doe', 'johndoe@example.com', 'renter', 'password123'),
('Jane Smith', 'janesmith@example.com', 'agent', 'securepassword'),
('Bob Johnson', 'bobjohnson@example.com', 'renter', 'password321');

INSERT INTO renters (user_id, order_date, delivery_id, customer_id, email, rental_preferences)
VALUES
(1, '2023-05-01', 12345, 98765, 'johndoe@example.com', '2 bedrooms, furnished, pet-friendly'),
(3, '2023-05-03', 67890, 24680, 'bobjohnson@example.com', '1 bedroom, near public transportation');

INSERT INTO agents (user_id, job_title, real_estate_agency, contact_information, email)
VALUES
(2, 'Real Estate Agent', 'ABC Realty', '123-456-7890', 'janesmith@example.com')

INSERT INTO neighborhood (location, city, state, crime_rate)
VALUES
('Downtown', 'Los Angeles', 'CA', 75),
('Upper East Side', 'New York', 'NY', 45),
('Lincoln Park', 'Chicago', 'IL', 60);



INSERT INTO property (type, location, city, state, description, price, availability, neighborhood_id, agent_id)
VALUES ('apartment', '123 Main St', 'Los Angeles', 'CA', 'Spacious 2 bedroom apartment', 2500, true, 1, 1);

INSERT INTO property (type, location, city, state, description, price, availability, neighborhood_id, agent_id)
VALUES ('house', '456 Oak Ave', 'San Francisco', 'CA', 'Charming 3 bedroom house', 5000, true, 2, 1);

INSERT INTO property (type, location, city, state, description, price, availability, neighborhood_id, agent_id)
VALUES ('house', '789 Maple Dr', 'New York', 'NY', 'Large plot of land with potential for development', 1000000, true, 3, 1);

INSERT INTO property (type, location, city, state, description, price, availability, neighborhood_id, agent_id)
VALUES ('house', '101 Market St', 'Chicago', 'IL', 'Newly renovated commercial building in prime location', 500000, true, 1, 1);

INSERT INTO property (type, location, city, state, description, price, availability, neighborhood_id, agent_id)
VALUES ('apartment', '111 Beach Blvd', 'Miami', 'FL', 'Beautiful beachfront vacation home', 5000, true, 1, 1);


INSERT INTO house (property_id, number_of_rooms, square_footage, location)
VALUES (1, 4, 2000, '123 Main St');





INSERT INTO address (user_id, address, state, city, zip_code)
VALUES
(1, '123 Main St', 'CA', 'Los Angeles', '90001'),
(2, '456 Oak Ave', 'NY', 'New York', '10001'),
(3, '789 Pine St', 'IL', 'Chicago', '60601');

INSERT INTO creditcard (renter_id, cardnumber, expirationdate, paymentaddress_id, cvv)
VALUES
(1, '1234567812345678', '2024-06-30', 1, '123'),
(2, '1111222233334444', '2023-12-31', 3, '789');


INSERT INTO payment (payment_status, credit_card_id, renter_id, propertyid, agent_id, date, payment_amount)
VALUES
('PAID', 1, 1, 1, 1, '2023-05-06', 1500.00),
('PENDING', 2, 2, 2, 2, '2023-05-07', 2000.00);

INSERT INTO propertybooking (renter_id, propertyid, creditcardid, desired_move_in_date, billingaddress_id, budget, agentid)
VALUES
(1, 1, 1, '2023-07-01', 1, 2500.00, 1),
(2, 2, 2, '2023-06-15', 3, 3000.00, 2),
(3, 3, 1, '2023-07-31', 2, 2000.00, 1);


INSERT INTO school (name, location, city, state, neighborhoodid)
VALUES ('Example School', '123 Main St', 'Anytown', 'CA', 1);
