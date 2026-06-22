# 🏭 IoT Smart Warehouse Access & Inventory Control System

An IoT-based smart warehouse management system designed to improve **security, traceability, and inventory control** in industrial environments. The system replaces manual paper-based processes with a fully digital solution integrating **biometrics, RFID, computer vision, and real-time cloud synchronization**.

---

## 📌 Overview

This project was developed as a thesis to optimize warehouse operations in a high-value spare parts environment.

It focuses on:
- Secure and automated access control
- Real-time inventory tracking
- Reduction of human error in warehouse records
- Full traceability of personnel and material movement

The system integrates **IoT hardware + cloud software + automation mechanisms** into a unified platform.

---

## ⚙️ Key Features

### 🔐 Access Control
- Fingerprint authentication for authorized personnel
- RFID-based entry system
- Role-based access (Admin / Operator)
- Automated door control using a linear actuator

### 📸 Monitoring & Security
- Camera captures entry events automatically
- Laser barrier sensor counts entries/exits
- Real-time alerts for suspicious activity

### 📦 Inventory Management
- QR-based product identification system
- Automated stock updates in real time
- Digital replacement of paper-based withdrawal orders

### ☁️ Cloud Integration
- Firebase Realtime Database
- Instant synchronization across devices
- Centralized logging of warehouse activity

### 🔔 Notifications
- Alerts for:
  - Unauthorized access attempts
  - Multiple-entry detection
  - Low / zero stock events

---

## 🧠 System Architecture

### Hardware Layer
- Raspberry Pi 3 B+
- RFID Reader
- Fingerprint Sensor
- Laser Barrier Sensor
- Camera Module
- Linear Actuator (door mechanism)

### Processing Layer
- Python-based control system
- Sensor validation logic
- Event handling and automation

### Cloud Layer
- Firebase Realtime Database
- Inventory records
- Access logs
- Image storage references

---

## 🏗️ Mechanical Design

- Door automation using a **linear actuator system**
- Designed based on force, torque, and displacement calculations
- Optimized for industrial warehouse door dimensions
- Safety-aware opening mechanism

---

## 💻 Software Components

- Python (core IoT logic)
- Firebase integration (real-time data sync)
- QR-based inventory application
- User system:
  - Admin (full control)
  - Operator (limited permissions)

---

## 🧪 System Workflow

1. User requests entry via RFID or fingerprint
2. System validates identity against database
3. Door opens automatically using actuator
4. Camera captures entry image
5. Laser sensor tracks entry count
6. Event is logged in Firebase
7. Inventory updates in real time via QR system

---

## 📊 Results & Impact

- Reduced inventory inconsistencies
- Improved traceability of warehouse operations
- Faster and safer access during night shifts
- Elimination of manual paper-based workflows
- Increased operational transparency and security

---

## 🚀 Future Improvements

- AI-based anomaly detection inside warehouse
- Computer vision for object recognition
- Predictive inventory forecasting using ML
- Admin dashboard for access control management
- Replacement of hinged door with sliding mechanism

---

## 📷 System Preview

A visual demonstration of the IoT warehouse system, including hardware prototype and software application workflow.

---

### 🧠 Full System Prototype

Overview of the complete IoT system installed on the warehouse door prototype.

![System Prototype](assets/images/system_prototype.jpg)

---

### 🚪 Door Automation System

Linear actuator-based automatic door opening mechanism.

![Door Closed](assets/images/door_closed.jpg)
![Door Open](assets/images/door_open.jpg)

🖼️ *Shows mechanical transition between closed and open states.*

---

### 🔐 Access Control System

RFID and fingerprint authentication panel used for secure entry.

![Access Panel](assets/images/access_panel.jpg)

---

### 📸 Entry Monitoring (Camera System)

Camera module capturing entry events for traceability.

![Camera Module](assets/images/camera_module.jpg)

---

### 📦 Inventory Management App (GIF Demo)

Real-time QR-based inventory system with automatic stock updates.

![App Demo GIF](assets/gifs/app_demo.gif)

---

### 📊 Inventory Update Flow (GIF)

Shows product scan → validation → stock update in real time.

![Inventory Flow GIF](assets/gifs/inventory_flow.gif)

---

### ☁️ Firebase Real-Time Database

Cloud backend storing logs, inventory, and access records.

![Firebase DB](assets/images/firebase_db.jpg)

---

### 🔔 System Notifications

Automated alerts for access events and stock inconsistencies.

![Notifications](assets/images/notifications.jpg)
