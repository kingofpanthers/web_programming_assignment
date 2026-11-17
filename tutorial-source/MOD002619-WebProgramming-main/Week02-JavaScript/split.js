const form = document.querySelector('#split');
const items = document.querySelector('#items');

function addItem() {
    const row = document.createElement('div');
    row.className = 'card';

    const label = document.createElement('label');
    label.textContent = 'Menu item';
    const name = document.createElement('input');
    name.placeholder = 'e.g. Pasta';
    name.className = 'item-name';
    label.append(name);

    const priceLabel = document.createElement('label');
    priceLabel.textContent = 'Price (£)';
    const price = document.createElement('input');
    price.type = 'number';
    price.min = '0';
    price.step = '0.01';
    price.className = 'price';
    priceLabel.append(price);

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = 'Remove item';
    remove.onclick = () => row.remove();
    row.append(label, priceLabel, remove);
    items.append(row);
}

if (items) {
    document.querySelector('#add').onclick = addItem;
    addItem();
}

form.addEventListener('submit', event => {
    event.preventDefault();
    const errors = [];
    let cents = 0;
    const people = Number(document.querySelector('#people').value);

    if (!Number.isSafeInteger(people) || people < 1) {
        errors.push('Number of people must be a positive whole number.');
    }

    // Work in whole pennies when adding prices.
    if (items) {
        const rows = [...items.children];
        if (!rows.length) errors.push('Add at least one menu item.');

        rows.forEach((row, i) => {
            const input = row.querySelector('.price');
            const value = Number(input.value);
            if (!row.querySelector('.item-name').value.trim()) {
                errors.push(`Item ${i + 1} needs a name.`);
            }
            if (!input.value.trim() || !Number.isFinite(value) || value < 0) {
                errors.push(`Item ${i + 1} needs a valid non-negative price.`);
            } else {
                cents += Math.round(value * 100);
            }
        });
    } else {
        const input = document.querySelector('#bill');
        const value = Number(input.value);
        if (!input.value.trim() || !Number.isFinite(value) || value < 0) {
            errors.push('Enter a valid non-negative bill amount.');
        } else {
            cents = Math.round(value * 100);
        }
    }

    const total = Math.round(cents * (1 + Number(document.querySelector('#tip').value) / 100));
    if (!Number.isSafeInteger(total)) {
        errors.push('The bill is too large to calculate accurately.');
    }

    document.querySelector('#errors').textContent = errors.join(' ');
    const result = document.querySelector('#result');
    if (errors.length) {
        result.textContent = 'Please correct the inputs above.';
        return;
    }

    // Share leftover pennies so the payments add up to the exact total.
    const low = Math.floor(total / people);
    const extra = total % people;
    result.textContent = `Total with tip: £${(total / 100).toFixed(2)}. ` + (
        extra
            ? `${extra} person(s) pay £${((low + 1) / 100).toFixed(2)} and ${people - extra} pay £${(low / 100).toFixed(2)} to account for rounding.`
            : `Each person pays £${(low / 100).toFixed(2)}.`
    );
});
