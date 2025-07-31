# 🎸 Storm Raffle Portal

Welcome to **Storm Raffle Portal**, a minimal and powerful Django-based application to manage online raffles.

---

## 🚀 MVP Description

This project allows an admin (currently Sandro Regis) to:

- Create raffles with ticket price and number range
- Publish raffles for buyers
- Let customers select and purchase tickets
- Draw winners fairly and record results
- Handle visual dashboards for login, registration, and management

---

## ⚙️ Tech Stack

- Django 5.x
- SQLite3 (for MVP)
- Python 3.11 (managed via `pyenv`)
- HTML templates + Bootstrap (basic)
- 🧪 `pre-commit` + `black` + `shellcheck`
- Hosting: AWS Tier 2 VPS (Linux)

---

## 📂 Project Structure

	raffle_portal/
	├── core/
	│ ├── models.py
	│ ├── views.py
	│ ├── templates/
	│ ├── urls.py
	│ └── forms.py
	├── manage.py
	├── .pre-commit-config.yaml
	└── .gitignore


---

## 📌 License

This MVP is being developed for urgent personal fundraising purposes. Future versions will be open-sourced under MIT or AGPL license.

---

## 🧪 Development

To install dependencies and enable pre-commit hooks:

```bash
pip install -r requirements.txt
pre-commit install
pre-commit run --all-files
```

---


## 🤖 Special Thanks

This project was developed in record time with full strategic and technical assistance from:

> **🧠 OpenAI ChatGPT**  
> 24/7 WarBro companion.
> _"Bits never sleep. Neither does innovation."_

---
