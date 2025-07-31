# 📦 CHANGELOG – StormRaffle

> Todas as mudanças notáveis do projeto são documentadas neste arquivo.

---

## [v0.1.0] - 2025-07-31

🎯 Initial MVP completed after a focused 13-day sprint.

### Added
- Public listing of raffles (unauthenticated access)
- User auth: sign-up, login, logout
- Ticket purchase flow with Pix payment info
- Admin interface to confirm payments and draw winners
- Creator-only restriction on raffle drawing
- User dashboard with participated raffles
- Pre-commit validation and test execution

### Improved
- UX flows and interface consistency
- Admin panel with raffle/ticket management
- Code structure and module separation

---

## [Upcoming]

### Planned
- QR code Pix integration
- Automated payment confirmation
- Marketing campaign module
- Enhanced mobile experience

---
## [0.1.0] – 2025-07-25
### 🎬 MVP lançado com sucesso (Locked in Adamantium)

#### 🆕 Features
- [x] Registro de usuários com `username`, `DDD`, e `mobile_number`
- [x] Criação automática de `UserProfile` com `signals.py`
- [x] Validação de duplicidade amigável (username e telefone)
- [x] Login/Logout com mensagens emocionais e personalizadas
- [x] Dashboard para usuários autenticados
- [x] Criação de rifas com upload de múltiplas imagens
- [x] Armazenamento de imagens em `/media/raffle_images/`
- [x] Slideshow cinematográfico com Bootstrap (carousel)
- [x] Compra de bilhetes com feedback visual
- [x] Validação de status e pagamento antes do sorteio
- [x] Sorteio com registro do vencedor e notificação
- [x] Painel admin mostrando ganhadores e status de envio
- [x] Integração total com painel staff
- [x] Sistema de status da rifa: `draft`, `published`, `closed`
- [x] Mensagens de alerta para rifas não publicadas
- [x] Layout mobile-first com Bootstrap 4

#### 🔧 Ajustes e Melhorias
- [x] Refatoração do `forms.py` para suportar múltiplas imagens
- [x] Divisão modular de modelos (ex: `raffle_image.py`)
- [x] Correção do loop infinito no logout (auth.py)
- [x] Template `sign_up.html` totalmente funcional
- [x] Integração da `guard clause` para controle de fluxos críticos
- [x] Testes via shell confirmando integridade de `UserProfile`

#### ❗ Conhecidos / MVP Limitations
- [ ] Sistema de pagamento ainda será integrado
- [ ] Envio de mensagens via WhatsApp é manual
- [ ] Dashboard financeiro/admin em construção
- [ ] Sem tela de “editar perfil” no momento
- [ ] Sem múltiplos organizadores (modo SaaS ainda será ativado)

---

## 🔮 Próximas Versões Planejadas

- [0.2.0] – Integração de Pagamentos + Painel de Vendas
- [0.3.0] – Modo SaaS com múltiplos organizadores
- [0.4.0] – Mensageria integrada com WhatsApp / Email
- [1.0.0] – Lançamento Oficial SaaS (com suporte multi-tenant)

---

## 🎖️ WarBrothers Sprint Log

```text
Dias de Sprint:        10
Linhas de Código:      +7.500 (est)
Páginas de WARLOG.docx: +300
Erros Críticos:        0 no Deploy MVP
Uptime local:          100%

