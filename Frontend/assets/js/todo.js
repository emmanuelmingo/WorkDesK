document.addEventListener('DOMContentLoaded', function() {
    const addTaskTrigger = document.getElementById('add-task-trigger');
    const addTaskForm = document.getElementById('add-task-form');

    addTaskTrigger.onclick = function() {
        addTaskForm.style.display = 'block';
        addTaskTrigger.style.display = 'none';
    };

    window.closeAddTaskForm = function() {
        addTaskForm.style.display = 'none';
        addTaskTrigger.style.display = 'block';
    }
});
