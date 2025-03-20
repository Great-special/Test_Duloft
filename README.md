# Property Management System (Django)

A simple and efficient Property Management System built with Django. This system allows property managers to manage properties, tenants, leases, and maintenance requests seamlessly.

## Features

- **Property Management**: Add, update, and delete properties.
- **Tenant Management**: Manage tenant information and lease agreements.
- **Lease Tracking**: Track lease start and end dates, rent amounts, and payment status.
- **Maintenance Requests**: Submit and track maintenance requests for properties.
- **User Authentication**: Secure login and user management for property managers.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Great-special/property-management-system.git
   cd property-management-system
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the admin panel**:
   Visit `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## Usage

- **Admin Panel**: Use the Django admin panel to manage properties, tenants, leases, and maintenance requests.
- **API Endpoints**: Explore the API endpoints for integration with other systems (if applicable).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Happy Property Managing!
