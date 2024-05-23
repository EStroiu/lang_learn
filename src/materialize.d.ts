declare module 'materialize-css' {
    interface Textarea {
        textareaAutoResize(element: HTMLTextAreaElement): void;
    }

    export const textarea: Textarea;
}

declare const M: {
    textareaAutoResize(element: HTMLTextAreaElement): void;
};
