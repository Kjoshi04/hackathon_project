##  ReliefLink
A real-time emergency logistics coordination system to streamline crisis aid distribution with visibility, transparency, and simplicity.

##  Problem Statement
Problem Statement – Redesign Crisis Logistics and Relief Distribution
Build a digital logistics system to help NGOs and governments coordinate emergency aid, track supply chains, needs, drop zones, and distribution transparency in real-time during crises.

##  Objective
In times of disaster, coordinating aid is often chaotic — requests go unanswered, resources are misallocated, and visibility is lost.
ReliefLink solves this by creating a centralized, real-time digital platform where field volunteers, NGOs, and authorities can:

* Post and track aid requests
* Claim and fulfill needs transparently
* Monitor relief operations with complete accountability
* It ensures quick, accurate aid delivery, empowering both the providers and the recipients during emergencies.

---

[![View Presentation](https://img.shields.io/badge/View-Presentation-blue?style=for-the-badge)](https://drive.google.com/file/d/1xZjkHPdDuCEvDQd7FgwPHiiWmntAtGDm/view)</br>
[![Watch Demo Video](https://img.shields.io/badge/Watch-Demo%20Video-orange?style=for-the-badge)](https://www.youtube.com/watch?v=bLB3SUPoMzc)

### My Approach:
* Chose this problem due to its real-world humanitarian impact
* Focused on real-time visibility, minimal friction for field users, and robust coordination features
* Pivots included replacing auto-location with address-based geocoding for greater accuracy in low-connectivity zones
* Implemented features focused on transparency and operational resilience

##  Tech Stack
Core Technologies Used:
* Frontend: Streamlit (for rapid UI development and simplicity on field devices)
* Backend: Python (Streamlit integrated logic)
* Database: Firebase Realtime Database

APIs:
* Nominatim API (for geocoding address to lat/lon)
* SMTP (for email notifications)

##  Key Features
* Real-time Relief Request System – Submit and view emergency aid requests instantly</br>
* Volunteer Claim System – Volunteers can claim requests with their name, increasing transparency</br>
*  Email Notifications – Sends auto-email to requesters when their request is claimed</br>
*  Smart Filtering & Search – Filter requests by category, location, and urgency</br>
*  Firebase Realtime Sync – Ensures all users see the latest data without refresh</br>
*  Admin Dashboard – Manage requests, delete entries, and monitor the entire relief operation</br>

![Screenshot 2025-04-25 001753](https://github.com/user-attachments/assets/3839d799-ba55-4672-b1fa-0d517a102571)
![Screenshot 2025-04-25 002030](https://github.com/user-attachments/assets/5c694790-a297-468f-b439-31f546aa95f5)
![Screenshot 2025-04-25 002223](https://github.com/user-attachments/assets/2e0eb5ba-6a2d-4086-934f-404a18351562)
![Screenshot 2025-04-25 002138](https://github.com/user-attachments/assets/a76656a3-4bbd-4e2f-bd09-b9cc8e309293)

##  How to Run the Project
Requirements:
* Python 3.x
* Firebase project setup (Realtime DB)
* API Key for Nominatim (if hitting rate limits)

## Setup Instructions:
## Clone the repo
git clone https://github.com/Kjoshi04/hackathon_project

## Navigate to project
cd hackathon_project

## Install Streamlit
pip install streamlit firebase-admin requests

## Run the app
streamlit run temp1.py</br>
Make sure you configure Firebase credentials and optionally an .env file for sensitive keys.

##  Future Scope
*  Map Integration to visualize aid locations</br>
*  Role-based access for better data control (volunteer/admin/government)</br>
*  Offline mode using PWA or caching for field use in low-connectivity zones</br>
*  Mobile version for on-the-go access</br>
*  Push notifications for real-time claim and delivery updates</br>

##  Resources 
* OpenStreetMap Nominatim API
* Streamlit Docs
* Firebase Documentation
* SMTP & Python Email Tutorial

