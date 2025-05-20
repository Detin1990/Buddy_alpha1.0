# There used to be some cool stuff here, but it has been redacted for ethical concerns 😔
# This section may have interacted with a third-party interface in a way that could raise eyebrows.
console.log("[Buddy 4.0] content.js loaded");



};

function checkAndRelayTag(tag) {
  chrome.storage.local.get({ seenTags: [] }, ({ seenTags }) => {
    if (seenTags.includes(tag)) {
      console.log("[Buddy 4.0] Skipping already seen tag:", tag);
      return;
    }

    } else {
    }

    chrome.storage.local.set({ seenTags: [...seenTags, tag] });
  });
}

setInterval(() => {
  const messages = Array.from(document.querySelectorAll("div[data-message-author-role='user'], div[data-message-author-role='assistant']"));
  const last = messages[messages.length - 1];
  if (!last) return;

  const txt = last.innerText || last.textContent || "";
  const lines = txt.split("\n");

  for (const line of lines) {
    const match = line.trim().match(/^!exec:[^\n]+!$/);
    if (match) {
      const tag = match[0].trim();
      checkAndRelayTag(tag);
      break; // Only relay one tag per interval
    }
  }
}, 1000);
