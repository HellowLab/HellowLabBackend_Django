# HellowLabBackend_Django
Django backend API service for all Hellow Lab products

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Sub-Prjects](#sub-projects)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication for all HellowLab products
- Backend API for DblFeature app

## Requirements

- Python 3.11.4
- Django 5.0.2
- Use requirements.txt for all other requirements

## Installation

1. **Clone the repository:**

   Clone the repository.

2. **Create and activate a virtual environment:**

  ```bash
   python3 -m venv venv
   source venv/bin/activate
  ```
3. **Install dependencies:**

  ```bash
   pip install -r requirements.txt
  ```

4. **Run migrations:**

  ```bash
   cd HellowLab
   python manage.py makemigrations
   python manage.py migrate
  ```

5. **Create a superuser:**

  ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

  ```bash
   python manage.py runserver 0.0.0.0:8000
  ```

## Configuration

- **Environment Variables:** You can configure environment variables by creating a `.env` file in `./HellowLab/HellowLab/.env`. Common variables include:

```bash
  DEBUG=True
  SECRET_KEY=your_secret_key
  DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

- **Settings:** Modify `settings.py` for any additional settings such as installed apps, middleware, or custom configurations.

## Sub-Projects

- **HellowLab**

   HellowLab is the core module of our system, providing essential laboratory functionalities such as data analysis, result processing, and experiment management. This sub-project is designed to streamline lab operations by integrating various tools and resources necessary for scientific research and development.

- **Authentication**

   The Authentication sub-project handles all user-related security features, including user registration, login, password management, and access control. It ensures that only authorized users can access specific parts of the application by implementing robust authentication and authorization mechanisms using industry-standard practices.

- **DblFeature**

   DblFeature is the API interface for our application named DblFeature. This sub-project is responsible for managing the API endpoints that interact with the core application, providing data access and manipulation capabilities. It serves as the bridge between the front-end and back-end, ensuring smooth and efficient communication across the system.

## Usage

Once the server is running, you can access the API at `http://127.0.0.1:8000/`.
The admin service can be accessed at `http://127.0.0.1:8000/admin`.

### API Endpoints

- **Authentication:**
  - POST /api/auth/login/ - Log in a user.
  - POST /api/auth/logout/ - Log out a user.
  - POST /api/auth/register/ - Register a new user.

- **User:**
  - GET /api/users/ - Get all users.
  - GET /api/users/<id>/ - Get user by ID.
  - PUT /api/users/<id>/ - Update user by ID.
  - DELETE /api/users/<id>/ - Delete user by ID.

## Running Tests

To run tests, use the following command:

python manage.py test

## Contributing

If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.