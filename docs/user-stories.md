
# User Stories — Smart Farmer-to-Buyer Management System

## 1. Introduction

This document describes the primary user needs for the Smart Farmer-to-Buyer Management System. The user stories guide requirements analysis, product backlog development, prioritisation, and incremental delivery.

The main users are farmers who list agricultural produce and buyers who search for produce and identify suitable suppliers.

## 2. User Stories

### US-01: User Registration

**User:** Farmer / Buyer

As a farmer or buyer, I want to create an account using my details and user role, so that I can access the platform's features according to my needs.

**Acceptance Criteria**
- Given a user who has not registered, when they submit valid registration details, then an account is created.
- Given a user who submits invalid or incomplete details, when they attempt to register, then the system displays appropriate validation feedback.
- The system prevents duplicate accounts according to the chosen account-identification rules.

### US-02: User Authentication

**User:** Registered Farmer / Buyer

As a registered farmer or buyer, I want to log in and log out securely, so that I can access my account and protect it from unauthorised access.

**Acceptance Criteria**
- Given a registered user with valid credentials, when they log in, then the system grants access to their account.
- Given a user with invalid credentials, when they attempt to log in, then access is denied and an appropriate error message is displayed.
- When an authenticated user logs out, then their authenticated session ends.

### US-03: Farmer Inventory and Pricing

**User:** Farmer

As a farmer, I want to create produce listings with crop details, quantity, price, location, availability, photos, and minimum purchase quantities, so that buyers can understand what I have available and the terms of purchase.

**Acceptance Criteria**
- Given an authenticated farmer, when they submit valid listing details, then the system saves and publishes the listing.
- The listing displays the information provided by the farmer.
- Where supported, the farmer can specify photos and a minimum purchase quantity.

### US-04: Manage Produce Listings

**User:** Farmer

As a farmer, I want to update or deactivate my produce listings, so that buyers can see accurate information about what I currently have available.

**Acceptance Criteria**
- Given a farmer who owns a listing, when they update its details, then the system saves the changes.
- When the farmer deactivates a listing, then it is no longer presented as available.
- A farmer cannot modify another farmer's listing without appropriate authorisation.

### US-05: Buyer Marketplace Search

**User:** Buyer

As a buyer, I want to search and filter produce listings by crop type, location, and price range, so that I can quickly find produce that meets my requirements.

**Acceptance Criteria**
- Given available produce listings, when a buyer selects a crop and location filter, then the system displays listings matching those criteria.
- When a buyer specifies a price range, then the results reflect that range.
- Unavailable listings are excluded from available-stock search results.

### US-06: Buyer Views and Selects Matches

**User:** Buyer

As a buyer, I want to view and compare suitable farmers recommended by the system, so that I can choose a supplier who best meets my requirements.

**Acceptance Criteria**
- Given a buyer's produce requirements and available farmer listings, when matching is performed, then the system presents suitable results according to the implemented matching criteria.
- Where available, the buyer can compare relevant details such as price, quantity, and location.
- The buyer can select a suitable farmer or listing for further engagement.

### US-07: Farmer/Buyer Communication

**User:** Farmer / Buyer

As a farmer or buyer, I want to communicate with a matched user, so that we can discuss produce, quantity, price, delivery, and other transaction details before completing the trade.

**Acceptance Criteria**
- Given two users who have been matched, when an authorised user initiates communication, then the system allows them to exchange messages using the supported communication feature.
- Communication is restricted to authorised participants.
- The system provides appropriate feedback when a message cannot be sent.

### US-08: Buyer Order Tracking

**User:** Buyer

As a buyer, I want to view the status of my active purchase, so that I can understand the current stage of my order and its expected delivery.

**Acceptance Criteria**
- Given a buyer with an existing order, when they open the order details, then the system displays the current order status.
- When the order status changes, the updated status is reflected in the system.
- Delivery milestones and estimated arrival information are displayed when supported and available.

## 3. Relationship to the Product Backlog

These user stories describe user needs. They may be decomposed into smaller Product Backlog Items for estimation, prioritisation, and implementation.

The first increment focuses on **US-01: User Registration** and **US-02: User Authentication**. Subsequent increments are expected to introduce produce listing management, marketplace search, matching, communication, and order tracking.

The planned sequence may be adjusted as the team receives feedback, identifies dependencies, and reviews technical feasibility.
