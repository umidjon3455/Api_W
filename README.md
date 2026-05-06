# Blog API

A RESTful API for a blog application with user authentication, posts, comments, and likes functionality.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Posts**: Create, read, update, and delete posts
- **Comments**: Add comments to posts
- **Likes**: Like/unlike posts (one like per user per post)
- **Pagination**: 10 posts per page
- **Search**: Search posts by title and content
- **Filtering**: Filter posts by author
- **Sorting**: Sort posts by creation date and title
- **Admin Panel**: Django admin interface for content management

## Technology Stack

- **Backend**: Django 4.2.7 with Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT (JSON Web Tokens)
- **Documentation**: Swagger/OpenAPI with drf-spectacular

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | User registration | No |
| POST | `/api/login/` | User login | No |
| GET | `/api/me/` | Get current user profile | Yes |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | List all users | Yes |
| GET | `/api/users/{id}/` | Get user details | Yes |

### Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List posts (with pagination, search, filter, sort) | No |
| POST | `/api/posts/` | Create new post | Yes |
| GET | `/api/posts/{id}/` | Get post details | No |
| PUT | `/api/posts/{id}/` | Update post (author only) | Yes |
| DELETE | `/api/posts/{id}/` | Delete post (author only) | Yes |

### Comments

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/{post_id}/comments/` | List comments for a post | No |
| POST | `/api/posts/{post_id}/comments/` | Add comment to a post | Yes |

### Likes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/posts/{post_id}/like/` | Like a post | Yes |
| DELETE | `/api/posts/{post_id}/unlike/` | Unlike a post | Yes |

## Query Parameters

### Posts List (`/api/posts/`)

- `search`: Search in title and content
- `author`: Filter by author ID
- `ordering`: Sort by field (created_at, title)
- `page`: Page number for pagination

**Examples:**
```
GET /api/posts/?search=django
GET /api/posts/?author=1
GET /api/posts/?ordering=-created_at
GET /api/posts/?page=2
```

## Data Models

### User
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Post
```json
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content...",
  "author": 1,
  "author_email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "likes_count": 5,
  "is_liked": false,
  "comments": [...]
}
```

### Comment
```json
{
  "id": 1,
  "content": "Comment text",
  "author": 1,
  "author_email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message"
}
```

### Status Codes
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

## Business Rules

1. **Post Ownership**: Users can only edit/delete their own posts
2. **Like Limit**: One like per user per post
3. **Cascade Delete**: Deleting a post also deletes its comments and likes
4. **Authentication**: All write operations require authentication
5. **Pagination**: Posts are paginated (10 per page)

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd blog_api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## Testing with Postman

### 1. Register a new user
```http
POST /api/register/
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123",
  "password_confirm": "password123"
}
```

### 2. Login
```http
POST /api/login/
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

### 3. Create a post (using JWT token)
```http
POST /api/posts/
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my first post."
}
```

### 4. Like a post
```http
POST /api/posts/1/like/
Authorization: Bearer <your-jwt-token>
```

## Deployment

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Production Database
Update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### Recommended Hosting
- **Backend**: Render, Railway, or Heroku
- **Database**: PostgreSQL (provided by hosting platform)
- **Static Files**: AWS S3 or similar

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Passwords are hashed using Django's built-in authentication
- **CORS**: Configured for frontend integration
- **Input Validation**: Serializers validate all input data
- **Permission Checks**: Users can only modify their own content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
