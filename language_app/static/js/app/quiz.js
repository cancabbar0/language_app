document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('quiz-form');
    const quizContainer = document.getElementById('quiz-container');
    const totalQuestions = quizContainer.getAttribute('data-total-questions'); // Get the total number of questions

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Collect form data
        const formData = new FormData(form);
        const answerData = [];

        // Process form data into structured JSON
        for (let i = 1; i <= totalQuestions; i++) {
            const question = formData.get('question' + i);
            const answer = formData.get('answers' + i);
            if (question && answer) {
                answerData.push({
                    question: question,
                    answer: answer
                });
            }
        }


        // Send answer data to server
        fetch('/language_app/quiz/', {
            method: 'POST',
            body: JSON.stringify({answer_data: answerData}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
            }
        })
            .then(response => response.json())
            .then(data => {
                // Handle response data
                var message = '';
                for (var key in data) {
                    message += key + ': ' + data[key] + '\n';
                }
                alert(message);
                // You can update UI based on the response if needed
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Function to get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Get CSRF token
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
