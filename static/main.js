const NotesApp = (function () {
    const $ = (s) => document.querySelector(s);
    const $$ = (s) => [].slice.call(document.querySelectorAll(s));

    function saveHotkey() {
        const saveBtn = $('[data-save]');
        if (saveBtn === null) {
            return;
        }

        // bind CTRL + S
        window.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                saveBtn.click();
            }
        });
    }

    return {
        init() {
            saveHotkey();
            console.info('NotesApp loaded successfully');
        }
    }
})();

document.addEventListener('DOMContentLoaded', NotesApp.init);