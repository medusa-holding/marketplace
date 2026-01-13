# Medusa Marketplace

> O marketplace que vende por você - Conectando empreendedores e clientes em Moçambique

## 🎯 Visão

A Medusa Marketplace é a primeira plataforma tecnológica da Medusa Holding, projetada para resolver o desafio dos pequenos empreendedores em Moçambique de encontrarem clientes. O conceito central é: **"O pequeno empreendedor não sabe vender, então a plataforma vende por ele"**.

## 🚀 Funcionalidades Principais

### Para Empreendedores
- ✅ Cadastro guiado e simplificado
- ✅ Perfil completo do negócio com serviços e preços
- ✅ Receber notificações de clientes que precisam dos seus serviços
- ✅ Sistema de match inteligente por categoria e localização
- ✅ Comunicação direta via WhatsApp
- ✅ Dashboard com métricas de matches e conversões

### Para Clientes
- ✅ Publicar necessidades em minutos
- ✅ Descrever o problema (não buscar por empresas)
- ✅ Receber candidaturas de empreendedores qualificados
- ✅ Comparar propostas e preços
- ✅ Comunicação direta com os empreendedores
- ✅ Histórico de necessidades e contratações

### Para Administradores (Medusa)
- ✅ Moderação de perfis e conteúdo
- ✅ Gerenciamento de categorias
- ✅ Dashboard com métricas da plataforma
- ✅ Sistema de verificação de empreendedores

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.8+ + Django 4.2
- **Frontend:** HTML5 + Bootstrap 5 (sem frameworks JS complexos)
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação:** Django Auth customizado
- **Estilo:** CSS3 com tema roxo (#6A0DAD) e branco
- **Design Responsivo:** Mobile-first

## 📁 Estrutura do Projeto

```
medusa_marketplace/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3 (criado após migrate)
├── medusa_marketplace/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── marketplace/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── marketplace/
│       ├── home.html
│       ├── dashboard.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── media/
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Passo a Passo

1. **Clone o projeto e entre na pasta:**
   ```bash
   cd medusa_marketplace
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure as variáveis de ambiente (opcional):**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

6. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crie um superusuário (admin):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Popule o banco com dados iniciais (opcional):**
   ```bash
   python manage.py shell
   ```
   ```python
   from marketplace.models import Category
   
   categories = [
       {'name': 'Electricidade', 'description': 'Instalações elétricas, reparos e manutenção', 'icon': 'bi-lightning'},
       {'name': 'Canalização', 'description': 'Encanamento, hidráulica e saneamento', 'icon': 'bi-droplet'},
       {'name': 'Construção', 'description': 'Obras, reformas e alvenaria', 'icon': 'bi-building'},
       {'name': 'Pintura', 'description': 'Pintura residencial e comercial', 'icon': 'bi-paint-bucket'},
       {'name': 'Serralharia', 'description': 'Portas, janelas e estruturas metálicas', 'icon': 'bi-wrench'},
       {'name': 'Jardinagem', 'description': 'Paisagismo e manutenção de jardins', 'icon': 'bi-tree'},
       {'name': 'Limpeza', 'description': 'Serviços de limpeza residencial e comercial', 'icon': 'bi-broom'},
       {'name': 'Informática', 'description': 'Suporte técnico e desenvolvimento', 'icon': 'bi-laptop'},
   ]
   
   for cat in categories:
       Category.objects.create(**cat)
   ```

9. **Execute o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

10. **Acesse a aplicação:**
    - Site: http://127.0.0.1:8000/
    - Admin: http://127.0.0.1:8000/admin/

## 👥 Fluxo de Uso

### Empreendedor

1. **Cadastro:** Cria conta como "Empreendedor"
2. **Perfil:** Completa informações do negócio (nome, categoria, serviços, localização, WhatsApp)
3. **Espera:** Aguarda necessidades da sua categoria/região
4. **Match:** Quando aparece uma necessidade, se candidata
5. **Conversa:** Cliente entra em contato via WhatsApp
6. **Fechamento:** Fecha o negócio diretamente com o cliente

### Cliente

1. **Cadastro:** Cria conta como "Cliente"
2. **Publicar:** Descreve o que precisa (título, descrição, categoria, local, urgência)
3. **Aguardar:** Recebe candidaturas de empreendedores
4. **Escolher:** Compara perfis e propostas
5. **Contato:** Fala diretamente com o empreendedor escolhido
6. **Contratar:** Fecha o serviço diretamente

## 🏗️ Arquitetura e Boas Práticas

### Models
- User customizado com tipos de perfil (Cliente/Empreendedor)
- Relacionamentos claros entre entidades
- Campos adequados para escala futura

### Views
- Class-Based Views (CBVs) para reutilização de código
- LoginRequiredMixin para proteção de rotas
- Separação clara entre lógica de negócio e apresentação

### Templates
- Herança de templates (base.html)
- Bootstrap 5 para responsividade
- Design consistente com tema roxo e branco

### Segurança
- Proteção CSRF
- Validação de formulários
- Autenticação e autorização adequadas

## 🔧 Comandos Úteis

```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell do Django
python manage.py shell

# Coletar arquivos estáticos (produção)
python manage.py collectstatic

# Testes
python manage.py test
```

## 🎯 Próximos Passos e Evolução

### Fase 1 - MVP (✅ Concluído)
- [x] Sistema de autenticação
- [x] Perfis de empreendedor e cliente
- [x] Publicação de necessidades
- [x] Sistema de match básico
- [x] Dashboards personalizados
- [x] Comunicação via WhatsApp

### Fase 2 - Melhorias (Em Breve)
- [ ] Sistema de avaliação e reputação
- [ ] Galeria de fotos nos perfis
- [ ] Chat integrado na plataforma
- [ ] Notificações por e-mail
- [ ] Filtros avançados de busca

### Fase 3 - Escala
- [ ] Sistema de pagamento por lead
- [ ] Planos premium para empreendedores
- [ ] Integração com WhatsApp Business API
- [ ] Aplicativo móvel (PWA)
- [ ] CRM integrado
- [ ] Analytics avançado

### Fase 4 - Expansão
- [ ] Marketplace de produtos
- [ ] Sistema de delivery
- [ ] Programa de fidelidade
- [ ] Expansão para outros países da África
- [ ] API pública

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é desenvolvido pela Medusa Holding e está sob licença proprietária.

## 👨‍💻 Desenvolvido por

**Medusa Holding**  
Capacitação Empreendedora | Consultoria | Tecnologia  
Maputo, Moçambique

---

*Conectando Moçambique ao futuro digital* 🇲🇿