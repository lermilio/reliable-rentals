"""Create and demonstrate the Reliable Rentals SQLite database."""

import sqlite3


def create_tables(connection):
    """Create the five tables in foreign key order."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS Outlet (
            outletNumber INTEGER PRIMARY KEY,
            address TEXT NOT NULL,
            phoneNumber TEXT NOT NULL,
            faxNumber TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Vehicle (
            registrationNumber TEXT NOT NULL PRIMARY KEY
                CHECK (length(registrationNumber) > 0
                       AND registrationNumber NOT GLOB '*[^A-Za-z0-9]*'),
            make TEXT NOT NULL CHECK (length(trim(make)) > 0),
            model TEXT NOT NULL CHECK (length(trim(model)) > 0),
            engineSize REAL NOT NULL
                CHECK (typeof(engineSize) = 'real' AND engineSize > 0),
            capacity INTEGER NOT NULL
                CHECK (typeof(capacity) = 'integer' AND capacity > 0),
            currentMileage REAL NOT NULL
                CHECK (typeof(currentMileage) = 'real' AND currentMileage >= 0),
            dailyHireRate REAL NOT NULL
                CHECK (typeof(dailyHireRate) = 'real' AND dailyHireRate > 0),
            outletNumber INTEGER NOT NULL,
            FOREIGN KEY (outletNumber) REFERENCES Outlet(outletNumber)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            clientNumber INTEGER PRIMARY KEY,
            firstName TEXT NOT NULL CHECK (length(trim(firstName)) > 0),
            lastName TEXT NOT NULL CHECK (length(trim(lastName)) > 0),
            homeAddress TEXT NOT NULL,
            phoneNumber TEXT NOT NULL,
            dateOfBirth TEXT NOT NULL
                CHECK (date(dateOfBirth, '+0 days') IS dateOfBirth),
            drivingLicenseNumber TEXT NOT NULL
                CHECK (length(drivingLicenseNumber) > 0
                       AND drivingLicenseNumber NOT GLOB '*[^A-Za-z0-9]*'),
            licenseState TEXT NOT NULL CHECK (licenseState GLOB '[A-Z][A-Z]'),
            UNIQUE (drivingLicenseNumber, licenseState)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS StaffMember (
            staffNumber INTEGER PRIMARY KEY,
            firstName TEXT NOT NULL CHECK (length(trim(firstName)) > 0),
            lastName TEXT NOT NULL CHECK (length(trim(lastName)) > 0),
            homeAddress TEXT NOT NULL,
            homePhoneNumber TEXT NOT NULL,
            dateOfBirth TEXT NOT NULL
                CHECK (date(dateOfBirth, '+0 days') IS dateOfBirth),
            sex TEXT NOT NULL CHECK (sex IN ('F', 'M', 'X')),
            dateJoined TEXT NOT NULL
                CHECK (date(dateJoined, '+0 days') IS dateJoined),
            jobTitle TEXT NOT NULL CHECK (length(trim(jobTitle)) > 0),
            salary REAL NOT NULL
                CHECK (typeof(salary) = 'real' AND salary >= 0),
            outletNumber INTEGER NOT NULL,
            CHECK (dateJoined >= date(dateOfBirth, '+18 years')),
            FOREIGN KEY (outletNumber) REFERENCES Outlet(outletNumber)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS HireAgreement (
            hireNumber INTEGER PRIMARY KEY,
            startDate TEXT NOT NULL
                CHECK (date(startDate, '+0 days') IS startDate),
            requestedTerminationDate TEXT NOT NULL
                CHECK (date(requestedTerminationDate, '+0 days') IS requestedTerminationDate),
            mileageBeforeHire REAL NOT NULL
                CHECK (typeof(mileageBeforeHire) = 'real' AND mileageBeforeHire >= 0),
            mileageAfterHire REAL
                CHECK (mileageAfterHire IS NULL OR (
                    typeof(mileageAfterHire) = 'real'
                    AND mileageAfterHire >= mileageBeforeHire
                )),
            clientNumber INTEGER NOT NULL,
            registrationNumber TEXT NOT NULL,
            CHECK (requestedTerminationDate > startDate),
            FOREIGN KEY (clientNumber) REFERENCES Client(clientNumber),
            FOREIGN KEY (registrationNumber) REFERENCES Vehicle(registrationNumber)
        )
    """)


def insert_sample_data(connection):
    """Load five sample rows per table."""
    # Each tuple follows the column order in its INSERT statement.
    outlet_rows = [
        (1, "1200 Example Ave, Miami, FL 33131", "305-555-0101", None),
        (2, "1800 Example Ave, Coral Gables, FL 33134", "305-555-0104", None),
        (3, "2200 Example Ave, Doral, FL 33166", "305-555-0105", "305-555-0191"),
        (4, "410 Example Ave, Miami Beach, FL 33139", "305-555-0106", None),
        (5, "550 Example Ave, Key Biscayne, FL 33149", "305-555-0107", None),
    ]

    vehicle_rows = [
        ("FLA1234", "Toyota", "Camry", 2.5, 5, 18000, 59.95, 1),
        ("FLB2345", "Honda", "Civic", 2.0, 5, 22150, 54.95, 1),
        ("FLC3456", "Ford", "Escape", 1.5, 5, 31580, 69.95, 2),
        ("FLD4567", "Hyundai", "Tucson", 2.5, 5, 15420, 64.95, 3),
        ("FLE5678", "Kia", "Sportage", 2.5, 5, 28500, 64.95, 4),
    ]

    client_rows = [
        (1, "Jordan", "Lee", "250 Example St, Miami, FL 33131",
         "305-555-0102", "1998-04-12", "D1234567", "FL"),
        (2, "Alex", "Morgan", "310 Example St, Doral, FL 33166",
         "305-555-0111", "1993-09-18", "D1234567", "GA"),
        (3, "Sam", "Patel", "420 Example St, Miami, FL 33131",
         "305-555-0112", "1997-02-07", "S4321987", "FL"),
        (4, "Taylor", "Chen", "530 Example St, Coral Gables, FL 33134",
         "305-555-0113", "1990-07-21", "T8754321", "FL"),
        (5, "Jamie", "Brooks", "640 Example St, Miami Beach, FL 33139",
         "305-555-0114", "1995-12-03", "J7654321", "FL"),
    ]

    staff_rows = [
        (1, "Casey", "Rivera", "300 Example St, Miami, FL 33131", "305-555-0103",
         "1996-03-15", "F", "2023-06-05", "Rental Agent", 48000, 1),
        (2, "Avery", "Lewis", "710 Example St, Coral Gables, FL 33134", "305-555-0121",
         "1991-08-24", "X", "2021-05-17", "Outlet Manager", 69000, 2),
        (3, "Mia", "Davis", "820 Example St, Doral, FL 33166", "305-555-0122",
         "1999-04-09", "F", "2024-01-10", "Rental Agent", 46000, 3),
        (4, "Noah", "Wilson", "930 Example St, Miami Beach, FL 33139", "305-555-0123",
         "1994-11-02", "M", "2022-09-12", "Fleet Coordinator", 53500, 4),
        (5, "Riley", "Brown", "1040 Example St, Key Biscayne, FL 33149", "305-555-0124",
         "1997-06-18", "X", "2023-08-21", "Rental Agent", 47000, 5),
    ]

    hire_rows = [
        (1, "2026-11-24", "2026-11-27", 18000, None, 1, "FLA1234"),
        (3, "2026-10-10", "2026-10-12", 22000, 22150, 1, "FLB2345"),
        (4, "2026-10-15", "2026-10-18", 31400, 31580, 2, "FLC3456"),
        (5, "2026-11-01", "2026-11-04", 15250, 15420, 3, "FLD4567"),
        (6, "2026-11-20", "2026-11-23", 28200, 28500, 5, "FLE5678"),
    ]

    # Load parent rows before rows that reference them.
    connection.executemany("""
        INSERT INTO Outlet (outletNumber, address, phoneNumber, faxNumber)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(outletNumber) DO NOTHING
    """, outlet_rows)

    connection.executemany("""
        INSERT INTO Vehicle (
            registrationNumber, make, model, engineSize,
            capacity, currentMileage, dailyHireRate, outletNumber
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(registrationNumber) DO NOTHING
    """, vehicle_rows)

    connection.executemany("""
        INSERT INTO Client (
            clientNumber, firstName, lastName, homeAddress, phoneNumber,
            dateOfBirth, drivingLicenseNumber, licenseState
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(clientNumber) DO NOTHING
    """, client_rows)

    connection.executemany("""
        INSERT INTO StaffMember (
            staffNumber, firstName, lastName, homeAddress, homePhoneNumber,
            dateOfBirth, sex, dateJoined, jobTitle, salary, outletNumber
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(staffNumber) DO NOTHING
    """, staff_rows)

    connection.executemany("""
        INSERT INTO HireAgreement (
            hireNumber, startDate, requestedTerminationDate,
            mileageBeforeHire, mileageAfterHire, clientNumber, registrationNumber
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(hireNumber) DO NOTHING
    """, hire_rows)


def show_tables(connection):
    """Display the database contents before running the examples."""
    table_queries = (
        ("Outlet", "SELECT * FROM Outlet ORDER BY outletNumber"),
        ("Vehicle", "SELECT * FROM Vehicle ORDER BY registrationNumber"),
        ("Client", "SELECT * FROM Client ORDER BY clientNumber"),
        ("StaffMember", "SELECT * FROM StaffMember ORDER BY staffNumber"),
        ("HireAgreement", "SELECT * FROM HireAgreement ORDER BY hireNumber"),
    )
    for table_name, query in table_queries:
        print(f"\n{table_name}")
        for row in connection.execute(query):
            print(row)


def show_rental_history(connection, client_number):
    """Show a client's agreements and the associated vehicle details."""
    rental_history = connection.execute("""
        SELECT c.firstName, c.lastName,
               h.hireNumber, h.startDate, h.requestedTerminationDate,
               h.mileageBeforeHire, h.mileageAfterHire,
               v.make, v.model, v.dailyHireRate
        FROM Client AS c
        JOIN HireAgreement AS h ON h.clientNumber = c.clientNumber
        JOIN Vehicle AS v ON v.registrationNumber = h.registrationNumber
        WHERE c.clientNumber = ?
        ORDER BY h.startDate, h.hireNumber
    """, (client_number,)).fetchall()

    print(f"\nRental history for client {client_number}")
    for rental in rental_history:
        print(rental)


def show_available_vehicles(connection, outlet_number, requested_start, requested_end):
    """List the outlet's vehicles with no overlapping scheduled rentals."""
    available_vehicles = connection.execute("""
        SELECT v.registrationNumber, v.make, v.model,
               v.capacity, v.currentMileage, v.dailyHireRate
        FROM Outlet AS o
        JOIN Vehicle AS v ON v.outletNumber = o.outletNumber
        WHERE o.outletNumber = ?
          AND NOT EXISTS (
              SELECT 1
              FROM HireAgreement AS h
              WHERE h.registrationNumber = v.registrationNumber
                AND h.startDate < ?
                AND h.requestedTerminationDate > ?
          )
        ORDER BY v.registrationNumber
    """, (outlet_number, requested_end, requested_start)).fetchall()

    print(f"\nAvailable vehicles at outlet {outlet_number}")
    if not available_vehicles:
        print("No vehicles available for those dates.")
    for vehicle in available_vehicles:
        print(vehicle)


def create_hire_agreement(connection, booking):
    """Create a hire for an eligible client when the vehicle is available."""
    with connection:
        result = connection.execute("""
            INSERT INTO HireAgreement (
                hireNumber, startDate, requestedTerminationDate, mileageBeforeHire,
                mileageAfterHire, clientNumber, registrationNumber
            )
            SELECT :hire_number, :start_date, :end_date, v.currentMileage,
                   NULL, c.clientNumber, v.registrationNumber
            FROM Client AS c
            CROSS JOIN Vehicle AS v
            WHERE c.clientNumber = :client_number
              AND v.registrationNumber = :registration
              AND :start_date >= date(c.dateOfBirth, '+21 years')
              AND NOT EXISTS (
                  SELECT 1
                  FROM HireAgreement AS h
                  WHERE h.registrationNumber = v.registrationNumber
                    AND h.startDate < :end_date
                    AND h.requestedTerminationDate > :start_date
              )
            ON CONFLICT(hireNumber) DO NOTHING
        """, booking)

    if result.rowcount == 1:
        daily_rate = connection.execute("""
            SELECT dailyHireRate
            FROM Vehicle
            WHERE registrationNumber = :registration
        """, booking).fetchone()[0]

        print(f"\nCreated hire {booking['hire_number']} at ${daily_rate:.2f}/day.")
    else:
        print("\nNo hire added. Check the hire number, client, vehicle, and dates.")


def record_vehicle_return(connection, hire_number, return_mileage):
    """Save the agreement and vehicle mileage updates in one transaction."""
    return_details = {
        "hire_number": hire_number,
        "return_mileage": return_mileage,
    }

    with connection:
        return_update = connection.execute("""
            UPDATE HireAgreement
            SET mileageAfterHire = :return_mileage
            WHERE hireNumber = :hire_number
              AND mileageAfterHire IS NULL
              AND :return_mileage >= mileageBeforeHire
        """, return_details)

        if return_update.rowcount == 1:
            connection.execute("""
                UPDATE Vehicle
                SET currentMileage = :return_mileage
                WHERE registrationNumber = (
                    SELECT registrationNumber
                    FROM HireAgreement
                    WHERE hireNumber = :hire_number
                )
            """, return_details)

    if return_update.rowcount == 1:
        print(f"\nRecorded return for hire {return_details['hire_number']}.")
    else:
        print("\nReturn skipped. Check the hire number, return status, and mileage.")


def show_outlet_staff(connection, outlet_number):
    """List the staff and contact details for an outlet."""
    staff_at_outlet = connection.execute("""
        SELECT s.staffNumber, s.firstName, s.lastName, s.jobTitle,
               s.homePhoneNumber, s.dateJoined, s.salary,
               o.address, o.phoneNumber
        FROM StaffMember AS s
        JOIN Outlet AS o ON s.outletNumber = o.outletNumber
        WHERE o.outletNumber = ?
        ORDER BY s.lastName, s.firstName, s.staffNumber
    """, (outlet_number,)).fetchall()

    print(f"\nStaff assigned to outlet {outlet_number}")
    if not staff_at_outlet:
        print("No staff found for this outlet.")
    for staff_member in staff_at_outlet:
        print(staff_member)


def main():
    connection = sqlite3.connect("reliable_rentals.db")
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        create_tables(connection)
        with connection:
            insert_sample_data(connection)

        show_tables(connection)

        # Run the five Part 2 examples in report order.
        show_rental_history(connection, client_number=1)
        show_available_vehicles(connection, 1, "2026-11-25", "2026-11-26")
        booking = {
            "hire_number": 2,
            "client_number": 1,
            "registration": "FLA1234",
            "start_date": "2026-12-01",
            "end_date": "2026-12-03",
        }
        create_hire_agreement(connection, booking)
        record_vehicle_return(connection, hire_number=1, return_mileage=18125)
        show_outlet_staff(connection, outlet_number=1)
    finally:
        connection.close()


if __name__ == "__main__":
    main()