# Crow Email

Crow Email is a Home Assistant integration and Lovelace card that brings your email into your dashboards. Designed with an **iPhone Mail** look and feel, the card gives each person their own iCloud, Gmail, Yahoo, Outlook or other accounts, with a unified Inbox, VIPs, swipes, search, Remind Me, Send Later and parcel tracking — while the integration talks to your mail servers from your own Home Assistant, sends phone notifications through the Companion app and gives every account sensors, events and actions for your automations.

Everything is **private to each person** — no cloud service of its own.

> **One download installs both.** The card is bundled inside the integration and loads into your dashboards automatically — no resource to add.

> **AI features are optional and off by default.** Turn on **AI Features** in the card editor to unlock them — they use the AI Task you've already set up in Home Assistant. With AI off, everything else in the card works as normal.

**Step 1 — Add the repository to HACS:**

[![Open your Home Assistant instance and add this repository to HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jamesmcginnis&repository=crow-email&category=integration)

**Step 2 — After downloading and restarting, add the integration:**

[![Open your Home Assistant instance and start setting up Crow Email.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=crow_email)

**Step 3 — Add the card to a dashboard:**

[![Open your Home Assistant instance and show your dashboards.](https://my.home-assistant.io/badges/lovelace_dashboards.svg)](https://my.home-assistant.io/redirect/lovelace_dashboards/)

## Key Features

- **iPhone Mail Design** — Liquid Glass bars, large titles and swipe actions
- **Every Account in One Place** — iCloud, Gmail, Yahoo, Outlook and any IMAP account, with All Inboxes, VIP, Flagged, Unread, Today and Attachments
- **Side by Side** — mailboxes, the list and the email together on a tablet or computer
- **Swipes, Press and Hold, and Select Emails** — archive, delete, flag, move and more
- **Search, Remind Me, Send Later and Undo Send**
- **Pin to Top, Conversations and Export as PDF**
- **Rich Writing** — formatting, attachments, signatures, voting buttons, invitations and contact cards
- **Inbox Tools** — Snooze, Mute Conversation, the Screener, Subscriptions, Sweep, Custom Swipes, Today and keyboard shortcuts (each off until switched on)
- **Parcels** — tracking numbers found in delivery emails, with an Arriving Today section
- **Food Orders and Supermarket Deliveries** — takeaways with when they should arrive, and supermarket slots with substitutions and missing items, each in a mailbox of its own
- **Travel, Home Visits, Tickets, Returns and Refunds, Renewals, Council and Local, and Receipts** — each in a mailbox of its own, with sensors for automations
- **Sign-in Codes** — the latest code at the top of the Inbox with Copy, for 10 minutes
- **Add to Calendar** — tap a date in an email
- **Skins** — iPhone, Airmail, Gmail, Outlook, Spark, Superhuman, Proton Mail and old-school Outlook Express, Hotmail 2000, You've Got Mail, Terminal, iPhone OS 3, BlackBerry and Mac OS 9
- **Group by Type** — optional: the Inbox in sections, like Spark
- **Backgrounds, Colours and Full Screen**
- **Privacy** — images hidden until you choose, trackers blocked, ads removed, and Hide My Location
- **Spam and Scam Protection** — Report Spam, Block Sender, Report Phishing and scam warnings

## AI Features

All optional, and each can be switched off individually:

- **Catch Up, Summaries and Ask About This Email**
- **Smart Replies, Writing Tools and Tone Check**
- **Translate, Describe Pictures and Smart Search**
- **Smart Notifications and Smart Categories**
- **Parcel Tracker, Food Orders, Supermarket Deliveries, Appointments and Bills**
- **Morning Briefing** — a summary of your day, as a notification or read aloud
- **Smart Snooze, Screener Insights, Subscription Notes and Inbox Tidy-Up**
- **Contacts from Signatures, Follow-Up Nudges and Write the Follow-Up**
- **AI Rules, Email Details for Automations and Ask Your Email**

## Integration

- **Phone Notifications** — through the Companion app, with Reply, Mark as Read, Archive and more
- **Quiet Hours, Rules and the App Icon Badge**
- **Email Home Assistant** — email yourself `HA:` questions and Assist answers
- **Sensors** — unread (in total and for each Inbox group), VIP, latest email, today, flagged, drafts, junk, parcels, out for delivery, food orders, supermarket deliveries, monthly spend, travel, away on a trip, home visits, events, refunds, renewals, council updates, warranties, bills due and overdue, snoozed, reminders, waiting for a reply, the Screener, subscriptions and more, for every account
- **Actions** — `crow_email.send_email`, `mark_as_read`, `archive`, `move_to_folder`, `flag`, `refresh` and `update_badge`
- **Events** — `crow_email_received`, `crow_email_sent`, `crow_email_details`, `crow_email_parcel`, `crow_email_food`, `crow_email_grocery`, `crow_email_travel`, `crow_email_visit`, `crow_email_council`, `crow_email_action`, `crow_email_vote` and more

## Installation

1. Add `https://github.com/jamesmcginnis/crow-email` as an **Integration** custom repository in HACS
2. Search for **Crow Email** and click **Download**
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → + Add Integration**, search for **Crow Email** and click **Submit**
5. Hard-refresh your browser, or close and reopen the HA app on your iPhone
6. Add the **Crow Email** card to a dashboard, then tap **Add Account**

Or copy `custom_components/crow_email` from the [Releases](../../releases/latest) page into `/config/custom_components/`, restart, and add the integration.

> iCloud, Gmail and Yahoo need an **app password**. Outlook needs a one-off Microsoft app registration — the README explains how.

## Doorbell Example

```yaml
alias: Doorbell snapshot by email
triggers:
  - trigger: state
    entity_id: binary_sensor.doorbell
    to: "on"
actions:
  - action: camera.snapshot
    target:
      entity_id: camera.front_door
    data:
      filename: /config/www/snapshots/doorbell.jpg
  - action: crow_email.send_email
    data:
      account: me@icloud.com
      to: me@icloud.com
      subject: Someone is at the front door
      attachments:
        - /local/snapshots/doorbell.jpg
```

## Quick Start

```yaml
type: custom:crow-email-card
card_height: 700
appearance: auto
style: glass
```

> **Note:** Everything above can be set from the visual editor. Household settings are stored by the integration and set from the editor by an administrator.
