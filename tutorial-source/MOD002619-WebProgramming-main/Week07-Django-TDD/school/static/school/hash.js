let latest = 0;
let timer;

document.querySelector('#id_text').addEventListener('input', () => {
    const version = ++latest;
    clearTimeout(timer);

    // Wait briefly so typing does not send a request for every letter.
    timer = setTimeout(async () => {
        const result = document.querySelector('#quickhash');
        try {
            const response = await fetch('/quickhash/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    text: document.querySelector('#id_text').value
                })
            });
            const data = await response.json();

            // Ignore an older reply if the user has already typed more text.
            if (version === latest) {
                result.textContent = response.ok ? data.hash : data.error;
            }
        } catch {
            if (version === latest) {
                result.textContent = 'Preview unavailable. Use Save hash to continue.';
            }
        }
    }, 200);
});
