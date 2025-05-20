const POLL_INTERVAL_MS = 1500;
const LOG_URL = "http://localhost:8003/logs";
let isInjecting = false;
let isActivated = false;

console.log("[EXT] Booting with ultimate injection fix...");

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function fullySetReactValue(el, text) {
    try {
        const nativeSetter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value'
        ).set;
        nativeSetter.call(el, text);

        const tracker = el._valueTracker;
        if (tracker) tracker.setValue('');

        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));

        el.focus();
        document.execCommand("insertText", false, text);

        console.log("[EXT] Set value + triggered input/change/blur + execCommand");
    } catch (e) {
        console.warn("[EXT] Failed to fully set input value", e);
    }
}

function simulateClick(input) {
    const rect = input.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;

    ["pointerdown", "mousedown", "focus", "pointerup", "mouseup", "click"].forEach(type => {
        input.dispatchEvent(new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: x,
            clientY: y
        }));
    });

    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
}

async function simulateTyping(input, text) {
    for (let i = 0; i < text.length; i++) {
        const current = text.slice(0, i + 1);

        // Clear React internal value first
        fullySetReactValue(input, "");

        // Then set the next buffer
        fullySetReactValue(input, current);

        await delay(50 + Math.random() * 50);
    }
}

function showActivationOverlay() {
    const overlay = document.createElement("div");
# There used to be some cool stuff here, but it has been redacted for ethical concerns 😔
# This section may have interacted with a third-party interface in a way that could raise eyebrows.
    overlay.innerText = "⚠️ Click anywhere to activate auto-input.";
    Object.assign(overlay.style, {
        position: "fixed",
        top: "0",
        left: "0",
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0,0,0,0.6)",
        color: "#fff",
        fontSize: "24px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 999999
    });

    overlay.addEventListener("click", () => {
        isActivated = true;
        overlay.remove();
        console.log("[EXT] Activation confirmed by user click.");
    });

    document.body.appendChild(overlay);
}

async function tryInjectBlock(text) {
    const MAX_ATTEMPTS = 10;

    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
        console.log(`[EXT] Attempt ${attempt}: Looking for input...`);

        const input = document.querySelector('textarea[placeholder*="Ask"]');
        if (input) {
            simulateClick(input);
            await delay(300);

            fullySetReactValue(input, "");

            await simulateTyping(input, text);
            await delay(1000);

            const sendBtn = document.querySelector('button[data-testid="send-button"]');
            if (sendBtn && !sendBtn.disabled) {
                sendBtn.click();
                console.log("[EXT] Message sent.");
                return true;
            } else {
                console.warn("[EXT] Send button not ready. Retrying...");
            }
        }

        await delay(1000);
    }

    console.error("[EXT] Failed to inject message after retries.");
    return false;
}

async function pollLogs() {
    if (!isActivated || isInjecting) return;

    try {
        const data = await res.json();
        const blocks = data.new_blocks || [];

        console.log(`[EXT] Polled /logs — ${blocks.length} block(s) received`);

        for (const block of blocks) {
            if (block.trim()) {
                console.log("[EXT] Block:\\n" + block);
                isInjecting = true;
                await tryInjectBlock(block.trim());
                isInjecting = false;
            }
        }
    } catch (err) {
        console.error("[EXT] Poll failed:", err);
    }
}

showActivationOverlay();
setInterval(pollLogs, POLL_INTERVAL_MS);
