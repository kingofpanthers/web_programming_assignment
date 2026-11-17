document.querySelector('#todo').addEventListener('submit', event => {
    event.preventDefault();
    const input = document.querySelector('#task');
    if (!input.value.trim()) return;

    const li = document.createElement('li');
    const label = document.createElement('label');
    const check = document.createElement('input');
    const text = document.createElement('span');

    check.type = 'checkbox';
    text.textContent = ' ' + input.value.trim();
    check.onchange = () => text.classList.toggle('done', check.checked);
    label.append(check, text);
    li.append(label);
    document.querySelector('#tasks').append(li);
    input.value = '';
    input.focus();
});
