document.addEventListener('DOMContentLoaded', function() {
  // Guardar comentario por AJAX
  const commentForm = document.getElementById('comment-form');
  // función para obtener csrftoken (reutilizable)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  // intentar obtener CSRF desde cookie, si no, usar el input oculto en el form
  let csrftoken = getCookie('csrftoken');
  if (!csrftoken) {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) csrftoken = csrfInput.value;
  }
  if (commentForm) {
    commentForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(commentForm);
      const endpoint = commentForm.dataset.url || commentForm.action;
      // Asegurar que el campo 'action' esté presente en FormData (algunos navegadores no lo incluyen automáticamente)
      if (!formData.get('action')) {
        formData.append('action', 'save_comment');
      }
      fetch(endpoint, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken,
        },
        body: formData
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        if (data.success) {
          // Agregar el comentario al listado
          const commentsList = document.getElementById('comments-list');
          if (commentsList) {
            const li = document.createElement('li');
            li.style.padding = '0.5rem 0';
            li.style.borderBottom = '1px solid rgba(255,255,255,0.03)';
            li.innerHTML = `<div style='color:#93c5fd; font-weight:600;'>${data.author} <span style='color:#94a3b8; font-weight:400;'>— ${data.timestamp}</span></div><div style='color:#cbd5e1; margin-top:0.25rem;'>${data.text}</div>`;
            commentsList.prepend(li);
          }
          commentForm.reset();
        } else if (data.error) {
          alert(data.error);
        }
      })
      .catch(err => {
        console.error('Error saving comment:', err);
        alert('Ocurrió un error al guardar el comentario. Revisa la consola para más detalles.');
      });
    });
  }

  // Modal de confirmación para finalizar diagnóstico
  const finalizeBtn = document.getElementById('finalize-btn');
  if (finalizeBtn) {
    finalizeBtn.addEventListener('click', function(e) {
      e.preventDefault();
      document.getElementById('finalize-modal').style.display = 'flex';
    });
  }
  // Botón cerrar modal
  const closeModalBtn = document.getElementById('close-modal-btn');
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', function() {
      document.getElementById('finalize-modal').style.display = 'none';
    });
  }
  // Botón no
  const noBtn = document.getElementById('finalize-no-btn');
  if (noBtn) {
    noBtn.addEventListener('click', function() {
      document.getElementById('finalize-modal').style.display = 'none';
    });
  }
  // Botón sí
  const yesBtn = document.getElementById('finalize-yes-btn');
  if (yesBtn) {
    yesBtn.addEventListener('click', function() {
      // Enviar POST para finalizar diagnóstico
      fetch(finalizeBtn.dataset.url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken,
        },
        body: `patient_id=${encodeURIComponent(finalizeBtn.dataset.patient)}&action=finalize_diag`
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        if (data.success) {
          document.getElementById('finalize-modal').style.display = 'none';
          const msgEl = document.getElementById('finalize-message');
          if (msgEl) {
            msgEl.style.display = 'block';
            msgEl.innerText = data.success;
          }
          const cf = document.getElementById('comment-form');
          if (cf) cf.style.display = 'none';
        } else if (data.error) {
          alert(data.error);
        }
      })
      .catch(err => {
        console.error('Error finalizing diagnosis:', err);
        alert('Ocurrió un error al finalizar el diagnóstico. Revisa la consola para más detalles.');
      });
    });
  }
});
