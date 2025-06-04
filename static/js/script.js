// DOM Elements
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const genderInput = document.getElementById('gender');
const bloodGroupInput = document.getElementById('bloodGroup');
const descriptionInput = document.getElementById('description');
const submitBtn = document.getElementById('submitBtn');
const profileName = document.getElementById('profileName');
const profileEmail = document.getElementById('profileEmail');
const profilePhone = document.getElementById('profilePhone');
const profileGender = document.getElementById('profileGender');
const profileBloodGroup = document.getElementById('profileBloodGroup');
const summaryResults = document.getElementById('summaryResults');
const photoUpload = document.getElementById('photoUpload');
const userPhoto = document.getElementById('userPhoto');
const uploadPhotoBtn = document.getElementById('uploadPhotoBtn');

// File Upload Elements
const bloodReportInput = document.getElementById('bloodReport');
const medicalReportInput = document.getElementById('medicalReport');
const bloodReportFiles = document.getElementById('bloodReportFiles');
const medicalReportFiles = document.getElementById('medicalReportFiles');
const bloodReportUpload = document.getElementById('bloodReportUpload');
const medicalReportUpload = document.getElementById('medicalReportUpload');

// Tag Data
const conditionsData = [
    'Hypertension', 'Diabetes', 'Asthma', 'Migraine', 'Arthritis',
    'Anxiety', 'Depression', 'Allergies', 'Insomnia', 'GERD'
];

const symptomsData = [
    'Headache', 'Cough', 'Fever', 'Fatigue', 'Nausea',
    'Dizziness', 'Shortness of breath', 'Chest pain', 'Abdominal pain', 'Joint pain',
    'Muscle weakness', 'Rash', 'Sore throat', 'Runny nose', 'Sneezing',
    'Swelling', 'Weight loss', 'Weight gain', 'Blurred vision', 'Palpitations'
];

const bodyPartsData = [
    'Head', 'Neck', 'Chest', 'Abdomen', 'Back',
    'Arms', 'Legs', 'Hands', 'Feet', 'Pelvis',
    'Skin', 'Eyes', 'Ears', 'Nose', 'Throat'
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tag selectors
    initializeTagSelector('conditionsContainer', conditionsData);
    initializeTagSelector('symptomsContainer', symptomsData);
    initializeTagSelector('bodyPartsContainer', bodyPartsData);
    
    // Set up file upload handlers
    setupFileUpload(bloodReportInput, bloodReportFiles, bloodReportUpload);
    setupFileUpload(medicalReportInput, medicalReportFiles, medicalReportUpload);
    
    // Set up profile photo upload
    uploadPhotoBtn.addEventListener('click', function() {
        photoUpload.click();
    });
    
    photoUpload.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(event) {
                userPhoto.src = event.target.result;
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });
    
    // Set up form input listeners to update profile card
    nameInput.addEventListener('input', updateProfileCard);
    emailInput.addEventListener('input', updateProfileCard);
    phoneInput.addEventListener('input', updateProfileCard);
    genderInput.addEventListener('change', updateProfileCard);
    bloodGroupInput.addEventListener('change', updateProfileCard);
        
    // Set up form submission
    submitBtn.addEventListener('click', submitForm);
    
    // Initial profile card update
    updateProfileCard();
});

// Initialize a tag selector
function initializeTagSelector(containerId, tagsData) {
    const container = document.getElementById(containerId);
    
    tagsData.forEach(tag => {
        const tagElement = document.createElement('div');
        tagElement.className = 'tag';
        tagElement.textContent = tag;
        tagElement.dataset.value = tag.toLowerCase().replace(/\s+/g, '_');
        
        tagElement.addEventListener('click', function() {
            this.classList.toggle('selected');
        });
        
        container.appendChild(tagElement);
    });
}

// Set up file upload with drag and drop
function setupFileUpload(inputElement, filesContainer, dropZone) {
    let files = [];
    
    // Handle file selection
    inputElement.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            files = Array.from(e.target.files);
            updateFileList(filesContainer, files);
        }
    });
    
    // Drag and drop events
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('highlight');
    });
    
    dropZone.addEventListener('dragleave', function() {
        this.classList.remove('highlight');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('highlight');
        
        if (e.dataTransfer.files.length > 0) {
            files = Array.from(e.dataTransfer.files);
            updateFileList(filesContainer, files);
            
            // Update the input files
            const dataTransfer = new DataTransfer();
            files.forEach(file => dataTransfer.items.add(file));
            inputElement.files = dataTransfer.files;
        }
    });
}

// Update the file list display
function updateFileList(container, files) {
    container.innerHTML = '';
    
    if (files.length === 0) {
        return;
    }
    
    files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileIcon = document.createElement('i');
        fileIcon.className = getFileIconClass(file.name);
        
        const fileName = document.createElement('span');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('span');
        fileSize.className = 'file-size';
        fileSize.textContent = formatFileSize(file.size);
        
        const fileRemove = document.createElement('span');
        fileRemove.className = 'file-remove';
        fileRemove.innerHTML = '&times;';
        fileRemove.addEventListener('click', function(e) {
            e.stopPropagation();
            files.splice(index, 1);
            updateFileList(container, files);
            
            // Update the input files
            const dataTransfer = new DataTransfer();
            files.forEach(file => dataTransfer.items.add(file));
            const inputId = container.id.replace('Files', '');
            document.getElementById(inputId).files = dataTransfer.files;
        });
        
        fileItem.appendChild(fileIcon);
        fileItem.appendChild(fileName);
        fileItem.appendChild(fileSize);
        fileItem.appendChild(fileRemove);
        
        container.appendChild(fileItem);
    });
}

// Get appropriate icon for file type
function getFileIconClass(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    
    switch(extension) {
        case 'pdf':
            return 'fas fa-file-pdf';
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
            return 'fas fa-file-image';
        case 'mp4':
        case 'mov':
        case 'avi':
            return 'fas fa-file-video';
        default:
            return 'fas fa-file';
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Update profile card with form data
function updateProfileCard() {
    profileName.textContent = nameInput.value || 'Your Name';
    profileEmail.textContent = emailInput.value || 'email@example.com';
    profilePhone.textContent = phoneInput.value || 'Not provided';
    
    const genderText = genderInput.options[genderInput.selectedIndex].text;
    profileGender.textContent = genderText || 'Not specified';
    
    const bloodGroupText = bloodGroupInput.options[bloodGroupInput.selectedIndex].text;
    profileBloodGroup.textContent = bloodGroupText || 'Not specified';

}

// Submit form data to backend
function submitForm() {
    // Validate required fields
    if (!nameInput.value.trim()) {
        alert('Please enter your name');
        nameInput.focus();
        return;
    }
    
    if (!descriptionInput.value.trim()) {
        alert('Please describe your health concerns');
        descriptionInput.focus();
        return;
    }
    
    // Prepare form data
    const formData = new FormData();
    
    // Add personal info
    formData.append('name', nameInput.value.trim());
    formData.append('email', emailInput.value.trim());
    formData.append('phone', phoneInput.value.trim());
    formData.append('gender', genderInput.value);
    formData.append('bloodGroup', bloodGroupInput.value);
    formData.append('description', descriptionInput.value.trim());
    
    // Add selected symptoms and body parts
    const selectedConditions = getSelectedTags('conditionsContainer');
    const selectedSymptoms = getSelectedTags('symptomsContainer');
    const selectedBodyParts = getSelectedTags('bodyPartsContainer');
    
    selectedConditions.forEach(condition => {
        formData.append('symptoms[]', condition);
    });
    
    selectedSymptoms.forEach(symptom => {
        formData.append('symptoms[]', symptom);
    });
    
    selectedBodyParts.forEach(bodyPart => {
        formData.append('body_parts[]', bodyPart);
    });
    
    // Add files
    if (bloodReportInput.files) {
        for (let i = 0; i < bloodReportInput.files.length; i++) {
            formData.append('files', bloodReportInput.files[i]);
        }
    }
    
    if (medicalReportInput.files) {
        for (let i = 0; i < medicalReportInput.files.length; i++) {
            formData.append('files', medicalReportInput.files[i]);
        }
    }
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.innerHTML = '<span>Processing...</span><i class="fas fa-spinner"></i>';
    
    // Send to backend with proper headers
    fetch('/api/analyze', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'  // Crucial for Flask to identify as AJAX
        }
    })
    .then(response => {
        // First check for HTTP errors
        if (!response.ok) {
            // Try to parse error JSON, fallback to text
            return response.json()
                .catch(() => { throw new Error(`Server error: ${response.status}`) })
                .then(errorData => { throw new Error(errorData.message || 'Unknown error') });
        }
        return response.json();
    })
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Request failed:', error);
        alert(`Error: ${error.message}\n\nPlease check your inputs and try again.`);
    })
    .finally(() => {
        submitBtn.classList.remove('loading');
        submitBtn.innerHTML = '<span>Generate Health Summary</span><i class="fas fa-arrow-right"></i>';
    });
}

// Get selected tags from a container
function getSelectedTags(containerId) {
    const container = document.getElementById(containerId);
    const selectedTags = [];
    
    container.querySelectorAll('.tag.selected').forEach(tag => {
        selectedTags.push(tag.dataset.value);
    });
    
    return selectedTags;
}

// Display results from backend
function displayResults(data) {
    summaryResults.innerHTML = '';
    
    // Clear any existing event listeners
    symptomsContainer.removeEventListener('click', handleSymptomClick);
    
    // Add new event listener for severity sliders
    symptomsContainer.addEventListener('click', handleSymptomClick);
    
    if (!data.possible_conditions || data.possible_conditions.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'summary-item fade-in';
        noResults.innerHTML = `
            <h3><i class="fas fa-info-circle"></i> No Specific Conditions Identified</h3>
            <p>Based on your input, we couldn't identify specific conditions. Here are some general health recommendations.</p>
        `;
        summaryResults.appendChild(noResults);
    } else {
        const conditionsHeader = document.createElement('div');
        conditionsHeader.className = 'summary-item fade-in';
        conditionsHeader.innerHTML = `
            <h3><i class="fas fa-diagnoses"></i> Possible Conditions</h3>
            <div class="condition-list"></div>
        `;
        
        const conditionList = conditionsHeader.querySelector('.condition-list');
        data.possible_conditions.forEach(condition => {
            const conditionTag = document.createElement('span');
            conditionTag.className = 'condition-tag';
            conditionTag.textContent = condition;
            conditionList.appendChild(conditionTag);
        });
        
        summaryResults.appendChild(conditionsHeader);
    }
    
    // Add first aid recommendations
    if (data.health_summary.first_aid && data.health_summary.first_aid.length > 0) {
        const firstAidItem = document.createElement('div');
        firstAidItem.className = 'summary-item fade-in';
        firstAidItem.innerHTML = `
            <h3><i class="fas fa-first-aid"></i> First Aid & Home Remedies</h3>
            <ul></ul>
        `;
        
        const firstAidList = firstAidItem.querySelector('ul');
        data.health_summary.first_aid.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${item}`;
            firstAidList.appendChild(li);
        });
        
        summaryResults.appendChild(firstAidItem);
    }
    
    // Add lifestyle recommendations
    if (data.health_summary.lifestyle_recommendations && data.health_summary.lifestyle_recommendations.length > 0) {
        const lifestyleItem = document.createElement('div');
        lifestyleItem.className = 'summary-item fade-in';
        lifestyleItem.innerHTML = `
            <h3><i class="fas fa-heartbeat"></i> Lifestyle Recommendations</h3>
            <ul></ul>
        `;
        
        const lifestyleList = lifestyleItem.querySelector('ul');
        data.health_summary.lifestyle_recommendations.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${item}`;
            lifestyleList.appendChild(li);
        });
        
        summaryResults.appendChild(lifestyleItem);
    }
    
    // Add dietary suggestions
    if (data.health_summary.dietary_suggestions && data.health_summary.dietary_suggestions.length > 0) {
        const dietItem = document.createElement('div');
        dietItem.className = 'summary-item fade-in';
        dietItem.innerHTML = `
            <h3><i class="fas fa-utensils"></i> Dietary Suggestions</h3>
            <ul></ul>
        `;
        
        const dietList = dietItem.querySelector('ul');
        data.health_summary.dietary_suggestions.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${item}`;
            dietList.appendChild(li);
        });
        
        summaryResults.appendChild(dietItem);
    }
    
    // Add recommended specialist
    if (data.health_summary.recommended_specialist) {
        const specialistItem = document.createElement('div');
        specialistItem.className = 'summary-item fade-in';
        specialistItem.innerHTML = `
            <h3><i class="fas fa-user-md"></i> Recommended Specialist</h3>
            <p>${data.health_summary.recommended_specialist}</p>
        `;
        summaryResults.appendChild(specialistItem);
    }
    
    // Add PDF download button
    if (data.pdf_url) {
        const downloadBtn = document.createElement('a');
        downloadBtn.className = 'download-btn';
        downloadBtn.href = data.pdf_url;
        downloadBtn.innerHTML = '<i class="fas fa-file-pdf"></i> Download PDF Report';
        summaryResults.appendChild(downloadBtn);
    }
    
    // Add telemedicine button
    if (data.session_id) {
        const teleBtn = document.createElement('a');
        teleBtn.className = 'tele-btn';
        teleBtn.href = `https://telemed.example.com/join/${data.session_id}`;
        teleBtn.target = '_blank';
        teleBtn.innerHTML = '<i class="fas fa-video"></i> Video Consult Doctor';
        summaryResults.appendChild(teleBtn);
    }
    
    // Add medication tracker
    const medTracker = document.createElement('div');
    medTracker.className = 'med-tracker fade-in';
    medTracker.innerHTML = `
        <h3><i class="fas fa-pills"></i> Medication Reminder</h3>
        <div class="med-tracker-controls">
            <input type="time" id="reminderTime">
            <button id="setReminderBtn">Set Daily Reminder</button>
        </div>
    `;
    summaryResults.appendChild(medTracker);
    
    // Add event listener to reminder button
    document.getElementById('setReminderBtn').addEventListener('click', setReminder);
    
    // Add health score visualization
    if (data.health_score) {
        const healthScoreEl = document.createElement('div');
        healthScoreEl.className = 'gauge fade-in';
        healthScoreEl.innerHTML = `
            <div class="gauge-fill" style="width: ${data.health_score}%"></div>
            <span>${data.health_score}/100 Health Score</span>
        `;
        summaryResults.appendChild(healthScoreEl);
    }
    
    // Scroll to results
    summaryResults.scrollIntoView({ behavior: 'smooth' });
}

// Severity slider handler
function handleSymptomClick(e) {
    if (e.target.classList.contains('tag')) {
        // Remove existing slider if any
        const existingSlider = e.target.nextElementSibling;
        if (existingSlider && existingSlider.classList.contains('severity-slider')) {
            existingSlider.remove();
        }
        
        // Create new slider
        const severitySlider = document.createElement('div');
        severitySlider.className = 'severity-slider';
        severitySlider.innerHTML = `
            <label>Symptom Severity:</label>
            <input type="range" min="1" max="5" value="3">
            <span class="severity-value">3/5</span>
        `;
        
        // Insert after clicked tag
        e.target.parentNode.insertBefore(severitySlider, e.target.nextSibling);
        
        // Add event listener to update value display
        const rangeInput = severitySlider.querySelector('input[type="range"]');
        const valueDisplay = severitySlider.querySelector('.severity-value');
        rangeInput.addEventListener('input', () => {
            valueDisplay.textContent = `${rangeInput.value}/5`;
        });
    }
}

// Medication reminder function
function setReminder() {
    const timeInput = document.getElementById('reminderTime');
    if (!timeInput.value) {
        alert('Please select a time for your reminder');
        return;
    }
    
    alert(`Medication reminder set for ${timeInput.value} daily`);
    // In a real app: Integrate with browser notifications
}