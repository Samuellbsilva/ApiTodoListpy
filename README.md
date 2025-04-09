# ApiTodoListpy

**ApiTodoListpy** é uma API REST desenvolvida com **Flask** e **SQLite**, ideal para gerenciamento de tarefas (To-Do).  

Ela permite **criar, listar, atualizar, excluir e acompanhar o progresso de tarefas**, além de oferecer funcionalidades extras como **exportação em PDF** e **estatísticas em tempo real**.

A aplicação utiliza **SQLAlchemy** como ORM e organiza as tarefas com campos como:

- Título  
- Status (feito ou não)  
- Timestamps de criação e atualização

Com a rota `/exportar/pdf`, o usuário pode gerar um **relatório completo das tarefas em formato PDF**, incluindo **estatísticas de conclusão**.

---

### Rotas disponíveis

- `GET /tarefas` - Lista todas as tarefas  
- `POST /tarefas` - Cria uma nova tarefa  
- `PUT /tarefas/<id>` - Atualiza uma tarefa existente  
- `DELETE /tarefas/<id>` - Deleta uma tarefa  
- `GET /tarefas/estatisticas` - Retorna estatísticas de conclusão  
- `GET /exportar/pdf` - Gera um PDF com todas as tarefas e estatísticas  

---

### Requisitos

- Python 3.x  
- Flask  
- Flask SQLAlchemy  
- ReportLab

Instale os requisitos com:

```bash
pip install flask flask_sqlalchemy reportlab
