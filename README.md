# CS-425-Database-Project

		• For each User, we should record the name of the User, one or more
		addresses, and email address. Users can be either agents or perspective
		renters and are identified by their email address.

		– For agents, we should also record their job title, real estate agency
		they work for, and contact information.

		– For perspective renters, we should record their rental preferences
		such as desired move-in date, preferred location, and budget, as
		well as their credit card information. A perspective renter can
		have multiple credit cards, and for each credit card, we associate
		it with a payment address (one of the User’s addresses). Furthermore, we record for each User their preferred location.


3.2 Property information

	The database should record information about Users, properties, prices, and
	booking.
	• Property: The main asset of the real estate agency are properties.
	– A property has a unique identifier, a type (e.g., apartment, house),
	a location, and a description. For each property, record the city
	it is located in (e.g., Chicago), and the state (if applicable).
	– For the project, we will consider the following types of properties:
	∗ Houses: Houses have a location, number of rooms, and square
	footage.
	∗ Apartments: Apartments have a location, number of rooms,
	square footage, and building type.
	∗ Commercial Buildings: Commercial buildings have a location, square footage, and type of business.

		– For each property, we need to store information such as the address, price, and availability.
	• Price: Each property has a rental price
	• Booking: A property booking is for a particular Renter. For each
	property booking we have to store which of the Renter’s credit cards
	was used to make the booking.
	3.2.1 BONUS: Additional Property Types
	• Extend the schema to include information about the neighborhood,
	such as crime rates and nearby schools.
	3.2.2 BONUS: Neighborhood Information
	• Store information about additional property types such as vacation
	homes and land.
	3.2.3 BONUS: Reward Program
	• Renters can join a reward program. If a Renter is registered in the
	reward program, then we store a reward point count for the Renter.
	For every property booking, the Renter received reward points equal



4 Application Requirements

	The application should support the following actions. We indicate for each
	action whether it can be executed by agents or prospective renters.

	• A user can create an account by registering with an email address
	(prospective renters and agents)

	• Add/modify payment/address information: a user holding an account
	can register/modify/delete credit cards and addresses for their account
	(prospective renters) register/modify/delete credit cards and addresses

	for their account
	• Add/Delete/Modify properties (agents only)
	• Search for propertieseate About
	• Book properties (prospective renters only)

4.1 Registration
	The application should allow both agents and perspective renters to register.

4.2 Payment Information and Addresses
	Renters can add/modify/delete addresses and payment methods (credit cards).
	Addresses that are payment addresses (billing) for a credit card can not be
	deleted before deleting the credit card.


4.3 Search For Properties

	The application should allow a user to search for properties. The minimal
	information provided should be a location and a date for the property. The
	user can select whether they want to search for a rental or a sale property.
	Additionally, the user can provide a limit for the number of bedrooms, the
	price range, and the property type (e.g. apartment, house, etc.).

	Only properties that are located in the specified location and available on
	the date provided by the user should be shown. Furthermore, the properties
	have to fulfill all the additional requirements stated by the user. For each
	property show the price, number of bedrooms, property type, and property
	description.
	Furthermore, the user can specify how results should be ordered: by
	price or by number of bedrooms.




sudo -iu postgres psql
CREATE DATABASE flask_db;
CREATE USER sammy WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flask_db TO sammy;
\l
\q

export DB_USERNAME="sammy"
export DB_PASSWORD="password"

