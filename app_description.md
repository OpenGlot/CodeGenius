# Language Learning Application

## Overview

The Language Learning Application is a comprehensive platform designed to facilitate language learning through interactive lessons, multimedia content, AI-powered chatbots, and user-generated content. The app supports various user roles, including Users, Reviewers, Creators, Admins, and SuperAdmins, providing a robust framework for both learners and content creators.

## Features

### User Profiles

- **User Registration and Authentication**: Users can register and log in using their credentials.
- **User Roles**: Users can have multiple roles such as User, Reviewer, Creator, Admin, and SuperAdmin.
- **User Dashboard**: A comprehensive dashboard that displays learning progress, strengths, and areas for improvement.

### Learning Content

- **Languages**: Users can select and learn multiple languages.
- **Courses**: Each language contains multiple courses tailored to different levels and topics.
- **Modules**: Courses are divided into modules, each focusing on specific aspects of the language.
- **Lessons**: Modules contain lessons that include various types of questions and multimedia content.

### Question Types

The application supports several types of questions, including:
- Listen to the Sentence
- Translate the Sentence
- Fill in the Blank
- True or False
- Multiple Choice
- Reorder the Sentence (Unjumble)

Questions can include audio and images to enhance the learning experience.

### Multimedia Content

- **Audio and Video Integration**: High-quality audio and video content are integrated to improve listening and comprehension skills.
- **Images**: Visual aids are used to reinforce learning.

### AI Chatbots

- **Conversational Practice**: AI-powered chatbots provide conversational practice and instant feedback.
- **Multiple AI Options**: Integration with APIs such as OpenAI's ChatGPT and Llama.

### User Interaction

- **Content Rating**: Users can rate lessons and other content with thumbs up or thumbs down.
- **Spaced Repetition System**: Vocabulary learning through flashcards using spaced repetition.
- **Notifications**: Users receive notifications for progress updates, upcoming lessons, and goals.

### Achievements and Rewards

- **Achievement Badges**: Users earn badges for reaching milestones and achievements.
- **Progress Tracking**: Detailed tracking of user progress across courses, modules, and lessons.

### User-Generated Content

- **Content Creation Tools**: Users can create and share lessons, exercises, and quizzes.
- **Community Sharing**: Content can be shared with the community for collaborative learning.

### Subscription Plans

- **Free and Premium Plans**: Various subscription plans with different access levels and features, including additional AI tools and an ad-free experience.

### Interactive Storybooks

- **Engaging Storybooks**: Interactive storybooks where learners make choices that affect the story's outcome, practicing the target language in context.

## Technical Details

### Technologies Used

- **Backend**: C#, .NET 8, Entity Framework Core
- **Frontend**: JavaScript, HTML, CSS
- **Database**: PostgreSQL
- **Authentication**: Amazon Cognito
- **Cloud Services**: Azure for media services and scalability

### API Endpoints

#### Users

- `GET /api/Users` - Retrieve all users
- `GET /api/Users/{id}` - Retrieve a user by ID
- `POST /api/Users` - Add a new user
- `PUT /api/Users/{id}` - Update a user
- `DELETE /api/Users/{id}` - Delete a user
- `GET /api/Users/{id}/Roles` - Retrieve roles for a user
- `POST /api/Users/{id}/Roles` - Add a role to a user
- `DELETE /api/Users/{id}/Roles/{roleId}` - Remove a role from a user

#### Languages

- `GET /api/Languages` - Retrieve all languages
- `GET /api/Languages/{id}` - Retrieve a language by ID
- `POST /api/Languages` - Add a new language
- `PUT /api/Languages/{id}` - Update a language
- `DELETE /api/Languages/{id}` - Delete a language

#### Courses

- `GET /api/Courses` - Retrieve all courses
- `GET /api/Courses/{id}` - Retrieve a course by ID
- `POST /api/Courses` - Add a new course
- `PUT /api/Courses/{id}` - Update a course
- `DELETE /api/Courses/{id}` - Delete a course

#### Modules

- `GET /api/Modules` - Retrieve all modules
- `GET /api/Modules/{id}` - Retrieve a module by ID
- `POST /api/Modules` - Add a new module
- `PUT /api/Modules/{id}` - Update a module
- `DELETE /api/Modules/{id}` - Delete a module

#### Lessons

- `GET /api/Lessons` - Retrieve all lessons
- `GET /api/Lessons/{id}` - Retrieve a lesson by ID
- `POST /api/Lessons` - Add a new lesson
- `PUT /api/Lessons/{id}` - Update a lesson
- `DELETE /api/Lessons/{id}` - Delete a lesson