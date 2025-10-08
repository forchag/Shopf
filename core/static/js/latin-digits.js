(function () {
  const digitMap = {
    '\u0660': '0',
    '\u0661': '1',
    '\u0662': '2',
    '\u0663': '3',
    '\u0664': '4',
    '\u0665': '5',
    '\u0666': '6',
    '\u0667': '7',
    '\u0668': '8',
    '\u0669': '9',
    '\u06F0': '0',
    '\u06F1': '1',
    '\u06F2': '2',
    '\u06F3': '3',
    '\u06F4': '4',
    '\u06F5': '5',
    '\u06F6': '6',
    '\u06F7': '7',
    '\u06F8': '8',
    '\u06F9': '9'
  };

  const digitPattern = /[\u0660-\u0669\u06F0-\u06F9]/g;

  function convertDigits(value) {
    if (!value || typeof value !== 'string') {
      return value;
    }
    return value.replace(digitPattern, (char) => digitMap[char] || char);
  }

  function shouldSkipElement(element) {
    if (!(element instanceof Element)) {
      return true;
    }

    const tagName = element.tagName;
    return tagName === 'SCRIPT' || tagName === 'STYLE' || tagName === 'CODE' || tagName === 'PRE';
  }

  function convertTextNodes(node) {
    if (node.nodeType === Node.DOCUMENT_FRAGMENT_NODE) {
      node.childNodes.forEach(convertTextNodes);
      return;
    }

    if (node.nodeType === Node.TEXT_NODE) {
      const newValue = convertDigits(node.textContent);
      if (newValue !== node.textContent) {
        node.textContent = newValue;
      }
      return;
    }

    if (node.nodeType === Node.ELEMENT_NODE && !shouldSkipElement(node)) {
      const element = node;

      if (element.childNodes.length) {
        element.childNodes.forEach(convertTextNodes);
      }

      if ('value' in element && typeof element.value === 'string') {
        const updatedValue = convertDigits(element.value);
        if (updatedValue !== element.value) {
          element.value = updatedValue;
        }
      }

      if (element.hasAttribute && element.hasAttribute('placeholder')) {
        const placeholder = element.getAttribute('placeholder');
        const updatedPlaceholder = convertDigits(placeholder);
        if (updatedPlaceholder !== placeholder) {
          element.setAttribute('placeholder', updatedPlaceholder);
        }
      }

      Array.from(element.attributes || []).forEach((attr) => {
        if (!attr.value) {
          return;
        }
        const updated = convertDigits(attr.value);
        if (updated !== attr.value) {
          element.setAttribute(attr.name, updated);
        }
      });
    }
  }

  function handleMutations(mutations) {
    mutations.forEach((mutation) => {
      if (mutation.type === 'characterData' && mutation.target.nodeType === Node.TEXT_NODE) {
        convertTextNodes(mutation.target);
      }

      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.TEXT_NODE || node.nodeType === Node.ELEMENT_NODE) {
            convertTextNodes(node);
          }
        });
      }

      if (mutation.type === 'attributes' && mutation.target.nodeType === Node.ELEMENT_NODE) {
        convertTextNodes(mutation.target);
      }
    });
  }

  function initializeDigitConversion() {
    convertTextNodes(document.body);

    const observer = new MutationObserver(handleMutations);
    observer.observe(document.body, {
      characterData: true,
      subtree: true,
      childList: true,
      attributes: true
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDigitConversion);
  } else {
    initializeDigitConversion();
  }
})();
