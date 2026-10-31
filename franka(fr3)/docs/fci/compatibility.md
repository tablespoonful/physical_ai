> 変換元: `compatibility.rst.txt`

# Software Versions Compatibility

This section provides an overview of the compatibility between different versions of the robot system version, libfranka and the robot/gripper server version which are coupled to the robot system version. E.g. a **robot system version** 5.7.2 needs a **robot** version 9 and **gripper** version 3.

Note: Often, people talk about *image version* while talking about the *robot system version*.

<style>
    .compatibility-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .robot-select {
        padding: 8px 12px;
        font-size: 16px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
        border-radius: 4px;
        width: 200px;
    }
    .compatibility-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    .compatibility-table th,
    .compatibility-table td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    .compatibility-table th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    .compatibility-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    .matrix {
        display: none;
    }
    .matrix.active {
        display: block;
    }
    .robot-description {
        margin-bottom: 15px;
        font-style: italic;
        color: #666;
    }
</style>
&#10;<div class="compatibility-container">
    <select class="robot-select" id="robotSelector" onchange="showCompatibility()">
    </select>
    <div class="robot-description" id="robotDescription"></div>
    <div id="matrixContainer"></div>
</div>
&#10;<script src="_static/compatibility_data.js"></script>
<script>
    // Populate the dropdown
    const selector = document.getElementById('robotSelector');
&#10;    // Sort robot names to ensure Franka Research 3 is first
    const robotNames = Object.keys(compatibilityData).sort((a, b) => {
        if (a === 'Franka Research 3') return -1;
        if (b === 'Franka Research 3') return 1;
        return a.localeCompare(b);
    });
&#10;    robotNames.forEach(robot => {
        const option = document.createElement('option');
        option.value = robot;
        option.textContent = robot;
        selector.appendChild(option);
    });
&#10;    // Set default selection to Franka Research 3
    selector.value = 'Franka Research 3';
    showCompatibility();  // Show the default selection immediately
&#10;    function createTable(robotData) {
        const table = document.createElement('table');
        table.className = 'compatibility-table';
&#10;        // Create header row
        const headerRow = document.createElement('tr');
        robotData.headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);
&#10;        // Create data rows
        robotData.data.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });
&#10;        return table;
    }
&#10;    function showCompatibility() {
        const selected = selector.value;
        const container = document.getElementById('matrixContainer');
        const descriptionElement = document.getElementById('robotDescription');
&#10;        // Clear previous content
        container.innerHTML = '';
        descriptionElement.textContent = '';
&#10;        if (selected && compatibilityData[selected]) {
            // Show robot description
            if (robotDescriptions[selected]) {
                descriptionElement.innerHTML = robotDescriptions[selected];
            }
&#10;            // Create and show compatibility table
            const mainHeading = document.createElement('h4');
            mainHeading.textContent = selected;
            container.appendChild(mainHeading);
            const table = createTable(compatibilityData[selected]);
            container.appendChild(table);
&#10;            // Show additional tables if configured
            if (additionalTables[selected]) {
                additionalTables[selected].forEach(entry => {
                    const heading = document.createElement('h4');
                    heading.textContent = entry.title;
                    heading.style.marginTop = '30px';
                    container.appendChild(heading);
                    if (entry.description) {
                        const desc = document.createElement('p');
                        desc.innerHTML = entry.description;
                        desc.style.fontStyle = 'italic';
                        desc.style.color = '#666';
                        container.appendChild(desc);
                    }
                    const extraTable = createTable(entry);
                    container.appendChild(extraTable);
                });
            }
        }
    }
&#10;    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        showCompatibility();
    });
</script>

## Further Compatibility Information

For <span class="title-ref">franka_ros</span> compatibility information, please refer to ros-compatibility and for <span class="title-ref">franka_matlab</span> compatibility information, please refer to compatibility-franka-matlab.

[Robot version](https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/robot/service_types.h) and [Gripper version](https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/gripper/types.h) are part of libfranka-common repository, a submodule of libfranka repository.

> [!CAUTION]
> Franka Robotics currently does not provide any support for Windows
