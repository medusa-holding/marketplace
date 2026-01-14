# Guia de Implantação - Medusa Marketplace

> Instruções para implantar o Medusa Marketplace em produção

## 📋 Pré-requisitos

### Servidor
- Ubuntu 20.04+ ou Debian 10+
- Python 3.8+
- PostgreSQL 12+
- Nginx
- Git
- Supervisor (opcional, para processos em background)

### Domínio
- Domínio próprio (ex: medusa.co.mz)
- Certificado SSL (Let's Encrypt recomendado)

## 🔧 Configuração do Servidor

### 1. Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependências
```bash
sudo apt install -y python3-pip python3-venv python3-dev postgresql nginx supervisor git
```

### 3. Configurar PostgreSQL
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE medusa_db;
CREATE USER medusa_user WITH PASSWORD 'sua_senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE medusa_db TO medusa_user;
\q
```

### 4. Criar Usuário de Aplicação
```bash
sudo useradd -m medusa
sudo usermod -aG sudo medusa
sudo su - medusa
```

## 📥 Implantação da Aplicação

### 1. Clonar Projeto
```bash
cd /home/medusa
git clone https://github.com/medusa-holding/marketplace.git
cd marketplace
```

### 2. Configurar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Para produção
```

### 3. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
nano .env
```

Edite o arquivo `.env`:
```env
SECRET_KEY= sua-super-chave-secreta-muito-longa-aqui
DEBUG=False
ALLOWED_HOSTS=medusa.co.mz,www.medusa.co.mz

# PostgreSQL
DB_NAME=medusa_db
DB_USER=medusa_user
DB_PASSWORD=sua_senha_forte_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 4. Configurar Settings para Produção
Crie `settings_production.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['medusa.co.mz', 'www.medusa.co.mz']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Static files
STATIC_ROOT = '/home/medusa/staticfiles/'

# Media files
MEDIA_ROOT = '/home/medusa/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 5. Executar Migrações
```bash
export DJANGO_SETTINGS_MODULE=medusa_marketplace.settings_production
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Criar Superusuário
```bash
python manage.py createsuperuser
```

## 🌐 Configurar Nginx

Crie o arquivo de configuração:
```bash
sudo nano /etc/nginx/sites-available/medusa
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name medusa.co.mz www.medusa.co.mz;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/medusa/marketplace;
    }
    
    location /media/ {
        root /home/medusa/marketplace;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/medusa.sock;
    }
}
```

Ative o site:
```bash
sudo ln -s /etc/nginx/sites-available/medusa /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 🔥 Configurar Gunicorn

Crie o arquivo de serviço:
```bash
sudo nano /etc/systemd/system/medusa.service
```

Conteúdo:
```ini
[Unit]
Description=Medusa Marketplace
After=network.target

[Service]
User=medusa
Group=www-data
WorkingDirectory=/home/medusa/marketplace
Environment="DJANGO_SETTINGS_MODULE=medusa_marketplace.settings_production"
ExecStart=/home/medusa/marketplace/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/medusa.sock medusa_marketplace.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Inicie o serviço:
```bash
sudo systemctl start medusa
sudo systemctl enable medusa
```

## 🔒 Configurar SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d medusa.co.mz -d www.medusa.co.mz
```

## 📊 Configurar Supervisor (Opcional)

Para processos em background (notificações, e-mails, etc.):

```bash
sudo nano /etc/supervisor/conf.d/medusa.conf
```

```ini
[program:medusa]
command=/home/medusa/marketplace/venv/bin/gunicorn --workers 3 --bind unix:/run/medusa.sock medusa_marketplace.wsgi:application
directory=/home/medusa/marketplace
user=medusa
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/medusa/logs/gunicorn.log
environment=DJANGO_SETTINGS_MODULE="medusa_marketplace.settings_production"
```

## 🗄️ Backup do Banco de Dados

Crie um script de backup:
```bash
sudo nano /home/medusa/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump medusa_db > /home/medusa/backups/backup_$DATE.sql
gzip /home/medusa/backups/backup_$DATE.sql
# Remove backups com mais de 7 dias
find /home/medusa/backups -name "backup_*.sql.gz" -mtime +7 -delete
```

Torne executável e agende:
```bash
chmod +x /home/medusa/backup.sh
sudo crontab -e
```

Adicione:
```
0 2 * * * /home/medusa/backup.sh
```

## 🚀 Comandos de Manutenção

### Verificar status
```bash
sudo systemctl status medusa
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Logs
```bash
# Logs da aplicação
sudo journalctl -u medusa -f

# Logs do nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Reiniciar serviços
```bash
sudo systemctl restart medusa
sudo systemctl restart nginx
```

### Atualizar aplicação
```bash
cd /home/medusa/marketplace
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart medusa
```

## 🔍 Monitoramento

### Uso de Recursos
```bash
htop
df -h
free -h
```

### Conexões
```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Permission denied (publickey):**
   ```bash
   sudo chmod 755 /home/medusa
   sudo chown medusa:medusa /home/medusa/marketplace -R
   ```

2. **502 Bad Gateway:**
   ```bash
   sudo systemctl restart medusa
   sudo systemctl restart nginx
   ```

3. **Database connection failed:**
   ```bash
   sudo systemctl status postgresql
   sudo systemctl restart postgresql
   ```

4. **Static files não carregam:**
   ```bash
   python manage.py collectstatic --noinput
   sudo systemctl restart medusa
   ```

## 📈 Performance

### Ajustes no Gunicorn
Edite `/etc/systemd/system/medusa.service`:
```ini
ExecStart=/home/medusa/marketplace/venv/bin/gunicorn --workers 5 --worker-class gevent --worker-connections 1000 --bind unix:/run/medusa.sock medusa_marketplace.wsgi:application
```

### Cache
Adicione Redis para cache:
```bash
sudo apt install redis-server
pip install django-redis
```

### CDN
Configure Cloudflare ou AWS CloudFront para assets estáticos.

---

**Nota:** Este guia assume um ambiente Ubuntu/Debian. Ajuste conforme necessário para outros sistemas operacionais.