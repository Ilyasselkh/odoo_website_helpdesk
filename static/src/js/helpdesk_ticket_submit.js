/** @odoo-module **/

const TICKET_FORM_SELECTOR = "form#Ticket_form";
const SUBMIT_SELECTOR = `${TICKET_FORM_SELECTOR} .s_website_form_send, ${TICKET_FORM_SELECTOR} button[type='submit']`;
const HELPDESK_PAGE_SELECTOR = ".website_ticket, form#Ticket_form, form[action*='rating']";
const SALE_CLASSES = ["a-submit", "js_quantity", "js_add_cart_json", "js_delete_product"];

function disableSaleInteractions(root = document) {
    const isHelpdeskPage = Boolean(
        document.querySelector(HELPDESK_PAGE_SELECTOR)
        || root.matches?.(HELPDESK_PAGE_SELECTOR)
        || root.closest?.(HELPDESK_PAGE_SELECTOR)
        || root.querySelector?.(HELPDESK_PAGE_SELECTOR)
    );
    if (!isHelpdeskPage) {
        return;
    }
    for (const className of SALE_CLASSES) {
        const elements = [
            ...(root.matches?.(`.${className}`) ? [root] : []),
            ...root.querySelectorAll(`.${className}`),
        ];
        for (const element of elements) {
            if (!element.closest(".oe_website_sale, .o_wsale_product_page, .o_cart, #shop_cart")) {
                element.classList.remove(className);
            }
        }
    }
}

function prepareTicketForm(form) {
    form.setAttribute("action", "/helpdesk_ticket/submit");
    form.setAttribute("method", "post");
    form.setAttribute("enctype", "multipart/form-data");
    form.removeAttribute("data-model_name");
    form.removeAttribute("data-success-mode");
    form.removeAttribute("data-success-page");
}

function submitTicketForm(form) {
    prepareTicketForm(form);
    if (typeof form.submit === "function") {
        form.submit();
    }
}

disableSaleInteractions();

document.addEventListener(
    "click",
    (ev) => {
        const submitButton = ev.target.closest(SUBMIT_SELECTOR);
        if (!submitButton) {
            return;
        }
        const form = submitButton.closest(TICKET_FORM_SELECTOR);
        if (!form) {
            return;
        }
        ev.preventDefault();
        ev.stopImmediatePropagation();
        submitTicketForm(form);
    },
    true
);

document.addEventListener(
    "submit",
    (ev) => {
        const form = ev.target.closest(TICKET_FORM_SELECTOR);
        if (!form || form.action.endsWith("/helpdesk_ticket/submit")) {
            return;
        }
        ev.preventDefault();
        ev.stopImmediatePropagation();
        submitTicketForm(form);
    },
    true
);

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        disableSaleInteractions();
        const form = document.querySelector(TICKET_FORM_SELECTOR);
        if (form) {
            prepareTicketForm(form);
        }
    });
} else {
    disableSaleInteractions();
    const form = document.querySelector(TICKET_FORM_SELECTOR);
    if (form) {
        prepareTicketForm(form);
    }
}

new MutationObserver((mutations) => {
    for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {
            if (node.nodeType === Node.ELEMENT_NODE) {
                disableSaleInteractions(node);
            }
        }
    }
}).observe(document.documentElement, { childList: true, subtree: true });
