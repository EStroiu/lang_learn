import Quill from 'quill';
import 'quill/dist/quill.snow.css';

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.querySelector('#chat-form') as HTMLFormElement;
    const noteForm = document.querySelector('#note-form') as HTMLFormElement;

    // Initialize Quill editor
    const quill = new Quill('#editor-container', {
        theme: 'snow',
        placeholder: 'Write your note here...',
        modules: {
            toolbar: [
                [{ header: [1, 2, false] }],
                ['bold', 'italic', 'underline'],
                ['link', 'blockquote', 'code-block'],
                [{ list: 'ordered' }, { list: 'bullet' }]
            ]
        }
    });

    function loadNotes() {
        fetch('/notes')
            .then(response => response.json())
            .then(data => {
                const notesDiv = document.querySelector('#notes') as HTMLDivElement;
                notesDiv.innerHTML = ''; 
                data.notes.forEach((note: [number, string, string]) => {
                    const noteElement = document.createElement('div');
                    noteElement.classList.add('collection-item', 'position-relative');

                    const date = document.createElement('small');
                    date.textContent = note[2]; 
                    date.classList.add('note-date');
                    noteElement.appendChild(date);

                    const deleteButton = document.createElement('button');
                    deleteButton.innerHTML = '<i class="material-icons">delete</i>'; 
                    deleteButton.classList.add('btn', 'waves-effect', 'waves-light', 'red', 'delete-btn', 'right'); 
                    deleteButton.onclick = () => confirmDelete(note[0]); 
                    noteElement.appendChild(deleteButton);

                    const content = document.createElement('div');
                    content.innerHTML = note[1]; // Insert the HTML content from Quill
                    content.classList.add();
                    noteElement.appendChild(content);

                    notesDiv.insertBefore(noteElement, notesDiv.firstChild); // Add new notes to the top
                });
            });
    }

    loadNotes();

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const input = document.querySelector('#question') as HTMLInputElement;
        const submitButton = chatForm.querySelector('button[type="submit"]') as HTMLButtonElement;
        const answerDiv = document.querySelector('#answer') as HTMLDivElement;
        const question = input.value;

        input.disabled = true;
        submitButton.disabled = true;

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
            input.disabled = false;
            submitButton.disabled = false;

            input.value = '';
        }
    });

    noteForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const content = quill.root.innerHTML; 
        const submitButton = noteForm.querySelector('button[type="submit"]') as HTMLButtonElement;

        submitButton.disabled = true;

        try {
            const response = await fetch('/notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    content: content,
                }),
            });

            if (response.ok) {
                quill.setText(''); 
                loadNotes(); 
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            submitButton.disabled = false;
        }
    });

    function confirmDelete(noteId: number) {
        if (confirm('Are you sure you want to delete this note?')) {
            deleteNote(noteId);
        }
    }

    async function deleteNote(noteId: number) {
        try {
            const response = await fetch(`/notes/${noteId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                loadNotes();
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
});
