# Tô Rifando – Online Raffle Portal [![GitHub Release](https://img.shields.io/github/v/release/srcsoftwareengineer/raffle-portal?label=Release&style=flat-square)](https://github.com/srcsoftwareengineer/raffle-portal/releases/latest)

🌎 English Version | [🇧🇷 Versão em Português](./README-pt.md)

> Version: **MVP 0.1 – Locked in Adamantium**  
> Release Date: `2025-07-27`
---

## 🌪️ Overview

**StormRaffle** is a complete system for managing online raffles.  
Developed as a robust MVP, the project delivers the full cycle: raffle creation, image uploads, ticket sales, drawing, and winner notification.

Inspired by real entrepreneurial experience, StormRaffle was built on solid software engineering practices, MVP principles, and is ready to scale as a **SaaS platform**.

---

## ✅ Delivered Features

### 🔐 Authentication & Profiles
- Registration with custom fields: area code (DDD) and mobile number  
- Automatic profile creation with `signals.py`  
- Validations and user-friendly messages  

### 🎟️ Raffles
- Create raffles with multiple images  
- Upload and secure storage in `/media/raffle_images/`  
- Cinematic slideshow (Bootstrap Carousel)  

### 🛒 Ticket Purchase
- Intuitive interface to choose and purchase numbers  
- Visual feedback for purchased tickets  
- Integration with payment status  

### 🎉 Drawing
- Admin panel to draw winners  
- Stores the date and winning ticket number  
- Friendly winner message  

### 📢 Admin & UX
- Smart raffle status: draft / published / closed  
- Quick action buttons: publish, draw  
- Warning for unpublished raffles  
- Motivational and emotional tone in messages  

---

## 💡 Tech Stack

- **Backend**: Django 4+  
- **Frontend**: Bootstrap 4, HTML5  
- **Database**: SQLite (MVP), ready for PostgreSQL  
- **Auth & Profiles**: Django Auth + UserProfile (area code, mobile)  
- **Files**: Upload to FileSystem `/media/`  

---

## 🚀 Deploy

> Production environment already defined:  
- Create superuser: `python manage.py createsuperuser`  
- Admin panel:  
- URL: `/admin/`
