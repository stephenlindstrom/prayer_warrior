# Prayer Warrior

This is a **Django-based web application** for managing prayer groups, prayer requests, and answered prayers. Users can create prayer groups, add prayer requests to both private and group lists, mark prayers as answered, and manage group memberships.

---

## Features

- **User Authentication**: Login, logout, and registration.
- **Personal Prayer Requests**: Add, view, mark as answered, and delete personal prayer requests.
- **Group Management**: Create groups, add members, and view group prayer requests.
- **Answered Prayers**: Track answered prayers and view them separately.

---

## Installation Instructions

### Prerequisites

- **Python 3.12.3**
- **Django 5.1.4**
- **Virtual Environment** (optional but recommended)

### Steps to Install

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/prayer-group-app.git
   cd prayer-group-app
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

   Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📂 Project Structure

```
prayer-group-app/
│
├── app/                            # Main Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # Views for handling requests
│   ├── forms.py                    # Forms for user input
│   ├── urls.py                     # URL configurations
│   └── templates/app/              # HTML templates
│
├── prayer-group-app/               # Django project configuration
│   ├── settings.py                 # Project settings
│   └── urls.py                     # Project-wide URL configurations
│
├── manage.py                       # Django management script
└── requirements.txt                # Python dependencies
```

---

## ⚙️ Key Views and Their Functionality

### `NewLoginView`
- **Purpose**: Custom login view.
- **URL**: `/login/`

### `IndexView`
- **Purpose**: Home page for logged-in users.
- **URL**: `/`

### `PersonalPrayerView`
- **Purpose**: View personal prayer requests (paginated).
- **URL**: `/personal-prayers/`

### `AddPrayerRequestView`
- **Purpose**: Add a new prayer request.
- **URL**: `/prayer-request/add/`

### `PrayerRequestDeleteView`
- **Purpose**: Delete a personal prayer request.
- **URL**: `/prayer-request/delete/<id>/`

### `AnsweredPrayerListView`
- **Purpose**: List answered prayers.
- **URL**: `/answered-prayers/`

### `CreateGroupView`
- **Purpose**: Create a new group and add the user to it.
- **URL**: `/group/create/`

### `GroupListView`
- **Purpose**: List groups the user belongs to.
- **URL**: `/groups/`

### `GroupDetailView`
- **Purpose**: View group details and associated prayers.
- **URL**: `/group/<id>/`

### `AddMemberView`
- **Purpose**: Add a new member to a group.
- **URL**: `/group/<group_id>/add-member/`

---

## 📝 Models Overview

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

## ✅ Usage Instructions

1. **Register an Account**: Go to `/register/` to create an account.
2. **Log In**: Log in via `/login/`.
3. **Add a Prayer Request**: Navigate to `/prayer-request/add/` to submit a new prayer.
4. **Create a Group**: Go to `/group/create/` to create a new group.
5. **View Groups**: Access your groups at `/groups/`.
6. **Add Members**: Add members to your group via `/group/<group_id>/add-member/`.

---

## 💻 Technologies Used

- **Django**: Web framework
- **SQLite**: Default database (can be replaced with PostgreSQL or MySQL)
- **Bootstrap**: Frontend styling (if applicable)
- **FontAwesome**: Icons for UI elements

---

## 💜 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it.

---

## 🙏 Acknowledgements

Special thanks to all contributors and the Django community for their support and resources.

---

## 🐛 Troubleshooting

- **Login Issues**: Ensure your credentials are correct. Reset your password if needed.
- **Database Issues**: Run `python manage.py migrate` to apply migrations.
- **Static Files**: Collect static files with `python manage.py collectstatic`.

---

## 📩 Contact

For questions or contributions, please contact:

- **Email**: `your-email@example.com`
- **GitHub**: [https://github.com/your-username](https://github.com/your-username)
