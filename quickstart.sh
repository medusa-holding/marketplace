#!/bin/bash

# Medusa Marketplace - Script de Inicialização Rápida
# Este script automatiza a configuração inicial do projeto

echo "==================================="
echo "  Medusa Marketplace - Setup"
echo "==================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado! Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado! Por favor, instale o pip."
    exit 1
fi

echo "✅ pip3 encontrado"

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Verifica se .env existe, se não, cria do exemplo
if [ ! -f ".env" ]; then
    echo "⚙️  Criando arquivo de configuração .env..."
    cp .env.example .env
    echo "📝 Por favor, edite o arquivo .env com suas configurações"
else
    echo "✅ Arquivo .env já existe"
fi

# Executa migrações
echo "🗄️  Executando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

# Pergunta se deseja criar superusuário
echo ""
echo "Deseja criar um usuário administrador (superuser)?"
echo "Isso permitirá acessar o painel admin do Django."
read -p "Criar superuser? (s/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "👤 Criando superusuário..."
    python manage.py createsuperuser
fi

# Finalização
echo ""
echo "==================================="
echo "  🎉 Setup concluído com sucesso!"
echo "==================================="
echo ""
echo "Para iniciar o servidor de desenvolvimento:"
echo "  $ source venv/bin/activate"
echo "  $ python manage.py runserver"
echo ""
echo "Acesse: http://127.0.0.1:8000/"
echo "Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "🚀 Bem-vindo ao Medusa Marketplace!"