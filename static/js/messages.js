document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');

    messages.forEach(function(msg) {
        const autoDismissTime = parseInt(msg.dataset.autoDismiss, 10);

        const dismiss = function() {
            msg.classList.add('message-dismissing');
            setTimeout(function() {
                msg.remove();
            }, 300);
        };

        msg.addEventListener('click', dismiss);

        if (autoDismissTime > 0) {
            setTimeout(dismiss, autoDismissTime);
        }
    });
});