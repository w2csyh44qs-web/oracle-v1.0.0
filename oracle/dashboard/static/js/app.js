/**
 * Oracle Dashboard - Main Application Logic
 *
 * Handles:
 * - WebSocket connection to server
 * - Real-time status updates
 * - Command execution
 * - Terminal output rendering
 * - UI state management
 */

// Global state
let socket = null;
let commandHistory = [];
let historyIndex = -1;

// View mode state
let currentView = 'full';
let logsExpanded = false;
let tasksExpanded = false;

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    initializeTerminal();
    initializeCommandHints();
    startStatusPolling();
    loadLogs();
    loadTasks();
});

/**
 * Initialize WebSocket connection
 */
function initializeWebSocket() {
    // Connect to Flask-SocketIO server
    socket = io();

    // Connection events
    socket.on('connect', () => {
        console.log('Connected to Oracle Dashboard');
        updateConnectionStatus(true);
        addTerminalLine('✓ Connected to Oracle Dashboard', 'success');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from Oracle Dashboard');
        updateConnectionStatus(false);
        addTerminalLine('✗ Disconnected from server', 'error');
    });

    // Status updates
    socket.on('status_update', (data) => {
        console.log('Status update:', data);
        updateDashboard(data);
    });

    // Command results
    socket.on('command_result', (result) => {
        console.log('Command result:', result);
        displayCommandResult(result);
    });

    // Error handling
    socket.on('error', (error) => {
        console.error('Socket error:', error);
        addTerminalLine(`✗ Error: ${error}`, 'error');
    });
}

/**
 * Initialize terminal input handling
 */
function initializeTerminal() {
    const input = document.getElementById('command-input');

    // Enter key: Execute command
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                executeCommand(command);
                commandHistory.push(command);
                historyIndex = commandHistory.length;
                input.value = '';
            }
        }
        // Up arrow: Previous command
        else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                input.value = commandHistory[historyIndex];
            }
        }
        // Down arrow: Next command
        else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                input.value = commandHistory[historyIndex];
            } else {
                historyIndex = commandHistory.length;
                input.value = '';
            }
        }
    });

    // Auto-focus input
    input.focus();
    document.addEventListener('click', () => input.focus());
}

/**
 * Initialize command hint buttons
 */
function initializeCommandHints() {
    const hints = document.querySelectorAll('.hint');
    hints.forEach(hint => {
        hint.addEventListener('click', () => {
            const command = hint.textContent;
            document.getElementById('command-input').value = command;
            document.getElementById('command-input').focus();
        });
    });
}

/**
 * Fill command input (called by onclick handlers)
 */
function fillCommand(command) {
    const input = document.getElementById('command-input');
    input.value = command;
    input.focus();
}

/**
 * Execute Oracle command
 */
function executeCommand(command) {
    // Display command in terminal
    addTerminalLine(`oracle> ${command}`, 'command');

    // Handle built-in commands
    if (command === 'help') {
        displayHelp();
        return;
    }

    if (command === 'clear') {
        clearTerminal();
        return;
    }

    // Send to server via WebSocket
    if (socket && socket.connected) {
        socket.emit('command', { command });
        addTerminalLine('Executing...', 'info');
    } else {
        // Fallback to REST API
        fetch('/api/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command })
        })
        .then(response => response.json())
        .then(result => displayCommandResult(result))
        .catch(error => {
            addTerminalLine(`✗ Error: ${error}`, 'error');
        });
    }
}

/**
 * Display command result in terminal
 */
function displayCommandResult(result) {
    if (result.success) {
        // Display output
        if (result.output) {
            const lines = result.output.split('\n');
            lines.forEach(line => {
                if (line.trim()) {
                    addTerminalLine(line, 'success');
                }
            });
        }
        addTerminalLine('✓ Command completed', 'success');
    } else {
        // Display error
        addTerminalLine(`✗ Command failed: ${result.error}`, 'error');
        if (result.output) {
            addTerminalLine(result.output, 'warning');
        }
    }

    addTerminalLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', '');
}

/**
 * Display help information
 */
function displayHelp() {
    const helpText = [
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
        'ORACLE DASHBOARD COMMANDS',
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
        '',
        'Oracle Commands:',
        '  audit          - Run health audit',
        '  audit --quick  - Quick health check',
        '  status         - Show Oracle status',
        '  verify         - Run integrity check',
        '  clean          - Clean reports',
        '  optimize       - Run optimizations',
        '  sync           - Sync contexts',
        '',
        'Dashboard Commands:',
        '  help           - Show this help',
        '  clear          - Clear terminal',
        '',
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    ];

    helpText.forEach(line => addTerminalLine(line, ''));
}

/**
 * Add line to terminal output
 */
function addTerminalLine(text, type = '') {
    const output = document.getElementById('terminal-output');
    const line = document.createElement('div');
    line.className = `terminal-line ${type}`;
    line.textContent = text;
    output.appendChild(line);

    // Auto-scroll to bottom
    output.scrollTop = output.scrollHeight;
}

/**
 * Clear terminal output
 */
function clearTerminal() {
    const output = document.getElementById('terminal-output');
    output.innerHTML = '';
    addTerminalLine('Oracle Terminal v1.0', '');
    addTerminalLine('Type \'help\' for available commands', '');
    addTerminalLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', '');
}

/**
 * Update connection status indicator
 */
function updateConnectionStatus(connected) {
    const dot = document.getElementById('status-dot');
    const text = document.getElementById('status-text');

    if (connected) {
        dot.classList.add('connected');
        dot.classList.remove('disconnected');
        text.textContent = 'Connected';
        text.style.color = '#00ff00';
    } else {
        dot.classList.remove('connected');
        dot.classList.add('disconnected');
        text.textContent = 'Disconnected';
        text.style.color = '#ff4444';
    }
}

/**
 * Update dashboard with new status data
 */
function updateDashboard(data) {
    // Update health score
    if (data.health) {
        const score = Math.round(data.health.score);
        document.getElementById('health-score').textContent = score;
        document.getElementById('health-bar').style.width = `${score}%`;

        // Color health bar based on score
        const bar = document.getElementById('health-bar');
        if (score >= 80) {
            bar.style.background = '#00ff00';  // Green for healthy
        } else if (score >= 60) {
            bar.style.background = '#ffaa00';  // Orange for warning
        } else {
            bar.style.background = '#ff4444';  // Red for critical
        }
    }

    // Update daemon status
    if (data.daemon) {
        document.getElementById('daemon-running').textContent =
            data.daemon.running ? '✓ YES' : '✗ NO';
        document.getElementById('daemon-running').style.color =
            data.daemon.running ? '#00ff00' : '#ff4444';

        document.getElementById('daemon-pid').textContent =
            data.daemon.pid || 'N/A';

        if (data.daemon.uptime) {
            const uptime = formatUptime(data.daemon.uptime);
            document.getElementById('daemon-uptime').textContent = uptime;
        }

        document.getElementById('active-context').textContent =
            data.daemon.active_context || 'N/A';
    }

    // Update issues and optimizations
    if (data.health) {
        const issues = data.health.issues || {critical: 0, warnings: 0};
        document.getElementById('issues-critical').textContent = issues.critical || 0;
        document.getElementById('issues-warnings').textContent = issues.warnings || 0;
        document.getElementById('optimizations-pending').textContent =
            data.health.optimizations_pending || 0;

        // Update cost
        const cost = data.health.cost_today || 0;
        document.getElementById('cost-today').textContent = '$' + cost.toFixed(2);
    }

    // Update autosave status
    if (data.autosave) {
        const minutes = data.autosave.last_minutes || 0;
        document.getElementById('autosave-status').textContent = minutes;
    } else {
        document.getElementById('autosave-status').textContent = '--';
    }

    // Update activity log
    if (data.activity && data.activity.length > 0) {
        updateActivityLog(data.activity);
    }

    // Update last update time
    const now = new Date();
    document.getElementById('last-update').textContent =
        `Last update: ${now.toLocaleTimeString()}`;
}

/**
 * Update activity log (inline format)
 */
function updateActivityLog(activities) {
    const log = document.getElementById('activity-log');
    log.innerHTML = '';

    if (activities.length === 0) {
        const item = document.createElement('span');
        item.className = 'activity-item';
        item.textContent = 'Waiting for activity...';
        log.appendChild(item);
        return;
    }

    activities.forEach((activity, index) => {
        const item = document.createElement('span');
        item.className = 'activity-item';

        // Format message (shortened for inline display)
        const message = activity.message.substring(0, 60);
        const suffix = activity.message.length > 60 ? '...' : '';
        item.textContent = `${message}${suffix}`;

        log.appendChild(item);

        // Add separator between items (not after last)
        if (index < activities.length - 1) {
            const separator = document.createElement('span');
            separator.textContent = ' • ';
            separator.style.color = '#666666';
            log.appendChild(separator);
        }
    });
}

/**
 * Format uptime seconds to human-readable string
 */
function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

/**
 * Start polling server for status (fallback if WebSocket fails)
 */
function startStatusPolling() {
    setInterval(() => {
        // Only poll if WebSocket is not connected
        if (!socket || !socket.connected) {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => {
                    console.error('Status polling error:', error);
                });
        }
    }, 5000); // Poll every 5 seconds
}

/**
 * Set dashboard view mode
 */
function setView(view) {
    currentView = view;

    // Update button states
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.view === view) {
            btn.classList.add('active');
        }
    });

    // Update container class
    const container = document.querySelector('.container');
    container.classList.remove('view-full', 'view-compact');
    container.classList.add(`view-${view}`);

    // Show/hide logs and tasks in full mode
    if (view === 'full') {
        document.getElementById('logs-section').style.display = 'block';
        document.getElementById('tasks-section').style.display = 'block';
    } else {
        document.getElementById('logs-section').style.display = 'none';
        document.getElementById('tasks-section').style.display = 'none';
    }
}

/**
 * Toggle logs section
 */
function toggleLogs() {
    logsExpanded = !logsExpanded;
    const content = document.getElementById('logs-content');
    const toggle = document.getElementById('logs-toggle');

    if (logsExpanded) {
        content.style.display = 'block';
        toggle.classList.remove('collapsed');
        loadLogs();  // Refresh logs when expanding
    } else {
        content.style.display = 'none';
        toggle.classList.add('collapsed');
    }
}

/**
 * Toggle tasks section
 */
function toggleTasks() {
    tasksExpanded = !tasksExpanded;
    const content = document.getElementById('tasks-content');
    const toggle = document.getElementById('tasks-toggle');

    if (tasksExpanded) {
        content.style.display = 'block';
        toggle.classList.remove('collapsed');
        loadTasks();  // Refresh tasks when expanding
    } else {
        content.style.display = 'none';
        toggle.classList.add('collapsed');
    }
}

/**
 * Load daemon logs
 */
function loadLogs() {
    fetch('/api/logs')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('log-entries');

            if (!data.logs || data.logs.length === 0) {
                container.innerHTML = '<span class="log-line">No logs available</span>';
                return;
            }

            // Display last 20 log lines
            const logs = data.logs.slice(-20);
            container.innerHTML = '';

            logs.forEach(log => {
                const line = document.createElement('span');
                line.className = 'log-line';

                // Color code by level
                if (log.toLowerCase().includes('error')) {
                    line.classList.add('error');
                } else if (log.toLowerCase().includes('warning')) {
                    line.classList.add('warning');
                } else if (log.toLowerCase().includes('info')) {
                    line.classList.add('info');
                }

                line.textContent = log.trim();
                container.appendChild(line);
            });

            // Auto-scroll to bottom
            container.scrollTop = container.scrollHeight;
        })
        .catch(error => {
            console.error('Failed to load logs:', error);
        });
}

/**
 * Load task list
 */
function loadTasks() {
    // For now, show placeholder tasks
    // In the future, this could read from .oracle_tasks.json
    const container = document.getElementById('task-list');

    const tasks = [
        { text: 'Next health audit scheduled', completed: false, priority: false },
        { text: 'Context sync pending', completed: false, priority: false },
    ];

    container.innerHTML = '';

    if (tasks.length === 0) {
        container.innerHTML = '<span class="task-item">No pending tasks</span>';
        return;
    }

    tasks.forEach(task => {
        const item = document.createElement('span');
        item.className = 'task-item';

        if (task.completed) {
            item.classList.add('completed');
        }
        if (task.priority) {
            item.classList.add('priority');
        }

        item.textContent = task.text;
        container.appendChild(item);
    });
}

/**
 * Export functions for external use
 */
window.executeCommand = executeCommand;
window.clearTerminal = clearTerminal;
window.addTerminalLine = addTerminalLine;
window.fillCommand = fillCommand;
window.setView = setView;
window.toggleLogs = toggleLogs;
window.toggleTasks = toggleTasks;
