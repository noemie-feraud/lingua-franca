(function () {
    "use strict";

    const form = document.getElementById("translation-form");
    const sourceText = document.getElementById("source-text");
    const sourceLang = document.getElementById("source-lang");
    const targetLang = document.getElementById("target-lang");
    const targetText = document.getElementById("target-text");
    const translateButton = document.getElementById("translate-button");
    const statusMessage = document.getElementById("status-message");
    const detectedLanguage = document.getElementById("detected-language");

    // Delay (ms) after the last keystroke before triggering detection.
    // Keeps the server from being hit on every single character typed.
    const DETECTION_DEBOUNCE_MS = 500;

    // Holds the last detected language code, used when the user keeps
    // "auto" selected and clicks Translate.
    let lastDetectedLang = null;

    // Timer reference for the debounce mechanism.
    let detectionTimer = null;

    /**
     * Map of ISO 639-1 codes to display names. Only used to show a
     * friendly label in the "Detected language" indicator.
     */
    const LANGUAGE_NAMES = {
        fr: "French", en: "English", es: "Spanish", de: "German",
        it: "Italian", pt: "Portuguese", nl: "Dutch", pl: "Polish",
        ru: "Russian", ja: "Japanese", zh: "Chinese", ar: "Arabic",
    };

    /**
     * Display the detected language in the UI. Falls back to the raw
     * code if the language is not in our friendly-name map.
     */
    function showDetectedLanguage(code) {
        const name = LANGUAGE_NAMES[code] || code;
        detectedLanguage.textContent = `Detected: ${name}`;
    }

    /**
     * Clear the detected-language indicator (used when the user
     * switches away from auto-detect or empties the text field).
     */
    function clearDetectedLanguage() {
        detectedLanguage.textContent = "";
        lastDetectedLang = null;
    }

    /**
     * Call the /detect endpoint with the current text. Updates the UI
     * with the detected language, or silently does nothing on error
     * (detection failures during typing are expected on short inputs).
     */
    async function detectLanguage() {
        const text = sourceText.value.trim();
        if (!text) {
            clearDetectedLanguage();
            return;
        }

        try {
            const response = await fetch("/detect", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: text }),
            });

            if (!response.ok) {
                // Most likely "text too short" — fine during typing.
                return;
            }

            const data = await response.json();
            lastDetectedLang = data.language;
            showDetectedLanguage(data.language);
        } catch (err) {
            // Network errors during background detection should not
            // surface to the user; they'll see the error when they
            // click Translate if it persists.
            console.error("Detection failed:", err);
        }
    }

    /**
     * Send the current form state to /translate and display the result.
     * When source language is "auto", uses the last detected language;
     * if none is available yet, sends "auto" and lets the server handle it.
     */
    async function translate() {
        const text = sourceText.value.trim();
        if (!text) {
            statusMessage.textContent = "Please enter some text to translate.";
            return;
        }

        // If auto-detect is selected, prefer the language we already
        // detected client-side. Falls back to "auto" if detection
        // hasn't run yet (e.g. user clicked Translate very quickly).
        let effectiveSourceLang = sourceLang.value;
        if (effectiveSourceLang === "auto") {
            effectiveSourceLang = lastDetectedLang || "auto";
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
                    source_lang: effectiveSourceLang,
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

    // -------------------------------------------------------------------
    // Event listeners
    // -------------------------------------------------------------------

    // Debounced detection on every keystroke. Only runs when the user
    // has the source language set to "auto" — otherwise there is
    // nothing to detect.
    sourceText.addEventListener("input", function () {
        if (sourceLang.value !== "auto") {
            return;
        }
        clearTimeout(detectionTimer);
        detectionTimer = setTimeout(detectLanguage, DETECTION_DEBOUNCE_MS);
    });

    // Clear the detected indicator when the user switches away from
    // auto-detect (no longer relevant).
    sourceLang.addEventListener("change", function () {
        if (sourceLang.value === "auto") {
            // Switched back to auto: re-run detection on current text.
            detectLanguage();
        } else {
            clearDetectedLanguage();
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        translate();
    });
})();
