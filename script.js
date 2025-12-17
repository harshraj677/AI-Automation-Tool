// ========================================
// DOM ELEMENTS
// ========================================
const textForm = document.getElementById('textForm');
const textInput = document.getElementById('textInput');
const actionSelect = document.getElementById('actionSelect');
const submitBtn = document.getElementById('submitBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const alertContainer = document.getElementById('alertContainer');
const alertMessage = document.getElementById('alertMessage');
const outputSection = document.getElementById('outputSection');
const outputContent = document.getElementById('outputContent');
const copyBtn = document.getElementById('copyBtn');
const charCount = document.getElementById('charCount');

// ========================================
// CHARACTER COUNTER
// ========================================
textInput.addEventListener('input', () => {
    const length = textInput.value.length;
    charCount.textContent = length;
    
    // Visual feedback for character count
    if (length > 1000) {
        charCount.style.color = 'var(--warning-color)';
    } else {
        charCount.style.color = 'var(--gray-400)';
    }
});

// ========================================
// FORM SUBMISSION HANDLER
// ========================================
textForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form values
    const text = textInput.value.trim();
    const action = actionSelect.value;
    
    // Validate input
    if (!text) {
        showAlert('Please enter some text to process.', 'error');
        return;
    }
    
    if (!action) {
        showAlert('Please select an action to perform.', 'error');
        return;
    }
    
    if (text.length < 10) {
        showAlert('Text is too short. Please enter at least 10 characters.', 'warning');
        return;
    }
    
    // Process the request
    await processText(text, action);
});

// ========================================
// MAIN PROCESSING FUNCTION
// ========================================
async function processText(text, action) {
    try {
        // Show loading state
        setLoadingState(true);
        hideAlert();
        hideOutput();
        
        // Prepare request payload
        const payload = {
            text: text,
            action: action
        };
        
        // Make API request
        const response = await fetch('api.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        // Parse response
        const data = await response.json();
        
        // Handle response
        if (response.ok && data.status === 'success') {
            displayOutput(data.data);
            showAlert('Text processed successfully!', 'success');
        } else {
            throw new Error(data.message || 'An error occurred while processing your request.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showAlert(error.message || 'Failed to process text. Please try again.', 'error');
    } finally {
        setLoadingState(false);
    }
}

// ========================================
// UI STATE MANAGEMENT
// ========================================
function setLoadingState(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Processing...';
        loadingSpinner.classList.remove('hidden');
        textForm.style.opacity = '0.6';
        textForm.style.pointerEvents = 'none';
    } else {
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = 'Process Text';
        loadingSpinner.classList.add('hidden');
        textForm.style.opacity = '1';
        textForm.style.pointerEvents = 'auto';
    }
}

function showAlert(message, type = 'error') {
    alertMessage.textContent = message;
    alertMessage.className = `alert ${type}`;
    alertContainer.classList.remove('hidden');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            hideAlert();
        }, 5000);
    }
}

function hideAlert() {
    alertContainer.classList.add('hidden');
}

function displayOutput(content) {
    outputContent.textContent = content;
    outputSection.classList.remove('hidden');
    
    // Smooth scroll to output
    setTimeout(() => {
        outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function hideOutput() {
    outputSection.classList.add('hidden');
}

// ========================================
// COPY TO CLIPBOARD FUNCTIONALITY
// ========================================
copyBtn.addEventListener('click', async () => {
    const text = outputContent.textContent;
    
    try {
        await navigator.clipboard.writeText(text);
        
        // Visual feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copied!
        `;
        copyBtn.style.background = 'var(--secondary-color)';
        copyBtn.style.color = 'white';
        copyBtn.style.borderColor = 'var(--secondary-color)';
        
        // Reset after 2 seconds
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
            copyBtn.style.color = '';
            copyBtn.style.borderColor = '';
        }, 2000);
        
    } catch (error) {
        showAlert('Failed to copy to clipboard.', 'error');
    }
});

// ========================================
// KEYBOARD SHORTCUTS
// ========================================
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!submitBtn.disabled) {
            textForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to clear form
    if (e.key === 'Escape') {
        textInput.value = '';
        actionSelect.value = '';
        charCount.textContent = '0';
        hideAlert();
        hideOutput();
    }
});

// ========================================
// INPUT VALIDATION FEEDBACK
// ========================================
textInput.addEventListener('blur', () => {
    const text = textInput.value.trim();
    if (text && text.length < 10) {
        textInput.style.borderColor = 'var(--warning-color)';
    } else {
        textInput.style.borderColor = '';
    }
});

textInput.addEventListener('focus', () => {
    textInput.style.borderColor = '';
});

// ========================================
// PREVENT FORM SUBMISSION ON ENTER
// ========================================
textInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
        // Allow regular Enter in textarea (for new lines)
        // Only Ctrl/Cmd+Enter will submit
    }
});

// ========================================
// AUTO-RESIZE TEXTAREA (OPTIONAL ENHANCEMENT)
// ========================================
textInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 400) + 'px';
});

// ========================================
// INITIALIZATION
// ========================================
console.log('Smart Text Assistant loaded successfully!');
console.log('Tip: Use Ctrl/Cmd + Enter to submit, Escape to clear');
