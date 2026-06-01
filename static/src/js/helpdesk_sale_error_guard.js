/** @odoo-module **/

import { registry } from "@web/core/registry";

const HELPDESK_SELECTORS = [
    ".website_ticket",
    "form#Ticket_form",
    "form[action='/helpdesk_ticket/submit']",
    "form[action*='/rating/']",
];

function isHelpdeskPage() {
    return HELPDESK_SELECTORS.some((selector) => document.querySelector(selector));
}

function isSaleDatasetError(error) {
    const message = String(error?.message || error || "");
    const stack = String(error?.stack || "");
    return (
        message.includes("Cannot read properties of null")
        && message.includes("dataset")
        && (
            stack.includes("SaleUpdateLineButton")
            || stack.includes("SafeSaleUpdateLineButton")
        )
    );
}

function isNullDatasetError(error) {
    const message = String(error?.message || error || "");
    return (
        message.includes("Cannot read properties of null")
        && message.includes("dataset")
    );
}

function patchSaleUpdateLineButton() {
    const interactions = registry.category("public.interactions");
    if (interactions.__helpdeskSalePatchApplied) {
        return;
    }
    interactions.__helpdeskSalePatchApplied = true;

    const originalAdd = interactions.add.bind(interactions);
    interactions.add = function (key, InteractionClass, options) {
        const keyName = String(key || "");
        const className = String(InteractionClass?.name || "");
        const isSaleUpdateLineButton = (
            className === "SaleUpdateLineButton"
            || keyName.includes("SaleUpdateLineButton")
            || keyName.includes("sale_update_line")
            || keyName.includes("update_line")
        );
        if (!isSaleUpdateLineButton) {
            return originalAdd(key, InteractionClass, options);
        }

        class SafeSaleUpdateLineButton extends InteractionClass {
            setup(...args) {
                try {
                    return super.setup(...args);
                } catch (error) {
                    if (isNullDatasetError(error)) {
                        return;
                    }
                    throw error;
                }
            }
        }
        return originalAdd(key, SafeSaleUpdateLineButton, options);
    };
}

patchSaleUpdateLineButton();

window.addEventListener(
    "unhandledrejection",
    (event) => {
        if (isHelpdeskPage() && isNullDatasetError(event.reason)) {
            event.preventDefault();
            event.stopImmediatePropagation();
        }
    },
    true
);

window.addEventListener(
    "error",
    (event) => {
        if (isHelpdeskPage() && isNullDatasetError(event.error)) {
            event.preventDefault();
            event.stopImmediatePropagation();
        }
    },
    true
);
