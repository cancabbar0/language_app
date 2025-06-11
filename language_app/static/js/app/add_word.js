// add_word.js

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('#add-word-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(form);

        fetch('/language_app/add_word/', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            alert(data.result.english);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            // Hata durumunda kullanıcıya bir hata mesajı gösterebilirsiniz
            alert('An error occurred while adding the word.');
        });
    });
});
