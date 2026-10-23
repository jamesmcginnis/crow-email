# Crow Email

Crow Email is a Home Assistant integration and Lovelace card that brings your email into your dashboards. Designed with an **iPhone Mail** look and feel, the card gives each person their own iCloud, Gmail, Yahoo, Outlook or other accounts, with a unified Inbox, VIPs, swipes, search, Remind Me, Send Later, parcel tracking and much more — while the integration talks to your mail servers from your own Home Assistant, sends phone notifications through the Companion app and gives every account sensors, events and actions for your automations.

Everything is **private to each person** — your accounts, contacts and settings are only visible to you in the card, and your email stays between your Home Assistant and your mail provider. No cloud service of its own.

> **One download installs both.** The card is bundled inside the integration and is loaded into your dashboards automatically — there's no separate resource to add.

> **AI features are optional and off by default.** Turn on **AI Features** in the card editor to unlock them — they use the AI Task you've already set up in Home Assistant (see [AI Features Setup](#ai-features-setup-optional) below). With AI off, everything else in the card works as normal.

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.8+-blue)
![HACS](https://img.shields.io/badge/HACS-Custom-orange)

**Step 1 — Add the repository to HACS:**

[![Open your Home Assistant instance and add this repository to HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jamesmcginnis&repository=crow-email&category=integration)

**Step 2 — After downloading and restarting, add the integration:**

[![Open your Home Assistant instance and start setting up Crow Email.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=crow_email)

**Step 3 — Add the card to a dashboard:**

[![Open your Home Assistant instance and show your dashboards.](https://my.home-assistant.io/badges/lovelace_dashboards.svg)](https://my.home-assistant.io/redirect/lovelace_dashboards/)

Open a dashboard, click **Edit** → **+ Add Card** and search for **Crow Email**. Then tap **Add Account** in the card.

---

## Installation

### Via HACS (Recommended)

1. Click the **Add to HACS** button above, or in Home Assistant open **HACS** → **⋮ menu** (top right) → **Custom repositories**
2. Add `https://github.com/jamesmcginnis/crow-email` as an **Integration** repository, then close
3. Search for **Crow Email** and click **Download**
4. **Restart Home Assistant**
5. Click the **Add Integration** button above, or go to **Settings → Devices & Services → + Add Integration** and search for **Crow Email**
6. Click **Submit** — there's nothing to fill in, accounts are added from the card
7. Hard-refresh your browser (Cmd+Shift+R on Mac) or close and reopen the Home Assistant app on your iPhone
8. Click the **Add Card** button above, edit a dashboard, click **+ Add Card** and search for **Crow Email**
9. In the card, tap **Add Account** and choose iCloud, Gmail, Yahoo, Outlook or Other

### Manual

1. Download this repository from [Releases](../../releases/latest)
2. Copy the `custom_components/crow_email` folder into `/config/custom_components/` on your Home Assistant instance
3. Restart Home Assistant, then add the integration under **Settings → Devices & Services → + Add Integration**
4. Hard-refresh your browser and add the **Crow Email** card to a dashboard

> **You don't need to add a dashboard resource.** The integration serves the card and registers it automatically. If you previously added `crow-email-card.js` as a resource by hand, remove it under **Settings → Dashboards → Resources** so only the bundled copy loads.

> **After an update,** restart Home Assistant so the new card is loaded. The version is shown at the bottom of the card's **Settings**.

> **Tip:** Crow Email works best on a dashboard of its own — use a **Panel** view, or tap the **Full Screen** button at the top of the Mailboxes to give the card the whole screen. On a tablet or computer the mailboxes, the list and the email sit side by side.

---

## Adding Accounts

Each person adds their own accounts in the card (**Settings → Add Account**). Only they can see them.

| Provider | How to sign in |
|----------|----------------|
| **iCloud** | An app-specific password: [appleid.apple.com](https://appleid.apple.com) → **Sign-In and Security** → **App-Specific Passwords** |
| **Gmail** | An App Password: [myaccount.google.com](https://myaccount.google.com) → **Security** → **2-Step Verification** → **App passwords** |
| **Yahoo** | An app password: **Yahoo Account Security** → **Generate app password** |
| **Outlook** (Outlook.com, Hotmail, Live and Microsoft 365) | Sign in with Microsoft: a short code is shown, you open **microsoft.com/devicelogin** on any device and sign in. Needs a one-off app registration — see below |
| **Other** | Your provider's IMAP and SMTP server settings |

Passwords and Microsoft sign-in tokens are kept by Home Assistant, never in the card.

### Microsoft (Outlook) Setup

Microsoft only lets apps it knows sign in to Outlook, so an administrator registers Crow Email once (free, about five minutes):

1. Go to [entra.microsoft.com](https://entra.microsoft.com) (or the Azure portal) and sign in with any Microsoft account
2. Open **App registrations** → **New registration**
3. Name it **Crow Email**, and under **Supported account types** choose **Accounts in any organizational directory and personal Microsoft accounts**. Leave **Redirect URI** empty, then click **Register**
4. Open **Authentication** → **Advanced settings**, set **Allow public client flows** to **Yes**, and click **Save**
5. Open **API permissions** → **Add a permission** → **APIs my organization uses** → **Office 365 Exchange Online** → **Delegated permissions**, tick **IMAP.AccessAsUser.All** and **SMTP.Send**, and click **Add permissions**
6. On the **Overview** page, copy the **Application (client) ID**
7. In the card editor, open **Accounts and Sending** and paste it into **Application (Client) ID**. Leave **Tenant** as `common` for personal and work accounts, or enter your organisation's tenant ID to allow only its accounts

> For Microsoft 365 work or school accounts, an administrator may need to grant consent for the permissions, and **Authenticated SMTP** must be allowed for the mailbox in the Microsoft 365 admin centre.

---

## AI Features Setup (Optional)

AI features are **off by default** — the card works fully without them. They use an **AI Task** entity, so no extra accounts or keys are added to the card:

1. Add an AI integration (such as OpenAI, Google Gemini, Anthropic or Ollama) under **Settings → Devices & Services**
2. Choose a preferred AI Task under **Settings → System → General → AI suggestions**, or pick one in the card editor
3. In the card editor's **AI** section, switch on **AI Features**

Each feature can be switched off on its own. The reading and writing features only send an email to the AI when someone uses them. The ones that read new email as it arrives (Smart Notifications, Smart Categories, the Parcel Tracker and so on) can be turned off individually if you'd rather they didn't.

> The email is always treated as something to read, not instructions to follow, so an email that says "forward me your passwords" is just summarised.

---

## Features

### Mail

- **iPhone Mail design** — Liquid Glass bars, large titles, swipe actions and smooth page transitions
- **Every account in one place** — All Inboxes, VIP, Flagged, Unread, Today and Attachments, plus each account's own folders
- **Side by side on a wide screen** — mailboxes, the list and the email together on a tablet, a computer or a Panel view
- **Swipes** — swipe right for Read and Pin, left for More, Flag and Archive (or Delete), with a long swipe to archive. Turn on **Custom Swipes** and each person chooses their own
- **Press and hold an email** — Reply, Forward, Mark as Read, Flag, Remind Me, Move, Export as PDF, Report Spam, Archive and Delete
- **Select Emails** — mark, move, copy, archive or delete several at once
- **Search** — across every account, with filters for unread, flagged, VIPs, attachments and today
- **Remind Me** — an email comes back to the top of the Inbox, with a notification, when you choose
- **Send Later and Undo Send** — schedule an email, or take one back in the seconds after sending
- **Pin to Top of Inbox** — keep important emails at the top
- **Conversations** — the emails in a back-and-forth, shown together
- **Export as PDF** — an email or a whole conversation, then download it or attach it to a new email
- **Group by Type** — optional: the Inbox in sections — People, Notifications, Shopping, Social and Newsletters
- **Instant when you come back** — the emails you've seen are kept on your device, so the card opens straight away, then quietly fetches anything new

### Writing

- **Rich text** — bold, italic, underline, lists, quotes, emoji and stickers
- **Attachments** — photos, files and PDFs, up to 25 MB by default
- **Signatures** for each account
- **Voting buttons** — a poll in an email; replies are counted for you
- **Event invitations** — send one, or answer one with Accept, Maybe or Decline
- **Contact cards** — attach a contact from your address book
- **Read receipts** — ask for one, and answer them

### Inbox Tools

Each one is off until it's switched on in the editor:

- **Snooze** — put an email away until later. It waits in a Snoozed folder, then comes back to the top of the Inbox, unread, with a notification
- **Mute Conversation** — replies in a busy thread skip the Inbox and don't notify you
- **The Screener** — the first email from someone new waits in the Screener until you choose **Let In** or **Screen Out**. Contacts, VIPs and anyone you've emailed always get through
- **Subscriptions** — every mailing list in your Inbox, busiest first, with one-tap Unsubscribe where the sender supports it and **Unsubscribe All** for the ones you never read
- **Sweep** — delete or archive everything from one sender, keep only the latest, or delete ones over 10 days old
- **Custom Swipes** — each person chooses the buttons a swipe shows, and what a long swipe does
- **Today** — a panel at the top of the Mailboxes with parcels arriving, appointments, bills due, reminders, snoozed emails coming back and follow-ups
- **Keyboard shortcuts** — on a tablet or computer: `j`/`k` to move, `e` archive, `#` delete, `r` reply, `c` new email, `/` search, `?` for the full list

### Parcels and Dates

- **Track Parcel** — tracking numbers are found in delivery emails from couriers in the UK, Ireland, the US, Canada, Australia and New Zealand, with a link to the courier's own tracking page (no API keys)
- **Parcels** — a mailbox of deliveries on their way, with swipes, Rename, Share and Add to Calendar, an Arriving Today section, and a countdown before delivered parcels are tidied away
- **Add to Calendar** — tap a date in an email (optional, off by default) to add it to the calendar each person chooses, with the time, place and notes filled in

### Look and Feel

- **Classic or Liquid Glass** style, with **Automatic, Light or Dark** appearance and a Glass slider from clear to frosted
- **Skins** — each person can pick their own look: iPhone, Airmail, Gmail, Outlook, Spark, Superhuman, Proton Mail, or old-school Outlook Express, Hotmail 2000, You've Got Mail, Terminal, iPhone OS 3, BlackBerry and Mac OS 9
- **Backgrounds** — any photo, for one mailbox or all of them
- **Colour** — one accent colour, or each account's own
- **Full Screen** — a button at the top of the Mailboxes makes the card fill the whole screen. Tap it again, or press Escape, to put it back. Turn on **Open in Full Screen** and it fills the screen every time it opens

### Privacy and Safety

- **Images** — pictures from the web are hidden until you choose Show Images (or always shown for senders you trust), so senders can't tell when you've opened an email
- **Block Trackers** — the hidden pictures that report when you open an email are left out, even when images are shown
- **Hide My Location** — pictures can be fetched through Home Assistant, so senders never see your IP address
- **Block Ads** — ads from ad networks are taken out before the email reaches you, and optionally labelled sponsored sections are folded away
- **Report Spam, Block Sender and Report Phishing** — with Unsubscribe in the same step
- **Scam warnings** — emails pretending to be from someone else, or with links that go somewhere other than they say, are flagged
- **Private contacts** — each person's own address book, with VIPs

### AI Features

All optional, and each can be switched off individually in the editor:

- **Catch Up and Summaries** — a digest of unread email, and a summary of any email or whole conversation
- **Ask About This Email** — ask a question, like "When's the refund deadline?"
- **Smart Replies and Writing Tools** — suggested replies, proofreading, rewriting, or an email from a few words
- **Tone Check** — a gentle warning if an email might come across badly, with a kinder version
- **Translate** and **Describe Pictures**
- **Smart Search** — "the plumber's email about the boiler last month"
- **Find Dates and To-dos** — appointments and deadlines, ready for a calendar or to-do list
- **Smart Notifications** — only email worth a notification
- **Smart Categories** — Primary, Transactions, Updates and Promotions
- **Parcel Tracker** — deliveries found in email, with a Parcels sensor
- **Appointments** — bookings found in new email, with Add to Calendar
- **Bills** — amounts and due dates, a reminder a few days before, and a warning when a bill is much higher than last time
- **Morning Briefing** — a short summary of your day each morning, as a notification or read aloud on a speaker
- **Smart Snooze** — a suggested time from what's in the email, like the morning of a delivery
- **Screener Insights** — who each new sender seems to be, with a suggested Let In or Screen Out
- **Subscription Notes** — what each mailing list sends
- **Inbox Tidy-Up** — old promotions, unopened newsletters, sign-in codes and order confirmations to clear in one go
- **Contacts from Signatures** — add a sender's phone number or address to their contact
- **Follow-Up Nudges and Write the Follow-Up** — emails you sent that haven't had a reply, with a polite chaser drafted for you
- **AI Rules** — describe a rule in plain English, like "anything about my car insurance"
- **Email Details for Automations** — bills, amounts, deliveries and appointments in a `crow_email_details` event
- **Ask Your Email** — ask an Assist conversation agent about your email

### Integration

- **Phone notifications** — through the Companion app on iPhone and Android, with the sender, subject and preview, grouped by sender if you like
- **Notification buttons** — Reply, Mark as Read, Archive, Flag, Remind Me in 1 Hour and Delete (each can be switched on or off)
- **Quiet Hours** — new email arrives silently overnight; VIPs still come through
- **App icon badge** — optional and off by default: a red number on the Home Assistant app's icon showing unread email
- **Rules** — move, mark or flag new email, and choose whether it notifies you
- **Email Home Assistant** — optional and off by default: email yourself a subject starting `HA:`, like "HA: is the garage door closed?", and Assist answers by email
- **Sensors and binary sensors** for every account (below)
- **Actions and events** for your automations (below)
- Runs entirely on your own Home Assistant — no cloud service of its own

---

## Sensors

Each account is a device with these entities:

| Entity | Description |
|--------|-------------|
| Unread | Unread emails in the Inbox |
| Unread VIP | Unread emails from VIPs |
| Latest email | Who the newest email is from, and its subject |
| Received today | Emails received today |
| Flagged | Flagged emails |
| Drafts and scheduled | Drafts, plus emails waiting to Send Later |
| Mailbox usage | How full the mailbox is, where the provider says |
| Last checked | When the account was last checked |
| Junk | Emails in Junk (or Spam) |
| Parcels | Deliveries on their way (with the Parcel Tracker) |
| Needs attention today | Parcels arriving, appointments, bills due, reminders, snoozed emails and follow-ups |
| Bills due this week | Unpaid bills due in the next 7 days, with the total (with Bills) |
| Badge | The number on the app icon (with the App Icon Badge) |
| Connected | On while Home Assistant is signed in to the mail server |
| New mail | On when unread email has arrived since the Inbox was last looked at |

> Each account's **Show Sender and Subject** and **Show Preview Text** settings decide whether those details appear in its sensors and events, since anyone who can see your Home Assistant can see them.

---

## Actions and Events

### Actions

| Action | Description |
|--------|-------------|
| `crow_email.send_email` | Sends an email from one of the accounts. `account` is its email address or name; `to`, `cc` and `bcc` take addresses separated by commas. Optional `subject`, `message` (or `html`), `attachments` (files under `/local/`, your `www` folder, or `/media/local/`), `send_at`, `buttons`, `poll` and `read_receipt` |
| `crow_email.mark_as_read` | Marks an email (by `uid` or `message_id`), or `all` emails in a folder, as read or unread |
| `crow_email.archive` | Archives an email |
| `crow_email.move_to_folder` | Moves an email to another folder |
| `crow_email.flag` | Flags or unflags an email |
| `crow_email.refresh` | Checks one account, or all of them, for new email now |
| `crow_email.update_badge` | Updates the app icon badge, optionally adding a number of your own |

### Events

| Event | Description |
|-------|-------------|
| `crow_email_received` | A new email arrived, with the account, sender, subject, whether it's from a VIP and (if allowed) a preview |
| `crow_email_sent` | An email was sent |
| `crow_email_rule_matched` | One of your rules matched a new email |
| `crow_email_details` | What the AI found in a new email: its kind, amount, due date, appointment time, location and reference (with Email Details for Automations) |
| `crow_email_follow_up` | An email you sent may need a follow-up |
| `crow_email_parcel` | A parcel was added, changed status or was removed |
| `crow_email_blocked` | Email from a blocked sender was moved to Junk |
| `crow_email_action` | Someone tapped a button in an email sent by an automation |
| `crow_email_vote` | Someone voted on an email with voting buttons |

---

## Automation Examples

### Email a snapshot when the doorbell rings

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
      message: Here's who was there.
      attachments:
        - /local/snapshots/doorbell.jpg
```

### Buttons in an email

```yaml
actions:
  - action: crow_email.send_email
    data:
      account: me@icloud.com
      to: me@icloud.com
      subject: The garage door has been open for 30 minutes
      buttons:
        - title: Close the garage
          action: close_garage
```

```yaml
alias: Close the garage from an email
triggers:
  - trigger: event
    event_type: crow_email_action
    event_data:
      action: close_garage
actions:
  - action: cover.close_cover
    target:
      entity_id: cover.garage_door
```

### Flash a light when a VIP emails

```yaml
alias: VIP email light
triggers:
  - trigger: event
    event_type: crow_email_received
    event_data:
      vip: true
actions:
  - action: light.turn_on
    target:
      entity_id: light.hallway
    data:
      flash: short
```

---

## Quick Start

```yaml
type: custom:crow-email-card
card_height: 700
appearance: auto
style: glass
default_skin: iphone
start_mailbox: mailboxes
fullscreen_button: true
```

> **Note:** Everything can be set from the visual editor. Household settings (Microsoft sign-in, attachments, notifications, the badge and AI) are stored by the integration and set from the editor by an administrator. Each person's own choices — their accounts, skin, colour, images, ads, swipes and so on — are set in the card's **Settings**.

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `card_height` | `700` | Height in pixels |
| `appearance` | `auto` | `auto`, `light` or `dark` |
| `style` | `glass` | `glass` (Liquid Glass) or `classic` |
| `use_ha_theme` | `false` | Use your Home Assistant theme's background, text and accent colours |
| `default_skin` | `iphone` | The skin everyone starts with; each person can choose their own |
| `wide_layout` | `auto` | `auto` shows mailboxes, the list and the email side by side on a wide card; `off` shows one at a time |
| `start_mailbox` | `mailboxes` | Open to the `mailboxes` or straight to `all_inboxes` |
| `preview_lines` | `2` | Lines of each email shown in the list, `0` to `5` |
| `show_avatars` | `true` | Contact photos (or initials) next to each email |
| `inbox_groups` | `false` | The Inbox in sections: People, Notifications, Shopping, Social and Newsletters |
| `swipe_action` | `archive` | What a long swipe to the left does: `archive` or `trash` |
| `confirm_delete` | `false` | Ask before deleting |
| `confirm_archive` | `false` | Ask before archiving |
| `show_parcels_inbox` | `false` | A Parcels strip at the top of the Inbox |
| `track_site` | `17track` | Where to track a parcel when the courier has no tracking page of its own: `17track`, `parcelsapp` or `none` |
| `date_links` | `false` | Underline dates in emails; tap one to add it to a calendar |
| `animations` | `true` | Pages slide in and out like on an iPhone |
| `fullscreen_button` | `true` | The Full Screen button at the top of the Mailboxes |
| `resize_btn_spin` | `true` | The Full Screen button gives a quick spin each time it's tapped |
| `start_full` | `false` | Open in Full Screen each time the dashboard opens (needs the Full Screen button) |
| `snooze` | `false` | Snooze |
| `mute` | `false` | Mute Conversation |
| `screener` | `false` | The Screener (each person turns it on for themselves) |
| `subscriptions` | `false` | Subscriptions |
| `sweep` | `false` | Sweep |
| `custom_swipes` | `false` | Each person chooses their own swipes |
| `show_today` | `false` | Today at the top of the Mailboxes |

### Household Settings (in the editor, administrators only)

| Setting | Default | Description |
|---------|---------|-------------|
| Microsoft Application (Client) ID | *(empty)* | Needed to add Outlook accounts — see [Microsoft (Outlook) Setup](#microsoft-outlook-setup) |
| Largest Attachment | 25 MB | The biggest file anyone can attach |
| Remove Parcels After | 3 days | How long a delivered parcel stays in Parcels |
| App Icon Badge | Off | A red number on the Home Assistant app's icon |
| Notification Buttons | Reply, Mark as Read and Archive | Which buttons new-email notifications have |
| Email Home Assistant | Off | Email yourself `HA:` questions and Assist answers |
| AI Features | Off | Turns on the AI features for everyone |

---

## Troubleshooting

**The card doesn't appear in the card picker**
- Make sure the integration has been added under **Settings → Devices & Services** — the card is loaded by the integration.
- Hard-refresh your browser, or close and reopen the Home Assistant app on your iPhone.

**The card shows an old version after updating**
- Restart Home Assistant, then hard-refresh your browser or close and reopen the app. The version is at the bottom of the card's **Settings**.

**An account won't sign in**
- iCloud, Gmail and Yahoo need an **app password**, not your normal password — see [Adding Accounts](#adding-accounts).
- For Outlook, check the app registration has **Allow public client flows** on and both Exchange permissions — see [Microsoft (Outlook) Setup](#microsoft-outlook-setup).

**Notifications don't arrive**
- Check the person has the Home Assistant Companion app installed and signed in as their own user, and that their device is ticked in the account's notification settings.
- Check **Quiet Hours** isn't on.

**Images don't show**
- Images are hidden until you tap **Show Images**, unless you've chosen to always show them. Change this in the card's **Settings → Images**.

**AI features are missing**
- Check **AI Features** is switched on in the editor — AI is off by default, and its menu entries are hidden until it's on.
- Check an AI Task is set up in Home Assistant, or chosen in the editor.

**Getting back from full screen**
- Tap the Full Screen button at the top of the Mailboxes again, or press Escape on a keyboard. Leaving the dashboard view always puts the card back too.

---

## Credits & Acknowledgements

- The [Home Assistant](https://www.home-assistant.io) team
- All users who test, report issues and suggest improvements
- My Loving Wife for her endless support

---

## License

MIT License — free to use, modify and distribute.

---

## Support

If this is useful to you, please **star the repository** and share it with the community!

For bugs or feature requests, use the [GitHub Issues](../../issues) page.
