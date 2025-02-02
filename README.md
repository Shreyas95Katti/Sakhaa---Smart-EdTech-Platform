# Sakhaa---Smart-Ed-Tech-Platform

## Overview
This project was built during a 24-hour hackathon and has been successfully deployed using HTML, CSS, and Flask. The platform aims to assist low-level institutions in maintaining education standards by automating and enhancing various educational processes. It enables teachers to conduct online classes, manage assessments, and track attendance efficiently.

## Pre-Requisites
**Twilio Integration:** Head over to https://console.twilio.com/ after creating your account n Twilio. Configure your whatsapp in the messages section. Access the account credentials mentioned in the page.

**Zoom Integration:** Head over to https://marketplace.zoom.us/, under the developer build app section select Server to Server OAuth App. Record the credentials and setup scope to meeting:write:meeting:admin access. 

**Dlib Installation**: Head over to https://pypi.org/project/dlib/#files. Install the file and add to environment variables.

## Usage
**Clone the repository:** Clone this repository in a virtual environment and install the requirements.
```bash
pip install -r requirements
``` 

**Tutor/Teacher Login**
1. Add your Twilio and Zoom credentials in **teacher_app.py** 


2. Run the file
```bash
python teacher_app.py
```
This file allows you to explore the virtual whiteboard, proctored examination and automated classroom meeting. 

3. Run the file
```bash
python student_app.py
```
This file allow you to explore the automated attendance system.

## Features

### Virtual Whiteboard
**Interactive Teaching:** Teachers can write in the air and annotate directly on study materials, providing an engaging and interactive learning experience.

### Automated Attendance
**Seamless Tracking:** Attendance is automatically recorded using computer vision and machine learning techniques, ensuring accuracy and saving time.

### Proctored Online Assessment
**Secure Testing:** Conduct proctored tests online, leveraging computer vision to ensure the integrity and security of the assessment process.

### WhatsApp Integration and Zoom API
**Effortless Communication:** Teachers can create Zoom meetings directly through the platform, with meeting details automatically sent to students via WhatsApp.

## Web Integration
User-Friendly Interface: The platform is built with HTML, CSS, and Flask, providing a seamless and intuitive web interface for both teachers and students.

## Technology Stack
1. Frontend: HTML, CSS
2. Backend: Flask
3. APIs: Zoom API, WhatsApp Integration
4. Advanced Technologies: API, Computer Vision, Machine Learning

## Problem Statement
This platform addresses the challenge faced by low-level institutions in maintaining educational standards. By automating and streamlining various educational processes, the platform ensures that institutions can provide quality education even with limited resources.

## Deployment
The project is fully deployed and ready for use. Institutions can integrate this platform into their existing systems or use it as a standalone solution to enhance their educational capabilities.
