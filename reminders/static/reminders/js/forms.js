// Reminder Form Enhancement JavaScript

// Date and Time Picker Enhancement
document.addEventListener('DOMContentLoaded', function() {
    initializeFormEnhancements();
    initializeDateTimeEnhancements();
});

// Initialize form enhancements
function initializeFormEnhancements() {
    // Auto-focus the title field for better UX
    const titleField = document.querySelector('input[name="title"]');
    if (titleField) {
        titleField.focus();
    }
}

// Date shortcuts functionality
function setDate(period) {
    const dateInput = document.querySelector('input[name="date"]');
    if (!dateInput) return;
    
    const today = new Date();
    let targetDate;
    
    switch(period) {
        case 'today':
            targetDate = today;
            break;
        case 'tomorrow':
            targetDate = new Date(today);
            targetDate.setDate(today.getDate() + 1);
            break;
        case 'next_week':
            targetDate = new Date(today);
            targetDate.setDate(today.getDate() + 7);
            break;
        case 'next_month':
            targetDate = new Date(today);
            targetDate.setMonth(today.getMonth() + 1);
            break;
    }
    
    if (targetDate) {
        // Format date as YYYY-MM-DD for date input
        const formattedDate = targetDate.toISOString().split('T')[0];
        dateInput.value = formattedDate;
        
        // Add visual feedback
        addVisualFeedback(dateInput);
    }
}

// Time shortcuts functionality
function setTime(timeString) {
    const timeInput = document.querySelector('input[name="time"]');
    if (!timeInput) return;
    
    timeInput.value = timeString;
    
    // Add visual feedback
    addVisualFeedback(timeInput);
}

// Visual feedback helper
function addVisualFeedback(element) {
    const originalBackground = element.style.background;
    element.style.background = 'var(--theme-shadow)';
    setTimeout(() => {
        element.style.background = originalBackground;
    }, 300);
}

// Enhanced date input interaction
function initializeDateTimeEnhancements() {
    const dateInput = document.querySelector('input[name="date"]');
    const timeInput = document.querySelector('input[name="time"]');
    
    // Add change listeners for better UX
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            // If no time is set when date is selected, suggest a default time
            if (timeInput && !timeInput.value) {
                const currentHour = new Date().getHours();
                let suggestedTime;
                
                if (currentHour < 9) {
                    suggestedTime = '09:00';
                } else if (currentHour < 12) {
                    suggestedTime = '12:00';
                } else if (currentHour < 17) {
                    suggestedTime = '17:00';
                } else {
                    suggestedTime = '19:00';
                }
                
                timeInput.value = suggestedTime;
                addVisualFeedback(timeInput);
            }
        });
    }
}

// Form validation enhancement
function validateForm() {
    const titleInput = document.querySelector('input[name="title"]');
    const dateInput = document.querySelector('input[name="date"]');
    
    let isValid = true;
    let errorMessage = '';
    
    // Check required fields
    if (!titleInput || !titleInput.value.trim()) {
        errorMessage += 'Title is required.\n';
        isValid = false;
    }
    
    if (!dateInput || !dateInput.value) {
        errorMessage += 'Date is required.\n';
        isValid = false;
    }
    
    // Check if date is in the past
    if (dateInput && dateInput.value) {
        const selectedDate = new Date(dateInput.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            errorMessage += 'Date cannot be in the past.\n';
            isValid = false;
        }
    }
    
    if (!isValid) {
        alert(errorMessage);
    }
    
    return isValid;
}

// Add form validation to submit
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.modern-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
            }
        });
    }
});
