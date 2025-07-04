# 🧳 Travel E-Commerce Website

A full-stack travel booking platform that allows users to browse scenic attractions in Taiwan and purchase a 2-day-1-night trip, with third-party payment integration.

---

## 📌 1. Overview

This project retrieves attraction data across Taiwan from a government-provided open JSON API.  
Users can browse and purchase a 2-day-1-night trip to their selected destinations.

---

## 🛠 2. Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask  
- **Database:** MySQL  
- **Infrastructure:** AWS (for deployment, database hosting, etc.)

---

## 🌐 3. Overall Website Architecture Diagram

![Website Architecture Diagram](https://github.com/Shiuan-Chang/flowcharts/blob/main/EcommerceWebsite/ecommerce.drawio.png?raw=true)

---

## 💳 4. Payment Flow Architecture Diagram

![Payment Flow Diagram](https://github.com/Shiuan-Chang/flowcharts/blob/main/EcommerceWebsite/Ecommerce-payment.drawio.png?raw=true)

---

## 🚀 5. Website Features & Implementation

### 🖼 Front-End Features

- **a. Display attractions using government open data**  
  Uses JavaScript's `fetch()` to load and parse JSON data from a public API, dynamically rendering attraction names and images on the homepage.

- **b. Responsive Web Design**  
  Uses CSS media queries to ensure the layout adapts to various screen sizes (mobile, tablet, desktop), preventing layout breaking or text overlap.

- **c. Form validation and error prompts**  
  Implements JavaScript validation on login and registration forms to ensure data completeness and format correctness before sending a request to the backend.

- **d. Dynamic page updates based on backend response**  
  Updates the interface based on backend API responses (e.g., successful login redirects to the cart page; failed login displays an error message and stays on the login page).

- **e. Payment integration and token generation**  
  Integrates a third-party payment SDK to build a payment form on the frontend. It generates a token and sends it to the backend for payment authorization.

- **f. Shopping cart and trip selection UI**  
  Uses JavaScript DOM manipulation to allow users to choose destinations and dates for their trips. Selected data is temporarily stored on the page before submission.

---

### 🧩 Back-End Features

- **a. Fetch and parse government JSON API for attractions**  
  Uses Python to retrieve and parse open JSON data, store it in a MySQL database, and provide APIs for the frontend to access attraction information.

- **b. User registration and login authentication**  
  Receives account credentials from the frontend, checks against the database, and returns login status.

- **c. JWT/Session-based login state management**  
  Upon successful login, generates a session or JWT token to track login state and verify user identity in protected APIs.

- **d. Order processing for shopping cart and trips**  
  Stores user-selected attractions, dates, and order information in the database, completing the trip booking process.

- **e. Third-party payment integration**  
  Receives a payment token from the frontend, sends a payment request to the third-party provider, processes the response, and records the transaction result.

- **f. Unified error handling and API response structure**  
  All backend API responses follow a standardized format (e.g., `{"ok": true}` or `{"error": "Invalid data"}`), making it easier for the frontend to handle cases like not logged in, payment failure, or input errors.

