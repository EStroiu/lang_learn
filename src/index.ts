document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const input = document.querySelector('input[name="question"]') as HTMLInputElement;
        const submitButton = document.querySelector('button[type="submit"]') as HTMLButtonElement;
        const answerDiv = document.querySelector('#answer') as HTMLDivElement;
        const question = input.value;

        // Disable the input and submit button
        input.disabled = true;
        submitButton.disabled = true;

        // Show loading message
        answerDiv.innerHTML = '<div class="progress"><div class="indeterminate"></div></div>';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    question: question,
                }),
            });

            const data = await response.json();
            answerDiv.innerHTML = data.answer;
        } catch (error) {
            console.error('Error:', error);
            answerDiv.innerHTML = 'An error occurred. Please try again.';
        } finally {
            // Re-enable the input and submit button
            input.disabled = false;
            submitButton.disabled = false;

            // Clear the input field
            input.value = '';
        }
    });
});

