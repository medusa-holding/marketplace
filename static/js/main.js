/**
 * Medusa Marketplace - JavaScript Principal
 * Funcionalidades interativas da plataforma
 */

// Aguarda o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializa tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializa popovers do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Confirmação antes de deletar
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });
    
    // Confirmação antes de cancelar
    var cancelButtons = document.querySelectorAll('.btn-cancel');
    cancelButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja cancelar?')) {
                e.preventDefault();
            }
        });
    });
    
    // Formatação de telefone/WhatsApp
    var phoneInputs = document.querySelectorAll('input[name="whatsapp"], input[name="phone"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            var value = e.target.value.replace(/\D/g, '');
            if (value.length >= 9) {
                value = value.replace(/(\d{2})(\d{3})(\d{4})/, '$1 $2 $3');
            }
            e.target.value = value;
        });
    });
    
    // Animação de scroll suave para âncoras
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Mostrar/esconder senha
    var passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            var targetId = this.getAttribute('data-target');
            var input = document.querySelector(targetId);
            if (input) {
                if (input.type === 'password') {
                    input.type = 'text';
                    this.innerHTML = '<i class="bi bi-eye-slash"></i>';
                } else {
                    input.type = 'password';
                    this.innerHTML = '<i class="bi bi-eye"></i>';
                }
            }
        });
    });
    
    // Loading state para formulários
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Aguarde...';
            }
        });
    });
    
    // Preview de imagem no formulário
    var imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var preview = document.querySelector(this.getAttribute('data-preview'));
            if (preview && e.target.files && e.target.files[0]) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    preview.src = event.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    });
    
    // Contador de caracteres para textareas
    var textareas = document.querySelectorAll('textarea[data-maxlength]');
    textareas.forEach(function(textarea) {
        var maxLength = parseInt(textarea.getAttribute('data-maxlength'));
        var counter = document.createElement('small');
        counter.className = 'form-text text-muted';
        counter.textContent = maxLength + ' caracteres restantes';
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            var remaining = maxLength - this.value.length;
            counter.textContent = remaining + ' caracteres restantes';
            if (remaining < 10) {
                counter.className = 'form-text text-danger';
            } else {
                counter.className = 'form-text text-muted';
            }
        });
    });
    
    // Filtros dinâmicos
    var filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            var form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
    
    // Atualização de status via AJAX
    var statusUpdates = document.querySelectorAll('.status-update');
    statusUpdates.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            var url = this.getAttribute('data-url');
            var status = this.getAttribute('data-status');
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: status })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Erro ao atualizar status.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao atualizar status.');
            });
        });
    });
    
    // Verificação de novas mensagens (para matches)
    if (document.querySelector('.message-list')) {
        setInterval(checkNewMessages, 30000); // Verifica a cada 30 segundos
    }
    
    // Animação de entrada dos elementos
    var observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observa todos os cards e seções
    document.querySelectorAll('.card, .section, .dashboard-card').forEach(function(el) {
        observer.observe(el);
    });
});

// Função auxiliar para pegar cookie CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para verificar novas mensagens
function checkNewMessages() {
    var matchId = document.querySelector('.message-list').getAttribute('data-match-id');
    if (matchId) {
        fetch('/api/match/' + matchId + '/messages/unread/')
            .then(response => response.json())
            .then(data => {
                if (data.unread_count > 0) {
                    // Atualiza a lista de mensagens ou mostra notificação
                    location.reload();
                }
            })
            .catch(error => console.error('Error checking messages:', error));
    }
}

// Função para copiar texto para área de transferência
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Mostra feedback visual
        var tooltip = new bootstrap.Tooltip(document.body, {
            title: 'Copiado!',
            placement: 'top',
            trigger: 'manual'
        });
        tooltip.show();
        setTimeout(function() {
            tooltip.hide();
        }, 2000);
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Função para compartilhar via WhatsApp
function shareViaWhatsApp(text, url) {
    var message = encodeURIComponent(text + ' ' + url);
    window.open('https://wa.me/?text=' + message, '_blank');
}