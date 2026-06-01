/** @odoo-module **/
/*
 * Helpdesk Dashboard - ported to OWL for Odoo 17+ / 19.
 *
 * The original file used the legacy `odoo.define` + `AbstractAction` API,
 * which was removed in Odoo 17. This rewrite uses an OWL Component
 * registered in the "actions" registry under the same tag
 * (helpdesk_dashboard_tag) so the existing ir.actions.client record keeps
 * working without changes.
 */

import { Component, useState, onWillStart, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";

export class HelpdeskDashboard extends Component {
    static template = xml`
        <section class="dashboard_main_section" id="main_section_manager">
            <style>
                .dashboard_main_section {
                    height: calc(100vh - 46px);
                    min-height: 0;
                    overflow-y: auto;
                    overflow-x: hidden;
                    background:
                        radial-gradient(circle at top left, rgba(113, 75, 103, 0.14), transparent 32rem),
                        linear-gradient(180deg, #f7f8fb 0%, #eef2f7 100%);
                }
                .dashboard_main_section::-webkit-scrollbar {
                    width: 10px;
                }
                .dashboard_main_section::-webkit-scrollbar-track {
                    background: rgba(226, 232, 240, 0.7);
                }
                .dashboard_main_section::-webkit-scrollbar-thumb {
                    background: rgba(113, 75, 103, 0.45);
                    border: 2px solid rgba(226, 232, 240, 0.7);
                    border-radius: 999px;
                }
                .dashboard_main_section::-webkit-scrollbar-thumb:hover {
                    background: rgba(113, 75, 103, 0.65);
                }
                .o_helpdesk_dashboard {
                    padding: 34px 36px 42px;
                }
                .o_helpdesk_dashboard_header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 16px;
                    margin-bottom: 24px;
                }
                .o_helpdesk_dashboard_eyebrow {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    color: #714b67;
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: 0;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                }
                .o_helpdesk_dashboard_eyebrow:before {
                    content: "";
                    width: 26px;
                    height: 3px;
                    border-radius: 99px;
                    background: #00a09d;
                }
                .o_helpdesk_dashboard_title {
                    color: #243047;
                    margin: 0;
                    font-size: 30px;
                    font-weight: 750;
                    line-height: 1.15;
                }
                .o_helpdesk_dashboard_subtitle {
                    color: #667085;
                    margin: 8px 0 0;
                    font-size: 14px;
                }
                .o_helpdesk_dashboard_filter {
                    display: flex;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 10px;
                    background: rgba(255, 255, 255, 0.78);
                    padding: 10px 12px 10px 14px;
                    border: 1px solid rgba(113, 75, 103, 0.12);
                    border-radius: 12px;
                    box-shadow: 0 10px 28px rgba(30, 41, 59, 0.08);
                    backdrop-filter: blur(10px);
                }
                .o_helpdesk_dashboard_filter label {
                    white-space: nowrap;
                    margin: 0;
                    color: #344054;
                    font-size: 13px;
                    font-weight: 700;
                }
                .o_helpdesk_dashboard_filter select {
                    min-width: 152px;
                    padding: 9px 34px 9px 12px;
                    border: 1px solid #d0d5dd;
                    border-radius: 9px;
                    background: #fff;
                    color: #1f2937;
                    font-weight: 600;
                    outline: none;
                    transition: border-color 150ms ease, box-shadow 150ms ease;
                }
                .o_helpdesk_dashboard_filter select:focus {
                    border-color: #00a09d;
                    box-shadow: 0 0 0 3px rgba(0, 160, 157, 0.14);
                }
                .o_helpdesk_dashboard_date_range {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .o_helpdesk_dashboard_date_range span {
                    color: #667085;
                    font-size: 12px;
                    font-weight: 700;
                }
                .o_helpdesk_dashboard_date_range input {
                    width: 138px;
                    padding: 8px 10px;
                    border: 1px solid #d0d5dd;
                    border-radius: 9px;
                    background: #fff;
                    color: #1f2937;
                    font-weight: 600;
                    outline: none;
                    transition: border-color 150ms ease, box-shadow 150ms ease;
                }
                .o_helpdesk_dashboard_date_range input:focus {
                    border-color: #00a09d;
                    box-shadow: 0 0 0 3px rgba(0, 160, 157, 0.14);
                }
                .o_helpdesk_dashboard_apply {
                    min-height: 38px;
                    padding: 0 14px;
                    border: 0;
                    border-radius: 9px;
                    color: #fff;
                    background: linear-gradient(135deg, #714b67, #00a09d);
                    font-size: 13px;
                    font-weight: 800;
                    box-shadow: 0 10px 20px rgba(113, 75, 103, 0.18);
                    transition: transform 160ms ease, box-shadow 160ms ease, opacity 160ms ease;
                }
                .o_helpdesk_dashboard_apply:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 12px 24px rgba(113, 75, 103, 0.24);
                }
                .o_helpdesk_dashboard_apply:disabled {
                    cursor: not-allowed;
                    opacity: 0.48;
                    transform: none;
                    box-shadow: none;
                }
                .o_helpdesk_dashboard_overview {
                    display: grid;
                    grid-template-columns: minmax(220px, 1fr) 2fr;
                    gap: 18px;
                    margin-bottom: 18px;
                }
                .o_helpdesk_dashboard_total {
                    position: relative;
                    overflow: hidden;
                    min-height: 154px;
                    padding: 22px;
                    border-radius: 8px;
                    color: #fff;
                    background:
                        linear-gradient(135deg, rgba(113, 75, 103, 0.96), rgba(0, 160, 157, 0.88)),
                        #714b67;
                    box-shadow: 0 18px 38px rgba(52, 64, 84, 0.16);
                }
                .o_helpdesk_dashboard_total:after {
                    content: "";
                    position: absolute;
                    right: -36px;
                    bottom: -54px;
                    width: 170px;
                    height: 170px;
                    border: 26px solid rgba(255, 255, 255, 0.13);
                    border-radius: 50%;
                }
                .o_helpdesk_dashboard_total_label,
                .o_helpdesk_dashboard_total_hint {
                    position: relative;
                    margin: 0;
                    color: rgba(255, 255, 255, 0.78);
                    font-size: 13px;
                    font-weight: 700;
                }
                .o_helpdesk_dashboard_total_count {
                    position: relative;
                    display: block;
                    margin-top: 12px;
                    font-size: 52px;
                    font-weight: 800;
                    line-height: 1;
                }
                .o_helpdesk_dashboard_total_hint {
                    margin-top: 14px;
                    max-width: 240px;
                    font-weight: 500;
                }
                .o_helpdesk_dashboard_quick {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 14px;
                }
                .o_helpdesk_dashboard_quick_item {
                    position: relative;
                    overflow: hidden;
                    min-height: 154px;
                    padding: 18px 18px 16px;
                    border: 1px solid rgba(15, 118, 110, 0.26);
                    border-radius: 8px;
                    background:
                        linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 250, 0.92) 100%),
                        #fff;
                    box-shadow:
                        0 18px 36px rgba(15, 23, 42, 0.08),
                        inset 0 1px 0 rgba(255, 255, 255, 0.9);
                    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
                }
                .o_helpdesk_dashboard_quick_item:before {
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;
                    bottom: 0;
                    width: 5px;
                    background: linear-gradient(180deg, #0f766e, #5eead4);
                }
                .o_helpdesk_dashboard_quick_item:after {
                    content: "";
                    position: absolute;
                    right: -44px;
                    top: -52px;
                    width: 150px;
                    height: 150px;
                    border-radius: 50%;
                    background:
                        radial-gradient(circle at center, rgba(15, 118, 110, 0.16), rgba(15, 118, 110, 0.04) 48%, rgba(15, 118, 110, 0) 70%);
                }
                .o_helpdesk_dashboard_quick_item:hover {
                    transform: translateY(-5px);
                    border-color: rgba(15, 118, 110, 0.62);
                    box-shadow:
                        0 24px 46px rgba(15, 23, 42, 0.13),
                        0 0 0 4px rgba(15, 118, 110, 0.08),
                        inset 0 1px 0 rgba(255, 255, 255, 0.95);
                }
                .o_helpdesk_dashboard_quick_top {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                    margin-bottom: 18px;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_quick_icon {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 42px;
                    height: 42px;
                    border: 1px solid rgba(15, 118, 110, 0.14);
                    border-radius: 8px;
                    color: #0f766e;
                    background: rgba(204, 251, 241, 0.72);
                    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.1);
                }
                .o_helpdesk_dashboard_quick_icon svg {
                    width: 21px;
                    height: 21px;
                    fill: none;
                    stroke: currentColor;
                    stroke-width: 2;
                    stroke-linecap: round;
                    stroke-linejoin: round;
                }
                .o_helpdesk_dashboard_quick_badge {
                    display: inline-flex;
                    align-items: center;
                    height: 26px;
                    padding: 0 10px;
                    border: 1px solid rgba(15, 118, 110, 0.15);
                    border-radius: 999px;
                    color: #115e59;
                    background: rgba(255, 255, 255, 0.72);
                    font-size: 11px;
                    font-weight: 800;
                    text-transform: uppercase;
                }
                .o_helpdesk_dashboard_quick_label {
                    position: relative;
                    margin: 0;
                    color: #4b5563;
                    font-size: 13px;
                    font-weight: 800;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_quick_count {
                    position: relative;
                    display: block;
                    margin-top: 14px;
                    color: #243047;
                    font-size: 34px;
                    font-weight: 800;
                    line-height: 1;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_quick_note {
                    position: relative;
                    display: block;
                    margin-top: 18px;
                    padding-top: 12px;
                    border-top: 1px solid rgba(15, 118, 110, 0.12);
                    color: #115e59;
                    font-size: 12px;
                    font-weight: 700;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_cards {
                    display: grid;
                    grid-template-columns: repeat(6, minmax(150px, 1fr));
                    gap: 18px;
                }
                .o_helpdesk_dashboard_card {
                    position: relative;
                    overflow: hidden;
                    min-height: 174px;
                    padding: 18px;
                    border: 1px solid rgba(208, 213, 221, 0.72);
                    border-radius: 8px;
                    background:
                        linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 255, 255, 0.84)),
                        #fff;
                    box-shadow: 0 14px 30px rgba(30, 41, 59, 0.08);
                    text-align: left;
                    cursor: pointer;
                    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
                }
                .o_helpdesk_dashboard_card:hover {
                    transform: translateY(-5px);
                    border-color: var(--helpdesk-card-accent);
                    box-shadow: 0 18px 38px rgba(30, 41, 59, 0.14);
                }
                .o_helpdesk_dashboard_card:before {
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, var(--helpdesk-card-accent), var(--helpdesk-card-accent-soft));
                }
                .o_helpdesk_dashboard_card:after {
                    content: "";
                    position: absolute;
                    right: -38px;
                    top: -38px;
                    width: 104px;
                    height: 104px;
                    border-radius: 50%;
                    background: var(--helpdesk-card-bg);
                }
                .o_helpdesk_dashboard_card_top {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 10px;
                    margin-bottom: 26px;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_card_icon {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 42px;
                    height: 42px;
                    border-radius: 8px;
                    color: var(--helpdesk-card-accent);
                    background: var(--helpdesk-card-bg);
                }
                .o_helpdesk_dashboard_card_icon svg {
                    width: 22px;
                    height: 22px;
                    fill: none;
                    stroke: currentColor;
                    stroke-width: 2;
                    stroke-linecap: round;
                    stroke-linejoin: round;
                }
                .o_helpdesk_dashboard_card_arrow {
                    color: #98a2b3;
                    font-size: 20px;
                    line-height: 1;
                    transition: color 180ms ease, transform 180ms ease;
                }
                .o_helpdesk_dashboard_card:hover .o_helpdesk_dashboard_card_arrow {
                    color: var(--helpdesk-card-accent);
                    transform: translateX(3px);
                }
                .o_helpdesk_dashboard_card_title {
                    position: relative;
                    color: #667085;
                    font-size: 14px;
                    font-weight: 750;
                    margin: 0 0 8px;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_card_count {
                    position: relative;
                    display: block;
                    color: #243047;
                    font-size: 42px;
                    font-weight: 800;
                    line-height: 1;
                    z-index: 1;
                }
                .o_helpdesk_dashboard_card_note {
                    position: relative;
                    display: block;
                    margin-top: 12px;
                    color: #98a2b3;
                    font-size: 12px;
                    font-weight: 650;
                    z-index: 1;
                }
                @media (max-width: 1400px) {
                    .o_helpdesk_dashboard_cards {
                        grid-template-columns: repeat(3, minmax(180px, 1fr));
                    }
                }
                @media (max-width: 992px) {
                    .o_helpdesk_dashboard_overview {
                        grid-template-columns: 1fr;
                    }
                    .o_helpdesk_dashboard_cards {
                        grid-template-columns: repeat(2, minmax(180px, 1fr));
                    }
                }
                @media (max-width: 767px) {
                    .o_helpdesk_dashboard {
                        padding: 20px 16px;
                    }
                    .o_helpdesk_dashboard_header {
                        align-items: stretch;
                        flex-direction: column;
                    }
                    .o_helpdesk_dashboard_filter {
                        justify-content: space-between;
                    }
                    .o_helpdesk_dashboard_quick {
                        grid-template-columns: 1fr;
                    }
                    .o_helpdesk_dashboard_cards {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
            <div class="o_helpdesk_dashboard">
                <div class="o_helpdesk_dashboard_header">
                    <div>
                        <div class="o_helpdesk_dashboard_eyebrow">Helpdesk</div>
                        <h2 class="o_helpdesk_dashboard_title">Helpdesk Dashboard</h2>
                        <p class="o_helpdesk_dashboard_subtitle">Suivi clair des tickets par statut.</p>
                    </div>
                    <div class="o_helpdesk_dashboard_filter">
                        <label for="helpdesk_dashboard_period">Filter by:</label>
                        <select id="helpdesk_dashboard_period"
                                t-on-change="onPeriodChange"
                                t-att-value="state.period">
                            <option value="this_year">This Year</option>
                            <option value="this_month">This Month</option>
                            <option value="this_week">This Week</option>
                            <option value="custom">Période</option>
                        </select>
                        <label for="helpdesk_dashboard_category">Category:</label>
                        <select id="helpdesk_dashboard_category"
                                t-on-change="onCategoryChange"
                                t-att-value="state.categoryId">
                            <option value="">All</option>
                            <option t-foreach="state.categories"
                                    t-as="category"
                                    t-key="category.id"
                                    t-att-value="category.id">
                                <t t-out="category.name"/>
                            </option>
                        </select>
                        <div class="o_helpdesk_dashboard_date_range" t-if="state.period === 'custom'">
                            <span>De</span>
                            <input type="date"
                                   name="dateFrom"
                                   t-att-value="state.dateFrom"
                                   t-on-change="onCustomDateChange"/>
                            <span>a</span>
                            <input type="date"
                                   name="dateTo"
                                   t-att-value="state.dateTo"
                                   t-on-change="onCustomDateChange"/>
                            <button type="button"
                                    class="o_helpdesk_dashboard_apply"
                                    t-att-disabled="!state.dateFrom || !state.dateTo"
                                    t-on-click="applyCustomPeriod">
                                Appliquer
                            </button>
                        </div>
                    </div>
                </div>
                <div class="o_helpdesk_dashboard_overview">
                    <div class="o_helpdesk_dashboard_total">
                        <p class="o_helpdesk_dashboard_total_label">Total tickets</p>
                        <span class="o_helpdesk_dashboard_total_count">
                            <t t-out="totalTickets"/>
                        </span>
                        <p class="o_helpdesk_dashboard_total_hint">Vue consolidée selon la période sélectionnée.</p>
                    </div>
                    <div class="o_helpdesk_dashboard_quick">
                        <div class="o_helpdesk_dashboard_quick_item">
                            <div class="o_helpdesk_dashboard_quick_top">
                                <span class="o_helpdesk_dashboard_quick_icon">
                                    <svg viewBox="0 0 24 24"><path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 15l3-3 3 2 5-7"/></svg>
                                </span>
                                <span class="o_helpdesk_dashboard_quick_badge">Focus</span>
                            </div>
                            <p class="o_helpdesk_dashboard_quick_label">Tickets actifs</p>
                            <span class="o_helpdesk_dashboard_quick_count">
                                <t t-out="activeTickets"/>
                            </span>
                            <span class="o_helpdesk_dashboard_quick_note">Tickets a traiter</span>
                        </div>
                        <div class="o_helpdesk_dashboard_quick_item">
                            <div class="o_helpdesk_dashboard_quick_top">
                                <span class="o_helpdesk_dashboard_quick_icon">
                                    <svg viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/><path d="M4 20h16"/></svg>
                                </span>
                                <span class="o_helpdesk_dashboard_quick_badge">Focus</span>
                            </div>
                            <p class="o_helpdesk_dashboard_quick_label">Tickets finalisés</p>
                            <span class="o_helpdesk_dashboard_quick_count">
                                <t t-out="state.counts.done + state.counts.closed"/>
                            </span>
                            <span class="o_helpdesk_dashboard_quick_note">Tickets termines</span>
                        </div>
                        <div class="o_helpdesk_dashboard_quick_item">
                            <div class="o_helpdesk_dashboard_quick_top">
                                <span class="o_helpdesk_dashboard_quick_icon">
                                    <svg viewBox="0 0 24 24"><path d="M6 6l12 12"/><path d="M18 6L6 18"/><circle cx="12" cy="12" r="9"/></svg>
                                </span>
                                <span class="o_helpdesk_dashboard_quick_badge">Focus</span>
                            </div>
                            <p class="o_helpdesk_dashboard_quick_label">Tickets annulés</p>
                            <span class="o_helpdesk_dashboard_quick_count">
                                <t t-out="state.counts.canceled"/>
                            </span>
                            <span class="o_helpdesk_dashboard_quick_note">Tickets rejetes</span>
                        </div>
                    </div>
                </div>
                <div class="o_helpdesk_dashboard_cards">
                    <button t-foreach="cards"
                            t-as="card"
                            t-key="card.key"
                            type="button"
                            class="o_helpdesk_dashboard_card"
                            t-att-style="'--helpdesk-card-accent: ' + card.accent + '; --helpdesk-card-accent-soft: ' + card.accentSoft + '; --helpdesk-card-bg: ' + card.bg"
                            t-on-click="() => this.openTickets(card.key)">
                        <div class="o_helpdesk_dashboard_card_top">
                            <span class="o_helpdesk_dashboard_card_icon">
                                <svg t-if="card.key === 'new'" viewBox="0 0 24 24"><path d="M12 5v14"/><path d="M5 12h14"/></svg>
                                <svg t-if="card.key === 'draft'" viewBox="0 0 24 24"><path d="M14 4l6 6"/><path d="M5 19l4.5-1 9-9L15 5.5l-9 9L5 19z"/></svg>
                                <svg t-if="card.key === 'in_progress'" viewBox="0 0 24 24"><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="8"/></svg>
                                <svg t-if="card.key === 'canceled'" viewBox="0 0 24 24"><path d="M6 6l12 12"/><path d="M18 6L6 18"/></svg>
                                <svg t-if="card.key === 'done'" viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg>
                                <svg t-if="card.key === 'closed'" viewBox="0 0 24 24"><path d="M7 11V8a5 5 0 0 1 10 0v3"/><rect x="5" y="11" width="14" height="9" rx="2"/></svg>
                            </span>
                            <span class="o_helpdesk_dashboard_card_arrow">&#8250;</span>
                        </div>
                        <h4 class="o_helpdesk_dashboard_card_title">
                            <t t-out="card.label"/>
                        </h4>
                        <span class="o_helpdesk_dashboard_card_count">
                            <t t-out="state.counts[card.key]"/>
                        </span>
                        <span class="o_helpdesk_dashboard_card_note">Ouvrir la liste</span>
                    </button>
                </div>
            </div>
        </section>
    `;
    static props = ["*"];

    setup() {
        this.action = useService("action");
        this.state = useState({
            period: "this_year",
            dateFrom: "",
            dateTo: "",
            categoryId: "",
            categories: [],
            counts: {
                new: 0,
                draft: 0,
                in_progress: 0,
                canceled: 0,
                done: 0,
                closed: 0,
            },
            ids: {
                new_id: [],
                draft_id: [],
                in_progress_id: [],
                canceled_id: [],
                done_id: [],
                closed_id: [],
            },
        });

        onWillStart(async () => {
            this.state.categories = await rpc("/helpdesk_dashboard_categories", {});
            await this._fetchDashboard();
        });
    }

    get cards() {
        return [
            { key: "new", label: _t("New"), accent: "#00a09d", accentSoft: "#38d9c6", bg: "rgba(0, 160, 157, 0.12)" },
            { key: "draft", label: _t("Draft"), accent: "#4763e4", accentSoft: "#7c8cff", bg: "rgba(71, 99, 228, 0.12)" },
            { key: "in_progress", label: _t("In Progress"), accent: "#f59f00", accentSoft: "#ffd43b", bg: "rgba(245, 159, 0, 0.14)" },
            { key: "canceled", label: _t("Cancelled"), accent: "#f03e3e", accentSoft: "#ff8787", bg: "rgba(240, 62, 62, 0.12)" },
            { key: "done", label: _t("Done"), accent: "#2f9e44", accentSoft: "#69db7c", bg: "rgba(47, 158, 68, 0.12)" },
            { key: "closed", label: _t("Closed"), accent: "#714b67", accentSoft: "#b197a8", bg: "rgba(113, 75, 103, 0.13)" },
        ];
    }

    get totalTickets() {
        return Object.values(this.state.counts).reduce((total, count) => total + count, 0);
    }

    get activeTickets() {
        return this.state.counts.new + this.state.counts.draft + this.state.counts.in_progress;
    }

    async _fetch(route, params = {}) {
        const res = await rpc(route, params);
        this.state.counts = {
            new: res.new || 0,
            draft: res.draft || 0,
            in_progress: res.in_progress || 0,
            canceled: res.canceled || 0,
            done: res.done || 0,
            closed: res.closed || 0,
        };
        this.state.ids = {
            new_id: res.new_id || [],
            draft_id: res.draft_id || [],
            in_progress_id: res.in_progress_id || [],
            canceled_id: res.canceled_id || [],
            done_id: res.done_id || [],
            closed_id: res.closed_id || [],
        };
    }

    async onPeriodChange(ev) {
        const value = ev.target.value;
        this.state.period = value;
        if (value === "custom") {
            if (this.state.dateFrom && this.state.dateTo) {
                await this._fetchDashboard();
            }
            return;
        }
        await this._fetchDashboard();
    }

    async onCustomDateChange(ev) {
        this.state[ev.target.name] = ev.target.value;
    }

    async onCategoryChange(ev) {
        this.state.categoryId = ev.target.value;
        if (this.state.period !== "custom" || (this.state.dateFrom && this.state.dateTo)) {
            await this._fetchDashboard();
        }
    }

    async applyCustomPeriod() {
        if (!this.state.dateFrom || !this.state.dateTo) {
            return;
        }
        await this._fetchDashboard();
    }

    async _fetchDashboard() {
        await this._fetch("/helpdesk_dashboard_filtered", {
            period: this.state.period,
            start_date: this.state.dateFrom,
            end_date: this.state.dateTo,
            category_id: this.state.categoryId || false,
        });
    }

    /**
     * Open the list of tickets matching one of the stage buckets.
     * stageKey is one of: new, draft, in_progress, canceled, done, closed.
     */
    openTickets(stageKey) {
        const idsField = `${stageKey}_id`;
        const titles = {
            new: _t("New Tickets"),
            draft: _t("Draft Tickets"),
            in_progress: _t("In Progress Tickets"),
            canceled: _t("Canceled Tickets"),
            done: _t("Done Tickets"),
            closed: _t("Closed Tickets"),
        };
        const ids = this.state.ids[idsField] || [];
        this.action.doAction({
            name: titles[stageKey],
            type: "ir.actions.act_window",
            res_model: "help.ticket",
            view_mode: "list,form",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [["id", "in", ids]],
        });
    }
}

registry.category("actions").add("helpdesk_dashboard_tag", HelpdeskDashboard);
