document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const input = document.querySelector('input[name="question"]') as HTMLInputElement;
        const question = input.value;

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
        document.querySelector('#answer')!.innerHTML = data.answer;
    });
});
