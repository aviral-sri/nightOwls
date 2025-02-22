document.addEventListener('DOMContentLoaded', () => {
    const dangerToggle = document.getElementById('dangerModeToggle');
    const soundToggle = document.getElementById('soundToggle');
    const actionBtn = document.getElementById('actionBtn');
    const statusDiv = document.getElementById('status');
    const neonHeading = document.getElementById('neonHeading'); 
    let isSystemRunning = false;


    function updateUI() {
        if (!isSystemRunning) {
            statusDiv.textContent = "System Inactive";        
            neonHeading.classList.remove('neon-on');
            neonHeading.classList.add('neon-off');
        } else {
            const mode = dangerToggle.checked ? "Danger Mode" : "Normal Mode";
            const sound = soundToggle.checked ? "OFF" : "ON";
            statusDiv.textContent = `${mode} | Sound: ${sound}`;
            neonHeading.classList.remove('neon-off');
            neonHeading.classList.add('neon-on');
        }
        actionBtn.textContent = isSystemRunning ? "Stop System" : "Start System";
    }

    actionBtn.addEventListener('click', () => {
        isSystemRunning = !isSystemRunning;
        if (isSystemRunning) {
            statusDiv.textContent = "initializing system";
            setTimeout(() => {
              fetch('/start_system', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                      dangerMode: dangerToggle.checked,
             
                      soundOn: !soundToggle.checked  
                  })
              });
            },);
            
            setTimeout(() => {
                if (isSystemRunning) {
                    updateUI();
                }
            }, 2000);
        } else {
            fetch('/stop_system', { method: 'POST' });
            updateUI();
        }
    });

    dangerToggle.addEventListener('change', updateUI);
    soundToggle.addEventListener('change', updateUI);

    updateUI();
});
