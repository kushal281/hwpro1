# Student Records Dashboard

A simple Flask web app for managing student courses and grades.

## Features

- User login
- View student courses and grades
- Add new courses (grade must be a number between 0 and 100)
- Remove courses
- Responsive UI (Tailwind CSS)
- Client-side grade validation

## Requirements

- Python 3.x
- pip

## Setup

1. **Clone or Download the Project**

   Download or clone the project folder to your computer.

2. **Install Dependencies**

   Open a terminal in the project folder and run:

   ```
   pip install flask werkzeug
   ```

3. **Project Structure**

   ```
   .
   ├── app.py
   ├── index.txt
   ├── password.txt
   ├── templates/
   │   ├── index.html
   │   └── options.html
   └── ...
   ```

4. **Run the App**

   ```
   python app.py
   ```

5. **Open in Browser**

   Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Usage

- **Login** with any of the given user ID and password or you can add yours.
- **Add a course:** Enter a course name and a grade (0-100, digits only).
- **Remove a course:** Click "Remove" next to a course.
- **Logout:** Click the "Logout" button.

## Notes

- Make sure `index.txt` and `password.txt` are present and formatted correctly.
- All changes are local to your machine.
- To share or collaborate, use Git or zip the project folder.

## License

MIT License
