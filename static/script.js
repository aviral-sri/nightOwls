document.addEventListener('DOMContentLoaded', () => {
    const dangerToggle = document.getElementById('dangerModeToggle');
    const soundToggle = document.getElementById('soundToggle');
    const actionBtn = document.getElementById('actionBtn');
    const statusDiv = document.getElementById('status');

    let isSystemRunning = false;

    function updateUI() {
        const mode = dangerToggle.checked ? "Danger Mode" : "Normal Mode";
        const sound = soundToggle.checked ? "ON" : "OFF";
        statusDiv.textContent = `${mode} | Sound: ${sound}`;
        actionBtn.textContent = isSystemRunning ? "Stop System" : "Start System";
    }

    actionBtn.addEventListener('click', () => {
        isSystemRunning = !isSystemRunning;
        if (isSystemRunning) {
            fetch('/start_system', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    dangerMode: dangerToggle.checked,
                    soundOn: soundToggle.checked
                })
            });
        } else {
            fetch('/stop_system', { method: 'POST' });
        }
        updateUI();
    });

    dangerToggle.addEventListener('change', updateUI);
    soundToggle.addEventListener('change', updateUI);
    updateUI();
});
