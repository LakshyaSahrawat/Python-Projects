# Video Management System (VMS) – Setup Instructions

## 1. Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- **Docker** (version 20.x or above)  
  [Download Docker](https://www.docker.com/get-started)
- **Docker Compose** (version 1.29.x or above)  
  [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
- Optional: **Git** if you want to clone the repository instead of using the zip file

---

## 2. Unzip the Project

1. Download the attached `vms-project.zip`.
2. Extract the zip file to a preferred directory, e.g., `C:\Projects\vms-project`.

After extraction, the directory structure should look like this:

```
vms-project/
├── backend/
├── vms-frontend/
├── docker-compose.yml
```

---

## 3. Build and Run Using Docker Compose

1. Open a terminal (Command Prompt / PowerShell / Terminal) and navigate to the project root folder:

```bash
cd path_to_extracted_folder/vms-project
```

2. Build and start the Docker containers:

```bash
docker-compose up --build
```

3. This will:

- Build the backend (FastAPI with OpenCV)
- Build the frontend (React)
- Start the backend at **http://localhost:8000**
- Start the frontend at **http://localhost:3000**

4. Access the application in your browser:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 4. Project Structure

### Backend (FastAPI)
- Location: `backend/`
- Contains:
  - `app/streams.py` – Handles video stream processing
  - `app/main.py` – FastAPI application entry point
  - `Dockerfile` – Container instructions for backend

### Frontend (React)
- Location: `vms-frontend/`
- Contains:
  - React application code
  - `Dockerfile` – Container instructions for frontend

### Docker Compose
- `docker-compose.yml` – Defines services for backend and frontend

---

## 5. Using the Application

1. Launch Docker Compose (as shown in Step 3).
2. Open the frontend in a browser.
3. Add or view streams.
4. Monitor alerts in real-time via the Alerts panel.

---

## 6. Stopping the Application

To stop the containers:

```bash
docker-compose down
```

This will stop and remove both backend and frontend containers.

---

## 7. Notes

- Ensure that sample videos used in the backend are located in the `backend/sample_videos/` folder.
- The application uses a **dummy motion detector**. You can integrate other AI models as needed.
- If ports 3000 or 8000 are occupied, change them in `docker-compose.yml`.

