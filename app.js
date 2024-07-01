    document.addEventListener('DOMContentLoaded', function() {
        const dateElement = document.getElementById('date');
        const today = new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        dateElement.textContent = `Today's Date: ${today}`;
    });

    function showPersonalDataPage() {
        document.getElementById('welcome-section').style.display = 'none';
        document.getElementById('personal-data-page').style.display = 'block';
    }

    function submitPersonalData() {
        const form = document.getElementById('personal-data-form');
        const data = {
            firstName: form.firstName.value,
            lastName: form.lastName.value,
            age: form.age.value,
            gender: form.gender.value,
            medicalHistory: form.medicalHistory.value,
            currentMedications: form.currentMedications.value,
            allergies: form.allergies.value,
            emergencyContact: form.emergencyContact.value,
            address: form.address.value
        };

        fetch('http://localhost:5000/personal-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Failed to submit personal data');
            }
        })
        .then(data => {
            alert(data);
            showQuestionnairePage();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting personal data');
        });
    }

    function showQuestionnairePage() {
        document.getElementById('personal-data-page').style.display = 'none';
        document.getElementById('questionnaire-page').style.display = 'block';
    }

    function submitQuestionnaire() {
        const form = document.getElementById('questionnaire-form');
        const data = {
            question1: form.question1.value,
            question2: form.question2.value,
            question3: form.question3.value,
            question4: form.question4.value,
            question5: form.question5.value,
            question6: form.question6.value,
            question7: form.question7.value,
            question8: form.question8.value,
            question9: form.question9.value
        };

        fetch('http://localhost:5000/questionnaire', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Failed to submit questionnaire');
            }
        })
        .then(data => {
            alert(data);
            showResultPage();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting questionnaire');
        });
    }

    function showResultPage() {
        fetch(`http://localhost:5000/risk-assessment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to get risk assessment');
            }
        })
        .then(data => {
            document.getElementById('result-message').textContent = data.message;
            document.getElementById('questionnaire-page').style.display = 'none';
            document.getElementById('result-page').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while getting risk assessment');
        });
    }
    