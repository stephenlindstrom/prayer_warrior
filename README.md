# Prayer Warrior

This is a **Django-based web application** for managing prayer groups, prayer requests, and answered prayers. Users can create prayer groups, add prayer requests to both private and group lists, mark prayers as answered, and manage group memberships.

---

## Features

- **User Authentication**: Login, logout, and registration.
- **Personal Prayer Requests**: Add, view, mark as answered, and delete personal prayer requests.
- **Group Management**: Create groups, add members, and view group prayer requests.
- **Answered Prayers**: Track answered prayers and view them separately.

---

## Demo

You can explore a live demo of the application here:  
🔗 [Live App on Heroku](https://prayer-warrior-app-d9809c63979b.herokuapp.com/login/?next=/)

To log in as a test user:

**Username:** `testuser1`  
**Password:** `p@$$word`

**Note:** This account contains fictional sample data and is intended for demonstration purposes only.

---

## Installation Instructions

### Prerequisites

- **Python 3.12.3**
- **Django 5.1.4**
- **Virtual Environment** (optional but recommended)

### Steps to Install

1. **Clone the Repository**

   ```bash
   git clone https://github.com/stephenlindstrom/prayer-warrior.git
   cd django-list
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   Open your browser and go to: [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)

---

## Project Structure

```
django-list/
│
├── app/                            
│   ├── models.py                   # Database models
│   ├── views.py                    # Views for handling requests
│   ├── forms.py                    # Forms for user input
│   ├── urls.py                     # URL configurations
│   ├── tests.py                    # Unit tests for the app
│   ├── templates/app/              # HTML templates
│   └── static/app/                 # Static files (CSS, JavaScript)
│    
├── list/               
│   ├── settings.py                 # Project settings
│   └── urls.py                     # Project-wide URL configurations
│
├── manage.py                       # Django management script
└── requirements.txt                # Python dependencies

```

---

## Key Views and Their Functionality

### `NewLoginView`
- **Purpose**: Custom login view.
- **URL**: `/login/`

### `IndexView`
- **Purpose**: Home page for logged-in users.
- **URL**: `/app/`

### `PersonalPrayerView`
- **Purpose**: View personal prayer requests.
- **URL**: `/app/personal-prayer/`

### `AddPrayerRequestView`
- **Purpose**: Add a new prayer request.
- **URL**: `/app/prayer-request/`

### `PrayerRequestDeleteView`
- **Purpose**: Delete a personal prayer request.
- **URL**: `/app/delete-prayer-request/<id>/`

### `AddAnsweredPrayerView`
- **Purpose**: Mark prayer request as answered.
- **URL**: `/app/add-answered-prayer/<id>/`

### `AnsweredPrayerListView`
- **Purpose**: List answered prayers.
- **URL**: `app/answered-prayer-list/`

### `CreateGroupView`
- **Purpose**: Create a new group and add the owner to it.
- **URL**: `app/create-group/`

### `GroupListView`
- **Purpose**: List groups the user belongs to.
- **URL**: `app/group-prayers/`

### `GroupDetailView`
- **Purpose**: View all prayer requests associated with group.
- **URL**: `app/group-prayers/<group_id>/`

### `AddMemberView`
- **Purpose**: Add a new member to a group.
- **URL**: `/app/group-prayers/<group_id>/add-member/`

---

## Models Overview

### `PrayerRequest`
- **Fields**: `user`, `content`, `answered`, `datetime`
- **Purpose**: Represents a prayer request by a user.

### `AnsweredPrayer`
- **Fields**: `prayer_request`, `datetime`, `content`
- **Purpose**: Represents an answered prayer tied to a prayer request.

### `Group`
- **Fields**: Inherits from Django's built-in `Group` model.
- **Purpose**: Represents a prayer group.

### `GroupPrayerManager`
- **Fields**: `prayer_request`, `group`
- **Purpose**: Manages the relationship between prayer requests and groups.

---

## Usage Instructions

1. **Register an Account**: Go to `/app/register/` to create an account.
2. **Log In**: Log in via `/login/`.
3. **Add a Prayer Request**: Navigate to `/app/prayer-request/` to submit a new prayer.
4. **Create a Group**: Go to `/app/create-group/` to create a new group.
5. **View Groups**: Access your groups at `/app/group-prayers/`.
6. **Add Members**: Add members to your group via `/app/group-prayers/<group_id>/add-member/`.

---

## Technologies Used

- **Django**: Web framework
- **SQLite**: Default database (can be replaced with PostgreSQL or MySQL)
- **FontAwesome**: Icons for UI elements

---

## Acknowledgements

Special thanks to the Django community for their support and resources.

---

## Contact

For questions or contributions, please contact:

- **GitHub**: [https://github.com/stephenlindstrom](https://github.com/stephenlindstrom)
