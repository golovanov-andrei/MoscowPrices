function activateTab(name) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === name);
    });
    document.querySelectorAll('.tab-content').forEach(section => {
        section.classList.toggle('active', section.id === name);
    });
}
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => activateTab(tab.dataset.tab));
    tab.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            activateTab(tab.dataset.tab);
        }
    });
});
document.querySelectorAll('[data-open-tab]').forEach(button => {
    button.addEventListener('click', () => activateTab(button.dataset.openTab));
});
