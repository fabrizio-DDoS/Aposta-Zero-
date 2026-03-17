# ApostaZero 🎯 — Simulador de Apostas sem Dinheiro Real

SafeBet é uma plataforma de apostas simuladas que utiliza dados reais de mercados de previsão, mas com **moeda totalmente fictícia**, com o objetivo de **reduzir o vício em apostas com dinheiro real**.

## ⚠️ Propósito

Este projeto foi criado com um objetivo claro:

> Mostrar, na prática, que apostar leva à perda de dinheiro na maioria dos casos — sem que o usuário precise perder dinheiro real.

O sistema funciona como uma alternativa segura para pessoas que têm o hábito de apostar.

---

## 🚀 Funcionalidades

- ✅ Criação de conta e autenticação de usuários  
- 📊 Visualização de mercados reais (via API)  
- 🎲 Sistema de apostas com moeda virtual  
- 💰 Saldo inicial fictício (ex: 1000 créditos)  
- 📉 Histórico de apostas  
- 🏆 Ranking de usuários  
- ⚠️ Alertas constantes sobre riscos do jogo  
- 📊 Estatísticas reais de desempenho (ganhos/perdas)

---

## 🧱 Tecnologias Utilizadas

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Banco de Dados
- SQLite

### Integrações
- API de mercados de previsão (ex: Polymarket)

---

## 📂 Estrutura do Projeto
project/
│
├── app.py
├── database.db
│
├── /templates
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── market.html
│
├── /static
│ ├── style.css
│ ├── script.js

---

## 🗄️ Modelagem do Banco de Dados

### Users
- id
- username
- email
- password_hash
- balance
- created_at

### Markets
- id
- title
- description
- status
- created_at

### Options
- id
- market_id
- name
- odds

### Bets
- id
- user_id
- option_id
- amount
- created_at

---

## 🔄 Fluxo de Funcionamento

1. Usuário cria uma conta  
2. Recebe saldo fictício inicial  
3. Visualiza mercados disponíveis  
4. Realiza apostas com créditos virtuais  
5. Resultados são calculados com base nos dados do mercado  
6. Ranking e histórico são atualizados  

---

## ⚠️ Aviso Importante

Este projeto:

- ❌ NÃO utiliza dinheiro real  
- ❌ NÃO permite saques  
- ❌ NÃO incentiva apostas financeiras  

Mensagens educativas são exibidas ao longo da plataforma para conscientizar sobre:

- riscos do vício em jogos  
- perdas financeiras  
- impacto social e familiar  

---

## 🧠 Filosofia do Projeto

SafeBet não é apenas um site — é um experimento:

> Se as pessoas puderem sentir a experiência de apostar sem risco, será que elas percebem o custo real do jogo?

---

## 🛠️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/safebet.git
cd safebet
