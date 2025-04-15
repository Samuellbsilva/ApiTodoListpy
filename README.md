# ✅ ApiTodoListpy

**ApiTodoListpy** é uma **API RESTful** desenvolvida com **Flask** e **SQLite**, projetada para o gerenciamento eficiente de tarefas (To-Do List).

Ela oferece funcionalidades completas para:

- 📌 Criar, listar, atualizar e excluir tarefas  
- 📊 Acompanhar o progresso com estatísticas em tempo real  
- 📝 Exportar um relatório completo em **PDF**

A API utiliza **SQLAlchemy** como ORM para abstração do banco de dados e armazena informações como:

- Título da tarefa  
- Status (concluída ou pendente)  
- Data de criação e atualização (timestamps)

---

## 🚀 Funcionalidades e Rotas

| Método | Rota                  | Descrição                                  |
|--------|-----------------------|--------------------------------------------|
| GET    | `/tarefas`            | 🔍 Lista todas as tarefas                   |
| POST   | `/tarefas`            | ➕ Cria uma nova tarefa                     |
| PUT    | `/tarefas/<id>`       | 🔁 Atualiza uma tarefa existente           |
| DELETE | `/tarefas/<id>`       | ❌ Remove uma tarefa pelo ID               |
| GET    | `/tarefas/estatisticas` | 📊 Retorna estatísticas de tarefas       |
| GET    | `/exportar/pdf`       | 🖨️ Gera e baixa um PDF com tarefas + stats |

---

## 📦 Requisitos

- Python 3.x  
- Flask  
- Flask SQLAlchemy  
- ReportLab

### 📥 Instalação

Clone o repositório e instale os pacotes necessários:

```bash
pip install flask flask_sqlalchemy reportlab
