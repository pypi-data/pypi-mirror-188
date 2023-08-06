(() => {
  const sortables = document.querySelectorAll('.sortable');
  sortables.forEach((sortable) => {
    new Sortable(sortable, {
      animation: 150,
      ghostClass: 'bg-info',
      handle: '.handle'
    })
  })

  // -------------- Modals --------------
  // Many thanks to Benoit Blanchon: https://blog.benoitblanchon.fr/django-htmx-modal-form/
  let modal = new bootstrap.Modal(document.getElementById('modal'))  // hide the dialog at empty response.
  // This maybe additionally could check for status_core==204
  htmx.on('htmx:beforeSwap', (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id === 'dialog' && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })
  htmx.on('htmx:afterSwap', (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id === 'dialog') {
      modal.show()
    }
  })

  // set focus to first not-hidden input on modal (hidden = csrf_input, etc)
  htmx.on('shown.bs.modal', (e) => {
    const modal = document.getElementById('modal')
    const inputs = modal.querySelectorAll('input:not([type="hidden"])');
    const textareas = modal.querySelectorAll('textarea:not([type="hidden"])');
    // not pretty, but works.
    // first try textareas
    for(const input of textareas) {
      if (!input.hidden) {
        input.focus()
        return
      }
    }
    // then input fields
    for(const input of inputs) {
      if (!input.hidden) {
        input.focus()
        return
      }
    }
  })

  // empty the dialog on hide
  htmx.on('hidden.bs.modal', () => {
    document.getElementById('dialog').innerHTML = ''
  })

  // // Litepicker
  // const litepickers = document.querySelectorAll('.textinput');
  // console.log("registering ",litepickers)
  // litepickers.forEach((litepicker) => {
  //   new Litepicker({
  //     element: litepicker
  //   });
  // })

  // update all .current-time tags system-wide with - who thought that?!? - the current time!
  function updateCurrentTime() {
    document.querySelectorAll(".current-time").forEach((element) =>  {
      element.innerText = new Date().toLocaleTimeString() // [], {hour: '2-digit', minute:'2-digit'}
    })
  }
  setInterval(updateCurrentTime, 1000);

})();
