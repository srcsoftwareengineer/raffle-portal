# Tô Rifando – Online Raffle Portal [![GitHub Release](https://img.shields.io/github/v/release/srcsoftwareengineer/raffle-portal?label=Release&style=flat-square)](https://github.com/srcsoftwareengineer/raffle-portal/releases/latest)

> Versão: **MVP 0.1 - Locked in Adamantium**  
> Data de Lançamento: `25/07/2025`

---

## 🌪️ Visão Geral

**StormRaffle** é um sistema completo para gerenciamento de rifas online. Desenvolvido como um MVP robusto, o projeto entrega um ciclo completo: criação de rifas, upload de imagens, venda de bilhetes, sorteio e notificação de ganhadores.

Inspirado pela experiência real de empreender, StormRaffle foi criado com base em práticas sólidas de engenharia de software, princípios MVP e pronto para escalar como **SaaS**.

---

## ✅ Funcionalidades Entregues

### 🔐 Autenticação e Perfis
- Registro com campos personalizados: DDD e celular
- Criação automática de perfil com `signals.py`
- Validações e mensagens amigáveis

### 🎟️ Rifas
- Criação de rifas com múltiplas imagens
- Upload e armazenamento seguro em `/media/raffle_images/`
- Slideshow cinematográfico (Bootstrap Carousel)

### 🛒 Compra de Bilhetes
- Interface intuitiva para escolher e comprar números
- Feedback visual dos bilhetes comprados
- Integração com status de pagamento

### 🎉 Sorteio
- Painel administrativo para sortear vencedores
- Registro da data e do bilhete vencedor
- Mensagem amigável de ganhador

### 📢 Admin & UX
- Status inteligente das rifas: draft / published / closed
- Botões de ação rápida: publicar, sortear
- Aviso para rifas não publicadas
- Mensagens com tom emocional e motivacional

---

## 💡 Tech Stack

- **Backend**: Django 4+
- **Frontend**: Bootstrap 4, HTML5
- **Banco de Dados**: SQLite (MVP), pronto para PostgreSQL
- **Auth & Perfis**: Django Auth + UserProfile (DDD, celular)
- **Arquivos**: Upload para FileSystem `/media/`

---

## 🚀 Deploy

> Production environment already defined:  
- Create superuser: `python manage.py createsuperuser`  
- Admin panel:  
- URL: `/admin/`
