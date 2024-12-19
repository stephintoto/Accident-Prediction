function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed'); // Toggles the 'collapsed' class
    

}

function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.add('collapsed'); // Start with the sidebar collapsed
}

function updateTime() {
    const currentTimeElement = document.getElementById('current-time');
    const now = new Date();
    const formattedTime = now.toLocaleString('en-US', { weekday: 'long', hour: '2-digit', minute: '2-digit', second: '2-digit' }); // This formats the date and time
    currentTimeElement.textContent = formattedTime;
}

function updatePsNames() {
    const selectedDistrict = document.getElementById('district').value;
    const psNameDropdown = document.getElementById('ps_name');

    // Fetch police stations for the selected district
    fetch(`/get_ps_names?district=${selectedDistrict}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            psNameDropdown.innerHTML = '<option value="All">All</option>';

            // Populate dropdown with new data
            data.forEach(ps_name => {
                const option = document.createElement('option');
                option.value = ps_name;
                option.textContent = ps_name;
                psNameDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Call updateTime every second
setInterval(updateTime, 1000); // 1000 ms = 1 second