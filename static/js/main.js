(function () {
    "use strict";

    const form = document.getElementById("translation-form");
    const sourceText = document.getElementById("source-text");
    const sourceLang = document.getElementById("source-lang");
    const targetLang = document.getElementById("target-lang");
    const targetText = document.getElementById("target-text");
    const translateButton = document.getElementById("translate-button");
    const statusMessage = document.getElementById("status-message");

    /**
     * Send the current form state to the /translate endpoint and display
     * the result. All errors are surfaced to the user via the status line.
     */
    async function translate() {
        const text = sourceText.value.trim();
        if (!text) {
            statusMessage.textContent = "Please enter some text to translate.";
            return;
        }

        translateButton.disabled = true;
        statusMessage.textContent = "Translating...";
        targetText.value = "";

        try {
            const response = await fetch("/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    source_lang: sourceLang.value,
                    target_lang: targetLang.value,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                statusMessage.textContent = data.error || "Translation failed.";
                return;
            }

            targetText.value = data.translation;
            statusMessage.textContent = "Done.";
        } catch (err) {
            statusMessage.textContent = "Network error. Please try again.";
            console.error(err);
        } finally {
            translateButton.disabled = false;
        }
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        translate();
    });
})();
