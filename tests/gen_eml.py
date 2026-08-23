"""
Generate 100 realistic .eml files for detector evaluation.
Named A01.eml – A100.eml, no test markers in headers or body.
Mix: ~50 phishing, ~50 legitimate, interleaved non-obviously.
"""

import os, textwrap
from datetime import datetime, timezone, timedelta

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eml")
os.makedirs(OUT, exist_ok=True)

def date_str(offset_days=0):
    dt = datetime(2026, 4, 10, 9, 0, 0, tzinfo=timezone.utc) + timedelta(days=offset_days, hours=offset_days % 7)
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

def msgid(n):
    return f"<msg{n:04d}.{n*31+7}@mailhost.internal>"

def eml(n, frm, to, subject, plain, html, date_offset=0):
    return f"""From: {frm}
To: {to}
Subject: {subject}
Date: {date_str(date_offset)}
Message-ID: {msgid(n)}
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="bound{n:04d}"

--bound{n:04d}
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

{textwrap.dedent(plain).strip()}

--bound{n:04d}
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: quoted-printable

{textwrap.dedent(html).strip()}

--bound{n:04d}--
"""

emails = []

# ── A01–A20 ───────────────────────────────────────────────────────────────────

emails.append(eml(1,
    "security-noreply@paypa1-accounts.com", "customer@gmail.com",
    "Your account has been limited",
    """
    Dear Customer,

    We noticed unusual activity on your account and have temporarily
    limited your access. To restore full access, please verify your
    information within 24 hours.

    Click here to verify: http://paypa1-accounts.com/verify?token=xK92mZ

    Failure to act may result in permanent account suspension.

    PayPal Security Team
    """,
    """<html><body><p>Dear Customer,</p><p>We noticed unusual activity on your account
    and have temporarily <b>limited your access</b>. To restore full access, please verify
    your information within 24 hours.</p>
    <p><a href="http://paypa1-accounts.com/verify?token=xK92mZ">Click here to verify</a></p>
    <p>Failure to act may result in permanent account suspension.</p>
    <p>PayPal Security Team</p></body></html>""", 0))

emails.append(eml(2,
    "j.morrison@acmecorp.com", "team@acmecorp.com",
    "Agenda for Thursday team sync",
    """
    Hi everyone,

    Here's the agenda for our Thursday 10am sync:
    1. Q2 roadmap review
    2. Sprint retrospective highlights
    3. Blockers and dependencies
    4. AOB

    Room: Conference B / Zoom fallback link in calendar invite.

    See you then,
    James
    """,
    """<html><body><p>Hi everyone,</p><ul><li>Q2 roadmap review</li>
    <li>Sprint retrospective highlights</li><li>Blockers and dependencies</li>
    <li>AOB</li></ul><p>Room: Conference B / Zoom fallback in calendar invite.</p>
    <p>James</p></body></html>""", 1))

emails.append(eml(3,
    "alerts@bankofamerica-secure.support", "client@hotmail.com",
    "Important: Suspicious login attempt detected",
    """
    Dear Valued Client,

    A login attempt from an unrecognized device was detected on your account.
    If this was not you, please secure your account immediately:

    http://bankofamerica-secure.support/lock?id=8821cc

    Your session will expire in 15 minutes.

    Online Banking Security
    """,
    """<html><body><p>Dear Valued Client,</p>
    <p>A login attempt from an <strong>unrecognized device</strong> was detected.</p>
    <p><a href="http://bankofamerica-secure.support/lock?id=8821cc">Secure your account now</a></p>
    <p>Your session expires in 15 minutes.</p></body></html>""", 2))

emails.append(eml(4,
    "notifications@github.com", "dev@company.com",
    "Pull request review requested: fix/auth-token-expiry",
    """
    Hi there,

    carlos_mendez requested your review on pull request #412:
    fix/auth-token-expiry in repository core-api.

    Changes: 3 files, +47 -12 lines
    View on GitHub: https://github.com/company/core-api/pull/412

    You are receiving this because you were mentioned.
    """,
    """<html><body><p>Hi there,</p><p><strong>carlos_mendez</strong> requested your review
    on pull request <a href="https://github.com/company/core-api/pull/412">#412: fix/auth-token-expiry</a>
    in <em>core-api</em>.</p><p>Changes: 3 files, +47 -12 lines</p></body></html>""", 3))

emails.append(eml(5,
    "billing-update@netf1ix-accounts.ru", "subscriber@yahoo.com",
    "Payment method declined — action required",
    """
    Hello,

    We were unable to process your last payment. To continue enjoying
    your subscription without interruption, please update your billing
    information immediately.

    Update now: http://netf1ix-accounts.ru/billing/update?u=7f3a

    This link expires in 12 hours.

    Billing Support Team
    """,
    """<html><body><p>Hello,</p><p>We were unable to process your last payment.</p>
    <p><a href="http://netf1ix-accounts.ru/billing/update?u=7f3a">Update your billing info</a></p>
    <p>This link expires in 12 hours.</p></body></html>""", 4))

emails.append(eml(6,
    "notifications@linkedin.com", "professional@outlook.com",
    "You have a new connection request",
    """
    Hi Sarah,

    Ana Gutierrez (Senior Product Designer at Fintech Corp) wants to
    connect with you on LinkedIn.

    View profile: https://www.linkedin.com/in/ana-gutierrez-design

    The LinkedIn Team
    """,
    """<html><body><p>Hi Sarah,</p><p><strong>Ana Gutierrez</strong> (Senior Product Designer
    at Fintech Corp) wants to connect with you on LinkedIn.</p>
    <p><a href="https://www.linkedin.com/in/ana-gutierrez-design">View profile</a></p></body></html>""", 5))

emails.append(eml(7,
    "refunds@irs-gov-refund.net", "taxpayer@gmail.com",
    "Tax refund notification — $1,842.00 pending",
    """
    Dear Taxpayer,

    Our records indicate you are eligible for a federal tax refund
    of $1,842.00. To process your refund we require identity confirmation.

    Claim your refund: http://irs-gov-refund.net/claim?ref=TXP2026

    Please provide your Social Security Number and bank details to
    complete the transfer.

    IRS Refund Processing Center
    """,
    """<html><body><p>Dear Taxpayer,</p>
    <p>You are eligible for a federal tax refund of <strong>$1,842.00</strong>.</p>
    <p><a href="http://irs-gov-refund.net/claim?ref=TXP2026">Claim your refund here</a></p>
    <p>Please provide your SSN and bank details to complete the transfer.</p></body></html>""", 6))

emails.append(eml(8,
    "shipment-update@amazon.com", "customer@gmail.com",
    "Your order has shipped",
    """
    Hello David,

    Good news! Your order #114-9283710-0042 has shipped and is on
    its way.

    Estimated delivery: April 17, 2026
    Carrier: UPS
    Tracking: 1Z999AA10123456784

    Track your package: https://www.amazon.com/gp/your-account/order-history

    Thank you for shopping with us.
    Amazon
    """,
    """<html><body><p>Hello David,</p><p>Your order <strong>#114-9283710-0042</strong>
    has shipped!</p><p>Estimated delivery: April 17, 2026 | Carrier: UPS</p>
    <p><a href="https://www.amazon.com/gp/your-account/order-history">Track your package</a></p>
    </body></html>""", 7))

emails.append(eml(9,
    "support@apple-id-verify.co", "iuser@icloud.com",
    "Your Apple ID has been locked",
    """
    Dear Apple Customer,

    Your Apple ID has been locked due to too many failed sign-in attempts.
    To unlock your account and protect your data, verify your identity now.

    Unlock account: http://apple-id-verify.co/unlock?session=A9x2

    If you do not verify within 48 hours your account will be permanently
    disabled.

    Apple Support
    """,
    """<html><body><p>Dear Apple Customer,</p>
    <p>Your Apple ID has been <strong>locked</strong> due to failed sign-in attempts.</p>
    <p><a href="http://apple-id-verify.co/unlock?session=A9x2">Unlock your account</a></p>
    <p>Verify within 48 hours to avoid permanent disabling.</p></body></html>""", 8))

emails.append(eml(10,
    "newsletter@thenewstack.io", "reader@gmail.com",
    "This week in cloud-native: eBPF, WASM, and AI inference at the edge",
    """
    Hi there,

    Here's your weekly digest from The New Stack:

    - eBPF observability tools hit production maturity
    - WebAssembly component model reaches 1.0
    - Running LLM inference on ARM edge nodes: a benchmark
    - Kubernetes 1.31 release notes summary

    Read more: https://thenewstack.io/newsletter/2026-04-14

    Unsubscribe at any time.
    """,
    """<html><body><p>Hi there,</p><ul>
    <li>eBPF observability tools hit production maturity</li>
    <li>WebAssembly component model reaches 1.0</li>
    <li>Running LLM inference on ARM edge nodes</li>
    <li>Kubernetes 1.31 release notes summary</li>
    </ul><p><a href="https://thenewstack.io/newsletter/2026-04-14">Read more</a></p></body></html>""", 9))

emails.append(eml(11,
    "it-helpdesk@microsoftonline-365.support", "employee@company.com",
    "Your password expires in 24 hours",
    """
    Dear User,

    Your Microsoft 365 password will expire in 24 hours. To avoid
    losing access to your email, Teams, and SharePoint, please
    reset your password immediately.

    Reset password: http://microsoftonline-365.support/reset?u=emp&t=9Kz3

    Do not share this link with anyone.

    IT Helpdesk
    """,
    """<html><body><p>Dear User,</p>
    <p>Your Microsoft 365 password expires in <strong>24 hours</strong>.</p>
    <p><a href="http://microsoftonline-365.support/reset?u=emp&t=9Kz3">Reset password now</a></p>
    </body></html>""", 10))

emails.append(eml(12,
    "noreply@zoom.us", "colleague@company.com",
    "Maria Lopez is inviting you to a scheduled Zoom meeting",
    """
    Hi,

    Maria Lopez is inviting you to a scheduled Zoom meeting.

    Topic: Q2 Budget Planning
    Time: Apr 18, 2026 02:00 PM Central Time
    Meeting ID: 812 4567 3901
    Passcode: xT7q9K

    Join: https://zoom.us/j/81245673901?pwd=xT7q9K

    Zoom Communications
    """,
    """<html><body><p><strong>Maria Lopez</strong> is inviting you to a Zoom meeting.</p>
    <p>Topic: Q2 Budget Planning<br>Time: Apr 18, 2026 2:00 PM CT</p>
    <p><a href="https://zoom.us/j/81245673901?pwd=xT7q9K">Join Zoom Meeting</a></p>
    </body></html>""", 11))

emails.append(eml(13,
    "delivery@dhl-parcel-support.com", "recipient@outlook.com",
    "Parcel on hold — customs fee required",
    """
    Dear Customer,

    Your DHL parcel (tracking: JD014600006281480070) is currently on
    hold at customs. A fee of $3.49 must be paid before we can release
    your shipment.

    Pay now: http://dhl-parcel-support.com/customs?ref=JD0146

    Failure to pay within 48 hours will result in return to sender.

    DHL Express Customer Service
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Your DHL parcel is on hold at customs. Pay a fee of <strong>$3.49</strong>
    to release it.</p>
    <p><a href="http://dhl-parcel-support.com/customs?ref=JD0146">Pay customs fee</a></p>
    </body></html>""", 12))

emails.append(eml(14,
    "notifications@slack.com", "user@company.com",
    "Carlos Mendez mentioned you in #engineering",
    """
    Hi,

    Carlos Mendez mentioned you in #engineering:

    "@sarah can you take a look at the failing CI pipeline?
    Seems related to the docker image update."

    Reply in Slack: https://app.slack.com/client/T01AB/C02XY

    Slack
    """,
    """<html><body><p><strong>Carlos Mendez</strong> mentioned you in #engineering:</p>
    <blockquote>"@sarah can you take a look at the failing CI pipeline?"</blockquote>
    <p><a href="https://app.slack.com/client/T01AB/C02XY">Reply in Slack</a></p></body></html>""", 13))

emails.append(eml(15,
    "drive-shares-noreply@googledrive-docs.info", "victim@gmail.com",
    "A document has been shared with you",
    """
    Hi,

    John Smith (jsmith.work91@gmail.com) has shared a document with you:

    \"Q1 Financial Report — CONFIDENTIAL\"

    View document: http://googledrive-docs.info/view?id=1BxTy9Zk&auth=open

    This document contains sensitive information. Please review and
    confirm receipt.

    Google Drive
    """,
    """<html><body><p>Hi,</p>
    <p><strong>John Smith</strong> shared a document with you:</p>
    <p><em>"Q1 Financial Report — CONFIDENTIAL"</em></p>
    <p><a href="http://googledrive-docs.info/view?id=1BxTy9Zk&auth=open">View document</a></p>
    </body></html>""", 14))

emails.append(eml(16,
    "statements@chase.com", "accountholder@gmail.com",
    "Your April statement is ready",
    """
    Hi Robert,

    Your Chase credit card statement for April 2026 is now available.

    Account ending: 4821
    Statement period: Mar 14 – Apr 13, 2026
    Balance due: $1,203.47
    Due date: May 8, 2026

    Sign in to chase.com to view your full statement.

    Chase Customer Service
    """,
    """<html><body><p>Hi Robert,</p><p>Your April 2026 statement is ready.</p>
    <table><tr><td>Account ending:</td><td>4821</td></tr>
    <tr><td>Balance due:</td><td>$1,203.47</td></tr>
    <tr><td>Due date:</td><td>May 8, 2026</td></tr></table>
    <p>Sign in to chase.com to view your statement.</p></body></html>""", 15))

emails.append(eml(17,
    "investment@crypto-profit-now.biz", "target@hotmail.com",
    "Exclusive opportunity: 400% returns in 30 days",
    """
    Hello,

    A limited group of investors made an average of 412% ROI last month
    using our proprietary AI trading algorithm.

    You have been selected for early access to our next cycle.

    Minimum investment: $500 USDT
    Expected return: $2,060 in 30 days — GUARANTEED

    Register now: http://crypto-profit-now.biz/join?ref=EARLY26

    Spots are limited. Act today.

    Profit-Now Investment Group
    """,
    """<html><body><p>Hello,</p>
    <p>Investors made an average of <strong>412% ROI</strong> last month.</p>
    <p>Minimum investment: $500 USDT — Expected return: $2,060 GUARANTEED</p>
    <p><a href="http://crypto-profit-now.biz/join?ref=EARLY26">Register now</a></p>
    </body></html>""", 16))

emails.append(eml(18,
    "hr@acmecorp.com", "employee@acmecorp.com",
    "Annual performance review — scheduling",
    """
    Hi Team,

    It's that time of year. Annual performance reviews will take place
    between April 28 and May 9, 2026.

    Please book a 45-minute slot with your manager using the link in
    your calendar invite. Self-assessment forms are due by April 25.

    Questions? Contact hr@acmecorp.com.

    HR Department
    """,
    """<html><body><p>Hi Team,</p>
    <p>Annual performance reviews: <strong>April 28 – May 9, 2026</strong>.</p>
    <ul><li>Book a 45-min slot with your manager</li>
    <li>Self-assessment due by April 25</li></ul>
    <p>Questions: hr@acmecorp.com</p></body></html>""", 17))

emails.append(eml(19,
    "ceo.michael.brennan.office@acmecorp-exec.com", "accountant@acmecorp.com",
    "Urgent wire transfer needed today",
    """
    Hi,

    I'm in back-to-back meetings and need you to process an urgent
    wire transfer before end of business today. This is time-sensitive
    and confidential — please do not discuss with other staff.

    Amount: $47,500 USD
    Beneficiary: Apex Consulting LLC
    Account: 8823-441-009 / Routing: 021000021

    I will explain the full context after the transfer is confirmed.
    Please action immediately and reply with confirmation.

    Michael Brennan
    CEO, Acme Corp
    """,
    """<html><body><p>Hi,</p>
    <p>Please process an urgent wire transfer today. <strong>Confidential.</strong></p>
    <p>Amount: $47,500 USD<br>Beneficiary: Apex Consulting LLC<br>
    Account: 8823-441-009 / Routing: 021000021</p>
    <p>Reply with confirmation immediately.</p>
    <p>Michael Brennan, CEO</p></body></html>""", 18))

emails.append(eml(20,
    "registrar@uth.edu.hn", "student@uth.edu.hn",
    "Course registration confirmation — Spring 2026",
    """
    Dear Student,

    Your course registration for Spring 2026 has been confirmed.

    Registered courses:
    - CIBR-401: Advanced Network Security (3 credits)
    - CIBR-450: Malware Analysis (3 credits)
    - MATH-310: Probability and Statistics (3 credits)

    Total credits: 9
    Registration ID: UTH-2026-03-18842

    For questions visit the registrar's office or email registrar@uth.edu.hn.

    Registrar's Office — UTH
    """,
    """<html><body><p>Dear Student,</p>
    <p>Your Spring 2026 registration is confirmed (ID: UTH-2026-03-18842).</p>
    <ul><li>CIBR-401: Advanced Network Security</li>
    <li>CIBR-450: Malware Analysis</li>
    <li>MATH-310: Probability and Statistics</li></ul>
    </body></html>""", 19))

# ── A21–A40 ───────────────────────────────────────────────────────────────────

emails.append(eml(21,
    "helpdesk@wellsfargo-alerts.info", "client@gmail.com",
    "Verification required — account access",
    """
    Dear Wells Fargo Customer,

    We have detected multiple failed login attempts on your account.
    As a precaution, your online access has been suspended.

    Please verify your identity to restore access:
    http://wellsfargo-alerts.info/verify?cid=WF2026a

    Wells Fargo Online Banking Security
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Your online access has been <strong>suspended</strong>.</p>
    <p><a href="http://wellsfargo-alerts.info/verify?cid=WF2026a">Verify identity</a></p>
    </body></html>""", 20))

emails.append(eml(22,
    "no-reply@atlassian.com", "dev@company.com",
    "Jira: Issue assigned to you — PROJ-1147",
    """
    Hi,

    An issue has been assigned to you in Jira:

    PROJ-1147: Fix rate-limiting bug on /api/analyze endpoint
    Priority: High
    Reporter: Carlos Mendez
    Due: Apr 22, 2026

    View issue: https://yourorg.atlassian.net/browse/PROJ-1147

    Atlassian
    """,
    """<html><body><p>Issue assigned to you in Jira:</p>
    <p><strong>PROJ-1147</strong>: Fix rate-limiting bug on /api/analyze endpoint</p>
    <p>Priority: High | Due: Apr 22, 2026</p>
    <p><a href="https://yourorg.atlassian.net/browse/PROJ-1147">View issue</a></p>
    </body></html>""", 21))

emails.append(eml(23,
    "security@dropbox-verify.net", "user@gmail.com",
    "New sign-in from unrecognized browser",
    """
    Hi,

    We noticed a sign-in to your Dropbox account from a new device.

    Device: Windows 11 / Chrome 123
    Location: Lagos, Nigeria
    Time: April 12, 2026, 03:14 AM UTC

    If this wasn't you, secure your account immediately:
    http://dropbox-verify.net/secure?token=DrBx9xA2

    Dropbox Security
    """,
    """<html><body><p>Hi,</p>
    <p>New sign-in detected from <strong>Lagos, Nigeria</strong>.</p>
    <p><a href="http://dropbox-verify.net/secure?token=DrBx9xA2">Secure your account</a></p>
    </body></html>""", 22))

emails.append(eml(24,
    "noreply@figma.com", "designer@company.com",
    "Maria shared a design file with you",
    """
    Hi,

    Maria Lopez shared a Figma file with you:
    "Mobile App Redesign v3 — Final"

    Open in Figma: https://www.figma.com/file/Kd92mNp8/Mobile-App-Redesign-v3

    Figma
    """,
    """<html><body><p>Hi,</p>
    <p><strong>Maria Lopez</strong> shared a Figma file with you:</p>
    <p><em>Mobile App Redesign v3 — Final</em></p>
    <p><a href="https://www.figma.com/file/Kd92mNp8/Mobile-App-Redesign-v3">Open in Figma</a></p>
    </body></html>""", 23))

emails.append(eml(25,
    "prize-notification@winner-clearinghouse.com", "lucky@yahoo.com",
    "Congratulations! You've been selected",
    """
    Dear Winner,

    You have been randomly selected from millions of participants to
    receive a prize of $85,000 USD in our 2026 Global Sweepstakes.

    To claim your prize, reply with:
    - Full name
    - Date of birth
    - Home address
    - Phone number

    A processing fee of $199 is required via Western Union.

    Claims Agent: Mrs. Patricia Howard
    Reply to: claims@winner-clearinghouse.com
    """,
    """<html><body><p>Dear Winner,</p>
    <p>You've been selected to receive <strong>$85,000 USD</strong>!</p>
    <p>Reply with your personal details. Processing fee: $199 via Western Union.</p>
    </body></html>""", 24))

emails.append(eml(26,
    "facilities@acmecorp.com", "staff@acmecorp.com",
    "Office HVAC maintenance — Floor 3 closure April 19",
    """
    Hi everyone,

    Facilities will be performing scheduled HVAC maintenance on Floor 3
    on Friday, April 19 from 8 AM to 1 PM. The floor will be inaccessible
    during that time.

    If your workstation is on Floor 3, please plan to work from home or
    use available hot-desks on Floor 2.

    Questions: facilities@acmecorp.com

    Facilities Team
    """,
    """<html><body><p>Hi everyone,</p>
    <p>HVAC maintenance on <strong>Floor 3 — April 19, 8 AM–1 PM</strong>.</p>
    <p>Floor 3 will be inaccessible. Use hot-desks on Floor 2 or WFH.</p>
    </body></html>""", 25))

emails.append(eml(27,
    "update@instagram-security-center.com", "instauser@gmail.com",
    "Your account will be disabled in 24 hours",
    """
    Hi,

    Your Instagram account has been flagged for violating our community
    guidelines. To prevent permanent disabling, you must complete a
    review within 24 hours.

    Complete review: http://instagram-security-center.com/appeal?id=IG2026x

    Ignoring this notice will result in permanent account removal.

    Instagram Safety Team
    """,
    """<html><body><p>Hi,</p>
    <p>Your account has been <strong>flagged</strong> and will be disabled in 24 hours.</p>
    <p><a href="http://instagram-security-center.com/appeal?id=IG2026x">Complete review</a></p>
    </body></html>""", 26))

emails.append(eml(28,
    "receipts@stripe.com", "owner@smallbiz.com",
    "Payment received — $2,340.00",
    """
    Hi,

    A payment of $2,340.00 has been successfully received.

    Customer: Globex Industries
    Invoice: INV-2026-0089
    Date: April 14, 2026
    Method: Visa ending 3842

    View in dashboard: https://dashboard.stripe.com/payments/

    Stripe
    """,
    """<html><body><p>Payment received: <strong>$2,340.00</strong></p>
    <p>Customer: Globex Industries | Invoice: INV-2026-0089</p>
    <p><a href="https://dashboard.stripe.com/payments/">View in dashboard</a></p>
    </body></html>""", 27))

emails.append(eml(29,
    "support@fedex-delivery-status.co", "customer@outlook.com",
    "Delivery failed — reschedule required",
    """
    Dear Customer,

    Our courier was unable to deliver your parcel today. To reschedule
    delivery you must confirm your address and pay a redelivery fee of $2.99.

    Reschedule: http://fedex-delivery-status.co/reschedule?id=FX9928X

    If not rescheduled within 48 hours the parcel will be returned.

    FedEx Delivery Services
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Delivery failed. Pay <strong>$2.99</strong> redelivery fee to reschedule.</p>
    <p><a href="http://fedex-delivery-status.co/reschedule?id=FX9928X">Reschedule now</a></p>
    </body></html>""", 28))

emails.append(eml(30,
    "professor.rodriguez@uth.edu.hn", "student@uth.edu.hn",
    "Midterm exam results posted",
    """
    Dear Students,

    Midterm exam scores for CIBR-401 have been posted to the student portal.

    Class average: 74.3 / 100
    Highest score: 97
    Lowest score: 41

    Please review your score and reach out during office hours
    (Tue/Thu 3–5 PM, Room 214) if you have questions.

    Dr. Rodriguez
    """,
    """<html><body><p>Dear Students,</p>
    <p>Midterm scores for CIBR-401 are posted.</p>
    <p>Average: 74.3 | Highest: 97 | Lowest: 41</p>
    <p>Office hours: Tue/Thu 3–5 PM, Room 214.</p></body></html>""", 29))

emails.append(eml(31,
    "noreply@coinbase-wallet-alert.com", "cryptouser@gmail.com",
    "Withdrawal request initiated — verify to proceed",
    """
    Hello,

    A withdrawal request of 1.42 BTC (~$87,300 USD) has been initiated
    from your Coinbase wallet.

    If you did not authorize this, cancel immediately:
    http://coinbase-wallet-alert.com/cancel?tx=CB29Zq1

    Failure to respond within 30 minutes will result in the transfer
    being completed.

    Coinbase Wallet Security
    """,
    """<html><body><p>Hello,</p>
    <p>Withdrawal of <strong>1.42 BTC (~$87,300)</strong> initiated.</p>
    <p><a href="http://coinbase-wallet-alert.com/cancel?tx=CB29Zq1">Cancel immediately</a></p>
    </body></html>""", 30))

emails.append(eml(32,
    "it@acmecorp.com", "staff@acmecorp.com",
    "Scheduled maintenance — VPN downtime April 20",
    """
    Hi Team,

    Our VPN infrastructure will undergo scheduled maintenance on
    Sunday, April 20, from 11 PM to 3 AM (CST).

    During this window remote access will be unavailable. Please
    ensure any critical tasks requiring VPN access are completed
    before 10:30 PM.

    IT Operations
    """,
    """<html><body><p>Hi Team,</p>
    <p>VPN maintenance: <strong>April 20, 11 PM – 3 AM CST</strong>.</p>
    <p>Remote access will be unavailable during this window.</p>
    </body></html>""", 31))

emails.append(eml(33,
    "security@steam-help-center.info", "gamer@gmail.com",
    "Your Steam account is at risk",
    """
    Dear Steam User,

    Someone attempted to access your Steam account from an unknown
    location. To protect your games and wallet balance, verify
    your identity now.

    Verify here: http://steam-help-center.info/verify?acct=SteamGrd9

    Your account will be locked if not verified in 1 hour.

    Steam Support
    """,
    """<html><body><p>Dear Steam User,</p>
    <p>Your account is at risk. Verify identity to protect it.</p>
    <p><a href="http://steam-help-center.info/verify?acct=SteamGrd9">Verify now</a></p>
    </body></html>""", 32))

emails.append(eml(34,
    "noreply@calendar.google.com", "professional@gmail.com",
    "Reminder: Dentist appointment tomorrow at 10 AM",
    """
    This is a reminder for an event in your Google Calendar.

    Event: Dentist Appointment
    When: April 16, 2026, 10:00 AM – 11:00 AM
    Where: Dr. Martinez Dental Clinic, 452 Oak Street

    View in Google Calendar: https://calendar.google.com/calendar/r

    Google Calendar
    """,
    """<html><body><p>Reminder from Google Calendar:</p>
    <p><strong>Dentist Appointment</strong><br>
    April 16, 2026, 10:00–11:00 AM<br>
    Dr. Martinez Dental Clinic, 452 Oak Street</p>
    <p><a href="https://calendar.google.com/calendar/r">View in Calendar</a></p>
    </body></html>""", 33))

emails.append(eml(35,
    "admin@sharepoint-document-portal.com", "employee@company.com",
    "Action required: Sign the updated NDA",
    """
    Dear Employee,

    HR requires all staff to sign the updated Non-Disclosure Agreement
    by April 30, 2026. Please access the document portal and complete
    your e-signature.

    Sign now: http://sharepoint-document-portal.com/sign?doc=NDA2026&emp=3821

    Your credentials from your company email apply.

    HR Compliance Team
    """,
    """<html><body><p>Dear Employee,</p>
    <p>Please sign the updated NDA by <strong>April 30, 2026</strong>.</p>
    <p><a href="http://sharepoint-document-portal.com/sign?doc=NDA2026&emp=3821">Sign now</a></p>
    </body></html>""", 34))

emails.append(eml(36,
    "orders@bestbuy.com", "shopper@outlook.com",
    "Your Best Buy order is ready for pickup",
    """
    Hi Sandra,

    Your order is ready for pickup at your selected store!

    Order: BBY-2026-447712
    Item: Sony WH-1000XM6 Headphones
    Store: Best Buy — 1200 Westfield Mall
    Ready until: April 20, 2026

    Bring this email or your order number to the customer service desk.

    Best Buy
    """,
    """<html><body><p>Hi Sandra,</p>
    <p>Your order <strong>BBY-2026-447712</strong> is ready for pickup.</p>
    <p>Item: Sony WH-1000XM6 Headphones<br>Store: Best Buy — 1200 Westfield Mall</p>
    </body></html>""", 35))

emails.append(eml(37,
    "tech-support@microsoft-helpdesk.info", "victim@outlook.com",
    "Critical security alert — your PC is infected",
    """
    CRITICAL SECURITY ALERT

    Our security systems have detected malware on your Windows computer.
    Your personal data, passwords, and banking information may be at risk.

    Call our certified technicians IMMEDIATELY:
    Toll-free: 1-888-555-0192

    Or click to start remote repair session:
    http://microsoft-helpdesk.info/remote?id=WIN2026sec

    Do not turn off your computer.

    Microsoft Security Response Center
    """,
    """<html><body style="background:red;color:white;">
    <h1>CRITICAL SECURITY ALERT</h1>
    <p>Malware detected on your PC. Call <strong>1-888-555-0192</strong> immediately.</p>
    <p><a href="http://microsoft-helpdesk.info/remote?id=WIN2026sec">Start remote repair</a></p>
    </body></html>""", 36))

emails.append(eml(38,
    "noreply@duolingo.com", "learner@gmail.com",
    "You're on a 30-day streak!",
    """
    Felicidades!

    You've kept your Duolingo streak alive for 30 days in a row!
    Keep practicing Spanish to reach the next milestone.

    Today's lesson is waiting: https://www.duolingo.com/lesson

    Duolingo
    """,
    """<html><body><p>You're on a <strong>30-day streak</strong>!</p>
    <p>Keep practicing Spanish on Duolingo.</p>
    <p><a href="https://www.duolingo.com/lesson">Today's lesson</a></p>
    </body></html>""", 37))

emails.append(eml(39,
    "refund-dept@amazon-returns-center.net", "shopper@yahoo.com",
    "Refund of $329.00 requires your confirmation",
    """
    Hello,

    A refund of $329.00 has been approved for your recent return.
    To process the refund to your original payment method, we need
    to confirm your account details.

    Confirm refund: http://amazon-returns-center.net/confirm?ref=AMZ3829

    If not confirmed within 24 hours the refund will be cancelled.

    Amazon Customer Service
    """,
    """<html><body><p>Hello,</p>
    <p>Your refund of <strong>$329.00</strong> requires confirmation.</p>
    <p><a href="http://amazon-returns-center.net/confirm?ref=AMZ3829">Confirm refund</a></p>
    </body></html>""", 38))

emails.append(eml(40,
    "newsletter@coursera.org", "learner@gmail.com",
    "New course recommendations based on your interests",
    """
    Hi,

    Based on your learning history, we think you'll love these courses:

    - Machine Learning Specialization (DeepLearning.AI)
    - Cloud Security Fundamentals (Google)
    - Applied Cryptography (Stanford)

    Explore: https://www.coursera.org/recommendations

    Happy learning!
    Coursera Team
    """,
    """<html><body><p>Hi,</p><p>New courses for you:</p>
    <ul><li>Machine Learning Specialization</li>
    <li>Cloud Security Fundamentals</li>
    <li>Applied Cryptography</li></ul>
    <p><a href="https://www.coursera.org/recommendations">Explore now</a></p>
    </body></html>""", 39))

# ── A41–A60 ───────────────────────────────────────────────────────────────────

emails.append(eml(41,
    "alert@usps-tracking-update.com", "recipient@gmail.com",
    "Package delivery attempt failed",
    """
    Dear Customer,

    USPS attempted delivery of your package (9400111899222870120) today.
    No one was available to receive it. To schedule redelivery or arrange
    pickup, a small handling fee of $1.99 is required.

    Schedule redelivery: http://usps-tracking-update.com/redeliver?id=9400U

    USPS Delivery Services
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Delivery attempt failed. Pay <strong>$1.99</strong> handling fee to redeliver.</p>
    <p><a href="http://usps-tracking-update.com/redeliver?id=9400U">Schedule redelivery</a></p>
    </body></html>""", 40))

emails.append(eml(42,
    "support@docusign.com", "legal@company.com",
    "Please DocuSign: Vendor Service Agreement",
    """
    [DocuSign] legal@company.com, please review and sign this document.

    Document: Vendor Service Agreement — Globex Industries
    Sent by: procurement@company.com
    Expires: April 25, 2026

    Review and sign: https://powerform.docusign.net/POWERFORM/v1/login?PF=abc123

    DocuSign — The Global Standard for eSignature
    """,
    """<html><body><p>Please review and sign:</p>
    <p><strong>Vendor Service Agreement — Globex Industries</strong></p>
    <p><a href="https://powerform.docusign.net/POWERFORM/v1/login?PF=abc123">Review & Sign</a></p>
    </body></html>""", 41))

emails.append(eml(43,
    "billing@paypal-invoice-center.com", "victim@gmail.com",
    "Invoice #INV-88123 — $599.00 has been charged",
    """
    Hi,

    An invoice for $599.00 has been processed from your PayPal account
    for a subscription to TechProtect Pro Annual Plan.

    If you did not authorize this charge, cancel it immediately:
    http://paypal-invoice-center.com/cancel?inv=88123

    You have 24 hours to dispute this transaction.

    PayPal Billing Department
    """,
    """<html><body><p>Hi,</p>
    <p>Invoice of <strong>$599.00</strong> charged for TechProtect Pro.</p>
    <p><a href="http://paypal-invoice-center.com/cancel?inv=88123">Cancel immediately</a></p>
    </body></html>""", 42))

emails.append(eml(44,
    "noreply@trello.com", "pm@company.com",
    "You have been added to the board: Product Launch Q3",
    """
    Hi,

    Ana Gutierrez added you to the Trello board:
    "Product Launch Q3 2026"

    View board: https://trello.com/b/Kx9mNp2/product-launch-q3-2026

    Trello
    """,
    """<html><body><p>Hi,</p>
    <p>You've been added to the Trello board <strong>Product Launch Q3 2026</strong>.</p>
    <p><a href="https://trello.com/b/Kx9mNp2/product-launch-q3-2026">View board</a></p>
    </body></html>""", 43))

emails.append(eml(45,
    "verify@meta-account-security.net", "fbuser@yahoo.com",
    "Unusual activity on your Facebook account",
    """
    Hi,

    We detected unusual activity on your Facebook account. Someone may
    have tried to access it from an unknown location.

    Secure your account: http://meta-account-security.net/secure?fb=9x2mZK

    If you don't act now, your account may be permanently restricted.

    Meta Security Team
    """,
    """<html><body><p>Hi,</p>
    <p>Unusual activity detected on your Facebook account.</p>
    <p><a href="http://meta-account-security.net/secure?fb=9x2mZK">Secure account now</a></p>
    </body></html>""", 44))

emails.append(eml(46,
    "payroll@acmecorp.com", "employee@acmecorp.com",
    "April payslip is available",
    """
    Dear Team Member,

    Your April 2026 payslip is now available in the HR portal.

    Pay date: April 30, 2026
    Access your payslip: https://hr.acmecorp.com/payslips

    If you have discrepancies, contact payroll@acmecorp.com by April 25.

    Payroll Department
    """,
    """<html><body><p>Dear Team Member,</p>
    <p>Your April 2026 payslip is available.</p>
    <p>Pay date: <strong>April 30, 2026</strong></p>
    <p><a href="https://hr.acmecorp.com/payslips">Access payslip</a></p>
    </body></html>""", 45))

emails.append(eml(47,
    "support@office365-email-quota.com", "worker@company.com",
    "Mailbox almost full — storage upgrade needed",
    """
    Dear User,

    Your Office 365 mailbox has reached 98% of its storage limit.
    Incoming emails will stop being delivered unless you act now.

    Upgrade storage: http://office365-email-quota.com/upgrade?user=worker3

    Log in with your company credentials to proceed.

    Microsoft Office 365 Team
    """,
    """<html><body><p>Dear User,</p>
    <p>Your mailbox is at <strong>98% capacity</strong>. Emails will stop delivering soon.</p>
    <p><a href="http://office365-email-quota.com/upgrade?user=worker3">Upgrade storage</a></p>
    </body></html>""", 46))

emails.append(eml(48,
    "noreply@notion.so", "teamlead@company.com",
    "Your weekly Notion digest",
    """
    Hi,

    Here's what happened in your Notion workspace this week:

    - 12 pages updated in "Engineering Wiki"
    - 3 new comments on "Q2 OKRs"
    - Sprint planning template was duplicated by Carlos

    Open Notion: https://notion.so

    Notion
    """,
    """<html><body><p>Your Notion digest:</p>
    <ul><li>12 pages updated in Engineering Wiki</li>
    <li>3 new comments on Q2 OKRs</li>
    <li>Sprint planning template duplicated</li></ul>
    <p><a href="https://notion.so">Open Notion</a></p>
    </body></html>""", 47))

emails.append(eml(49,
    "rewards@survey-cash-now.com", "target@hotmail.com",
    "Complete a short survey — earn $150 gift card",
    """
    Hi,

    You've been selected to complete a 2-minute survey for a chance
    to earn a $150 Visa gift card. No purchase necessary!

    Start survey: http://survey-cash-now.com/start?uid=SCN8821

    Hurry — only 8 spots remaining today!

    Survey Rewards Center
    """,
    """<html><body><p>Hi,</p>
    <p>Complete a 2-minute survey and earn a <strong>$150 Visa gift card</strong>!</p>
    <p><a href="http://survey-cash-now.com/start?uid=SCN8821">Start now</a></p>
    </body></html>""", 48))

emails.append(eml(50,
    "it-support@acmecorp.com", "employee@acmecorp.com",
    "New laptop setup instructions",
    """
    Hi,

    Your new laptop has been prepared and is ready for pickup from IT (Room 102).

    Before your first login, please complete these steps:
    1. Connect to the office Wi-Fi (SSID: AcmeCorp-Secure)
    2. Run Windows Update
    3. Install required software via the Software Center
    4. Enable BitLocker encryption (instructions in the IT wiki)

    IT Support — Acme Corp
    """,
    """<html><body><p>Hi,</p>
    <p>Your new laptop is ready for pickup at IT (Room 102).</p>
    <ol><li>Connect to AcmeCorp-Secure Wi-Fi</li>
    <li>Run Windows Update</li>
    <li>Install software via Software Center</li>
    <li>Enable BitLocker</li></ol>
    </body></html>""", 49))

emails.append(eml(51,
    "security@bankofamerica-service.info", "customer@gmail.com",
    "Your debit card has been temporarily blocked",
    """
    Dear Customer,

    For your protection, your Bank of America debit card ending in 4471
    has been temporarily blocked following a suspicious transaction.

    Unblock your card: http://bankofamerica-service.info/unblock?card=4471

    Please verify your identity within 2 hours to restore card access.

    Bank of America Fraud Prevention
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Your debit card ending in <strong>4471</strong> has been blocked.</p>
    <p><a href="http://bankofamerica-service.info/unblock?card=4471">Unblock card</a></p>
    </body></html>""", 50))

emails.append(eml(52,
    "no-reply@airbnb.com", "traveler@gmail.com",
    "Booking confirmed: Cozy Studio in Medellín",
    """
    Hi Roberto,

    Your booking is confirmed!

    Property: Cozy Studio near El Poblado
    Check-in: May 3, 2026
    Check-out: May 8, 2026
    Host: Isabella M.
    Confirmation: HMQK93AB

    View booking: https://www.airbnb.com/trips/

    Have a great trip!
    Airbnb
    """,
    """<html><body><p>Hi Roberto,</p>
    <p>Booking confirmed: <strong>Cozy Studio near El Poblado</strong></p>
    <p>May 3–8, 2026 | Confirmation: HMQK93AB</p>
    <p><a href="https://www.airbnb.com/trips/">View booking</a></p>
    </body></html>""", 51))

emails.append(eml(53,
    "claim@lottery-international-fund.com", "winner@outlook.com",
    "You have won €500,000 in the International E-Lottery",
    """
    CONGRATULATIONS!

    Your email address was selected as the winner of €500,000 in the
    2026 International E-Lottery promotional draw.

    To claim your winnings, contact our claims office:
    Email: claims@lottery-international-fund.com
    Reference: ELT-2026-WINNER-7729

    A processing fee of €350 is required to release the funds.

    International E-Lottery Foundation
    """,
    """<html><body><p>CONGRATULATIONS!</p>
    <p>You've won <strong>€500,000</strong> in the International E-Lottery!</p>
    <p>Processing fee: €350 to release funds.</p>
    </body></html>""", 52))

emails.append(eml(54,
    "do-not-reply@spotify.com", "listener@gmail.com",
    "Your Spotify Wrapped 2025 is here",
    """
    Hi,

    Your 2025 Spotify Wrapped is ready! Here's a sneak peek:

    Top artist: Bad Bunny
    Top song: "Luna Nueva"
    Minutes listened: 38,420
    Top genre: Latin Pop

    See your full Wrapped: https://open.spotify.com/wrapped

    Spotify
    """,
    """<html><body><p>Your Spotify Wrapped 2025:</p>
    <ul><li>Top Artist: Bad Bunny</li>
    <li>Top Song: "Luna Nueva"</li>
    <li>Minutes: 38,420</li></ul>
    <p><a href="https://open.spotify.com/wrapped">See full Wrapped</a></p>
    </body></html>""", 53))

emails.append(eml(55,
    "helpdesk@zoom-account-verify.com", "user@company.com",
    "Your Zoom Pro license will expire — renew now",
    """
    Dear Zoom User,

    Your Zoom Pro license expires in 3 days. To avoid service interruption,
    please renew your subscription immediately.

    Renew now: http://zoom-account-verify.com/renew?uid=ZM2026pr

    After expiry you will be downgraded to the free plan with 40-minute
    meeting limits.

    Zoom Accounts Team
    """,
    """<html><body><p>Dear Zoom User,</p>
    <p>Your Zoom Pro license expires in <strong>3 days</strong>.</p>
    <p><a href="http://zoom-account-verify.com/renew?uid=ZM2026pr">Renew now</a></p>
    </body></html>""", 54))

emails.append(eml(56,
    "updates@medium.com", "reader@gmail.com",
    "Stories we think you'll enjoy this week",
    """
    Hi,

    Based on your reading history, here are this week's top picks:

    - "The Hidden Cost of Microservices" by Jane Kim
    - "Why GraphQL Won" by Alex Rodriguez
    - "Burnout in Engineering Teams" by Dr. Priya Nair

    Read on Medium: https://medium.com/

    Medium Daily Digest
    """,
    """<html><body><p>This week's top picks on Medium:</p>
    <ul><li>"The Hidden Cost of Microservices"</li>
    <li>"Why GraphQL Won"</li>
    <li>"Burnout in Engineering Teams"</li></ul>
    <p><a href="https://medium.com/">Read now</a></p>
    </body></html>""", 55))

emails.append(eml(57,
    "no-reply@tax-refund-gov.info", "filer@yahoo.com",
    "IRS: Your 2025 refund is ready for deposit",
    """
    Dear Taxpayer,

    The IRS has processed your 2025 return and your refund of $2,211.00
    is ready. To deposit to your bank account, confirm your routing
    and account number.

    Confirm now: http://tax-refund-gov.info/deposit?ref=IRS2025X

    Refunds not claimed within 7 days are returned to the Treasury.

    Internal Revenue Service
    """,
    """<html><body><p>Dear Taxpayer,</p>
    <p>Your refund of <strong>$2,211.00</strong> is ready.</p>
    <p><a href="http://tax-refund-gov.info/deposit?ref=IRS2025X">Confirm bank details</a></p>
    </body></html>""", 56))

emails.append(eml(58,
    "noreply@eventbrite.com", "attendee@gmail.com",
    "Your ticket for PyCon Honduras 2026",
    """
    Hi Daniel,

    You're registered for PyCon Honduras 2026!

    Date: May 15–16, 2026
    Venue: Centro Cultural Sampedrano, San Pedro Sula
    Order: EB-2026-99123

    Your ticket is attached. Doors open at 8:00 AM.

    See you there!
    Eventbrite & PyCon Honduras
    """,
    """<html><body><p>Hi Daniel,</p>
    <p>You're registered for <strong>PyCon Honduras 2026</strong>.</p>
    <p>May 15–16 | Centro Cultural Sampedrano, San Pedro Sula</p>
    <p>Order: EB-2026-99123</p>
    </body></html>""", 57))

emails.append(eml(59,
    "admin@sharepoint-cloud-storage.net", "target@company.com",
    "Your OneDrive has been flagged for review",
    """
    Dear User,

    Your OneDrive account has been flagged for storing files that may
    violate Microsoft's Terms of Service. Your files will be deleted
    in 48 hours unless you complete an account review.

    Review account: http://sharepoint-cloud-storage.net/review?u=user3

    Microsoft OneDrive Compliance Team
    """,
    """<html><body><p>Dear User,</p>
    <p>Your OneDrive is flagged. Files will be <strong>deleted in 48 hours</strong>.</p>
    <p><a href="http://sharepoint-cloud-storage.net/review?u=user3">Review account</a></p>
    </body></html>""", 58))

emails.append(eml(60,
    "support@aws.amazon.com", "devops@company.com",
    "AWS Cost Explorer: Your bill is available",
    """
    Hello,

    Your AWS bill for March 2026 is now available.

    Total charges: $2,841.37
    Account: 112233445566
    Billing period: March 1–31, 2026

    View detailed breakdown: https://console.aws.amazon.com/billing/

    Amazon Web Services
    """,
    """<html><body><p>Your AWS bill for March 2026:</p>
    <p>Total: <strong>$2,841.37</strong> | Account: 112233445566</p>
    <p><a href="https://console.aws.amazon.com/billing/">View breakdown</a></p>
    </body></html>""", 59))

# ── A61–A80 ───────────────────────────────────────────────────────────────────

emails.append(eml(61,
    "noreply@whatsapp-verify-account.com", "user@gmail.com",
    "WhatsApp: Verify your phone number",
    """
    Hello,

    WhatsApp requires you to re-verify your phone number to continue
    using the service. Failure to verify will result in account deactivation.

    Verify here: http://whatsapp-verify-account.com/verify?num=+15551234567

    WhatsApp Support
    """,
    """<html><body><p>Hello,</p>
    <p>Re-verify your WhatsApp number or face <strong>account deactivation</strong>.</p>
    <p><a href="http://whatsapp-verify-account.com/verify?num=+15551234567">Verify now</a></p>
    </body></html>""", 60))

emails.append(eml(62,
    "library@uth.edu.hn", "student@uth.edu.hn",
    "Library books due for return — April 22",
    """
    Dear Library Member,

    The following items are due for return on April 22, 2026:

    1. "Computer Networks" — Tanenbaum (Loan ID: LIB-88123)
    2. "The Web Application Hacker's Handbook" (Loan ID: LIB-88124)

    Renew online: https://library.uth.edu.hn/renew

    Overdue fines: L.5 per day per item.

    UTH Library Services
    """,
    """<html><body><p>Dear Library Member,</p>
    <p>Books due <strong>April 22, 2026</strong>:</p>
    <ol><li>Computer Networks — Tanenbaum</li>
    <li>The Web Application Hacker's Handbook</li></ol>
    <p><a href="https://library.uth.edu.hn/renew">Renew online</a></p>
    </body></html>""", 61))

emails.append(eml(63,
    "security@twitter-account-suspend.com", "tweeter@yahoo.com",
    "Your X account has been suspended",
    """
    Hi,

    Your X (Twitter) account has been suspended for violating our
    rules. To appeal this decision and restore your account, complete
    the verification form.

    Appeal here: http://twitter-account-suspend.com/appeal?id=XSus2026

    X Trust & Safety Team
    """,
    """<html><body><p>Hi,</p>
    <p>Your X account has been <strong>suspended</strong>.</p>
    <p><a href="http://twitter-account-suspend.com/appeal?id=XSus2026">Appeal now</a></p>
    </body></html>""", 62))

emails.append(eml(64,
    "noreply@todoist.com", "productive@gmail.com",
    "You completed 47 tasks this week!",
    """
    Great job this week!

    You completed 47 tasks — your best week ever!

    Top project: Work (31 tasks)
    Karma points earned: 680
    Current streak: 12 days

    Keep going: https://todoist.com/app

    Todoist
    """,
    """<html><body><p>Great work this week!</p>
    <p>You completed <strong>47 tasks</strong> — your personal best!</p>
    <p>Karma earned: 680 | Streak: 12 days</p>
    <p><a href="https://todoist.com/app">Keep going</a></p>
    </body></html>""", 63))

emails.append(eml(65,
    "loans@quickcash-approvals.net", "target@hotmail.com",
    "Pre-approved: $10,000 personal loan — no credit check",
    """
    Congratulations!

    Based on your profile, you have been pre-approved for a personal
    loan of up to $10,000 with no credit check required.

    Interest rate: 2.9% monthly
    Terms: 12–36 months

    Claim your offer: http://quickcash-approvals.net/apply?uid=QCA2026

    Offer expires in 72 hours.

    QuickCash Financial Services
    """,
    """<html><body><p>You're pre-approved for <strong>$10,000</strong> — no credit check!</p>
    <p>Rate: 2.9% monthly</p>
    <p><a href="http://quickcash-approvals.net/apply?uid=QCA2026">Claim offer</a></p>
    </body></html>""", 64))

emails.append(eml(66,
    "receipts@uber.com", "rider@gmail.com",
    "Your Tuesday trip receipt",
    """
    Hi Carlos,

    Thanks for riding with Uber!

    Trip: Home → Airport
    Date: April 15, 2026, 6:42 AM
    Driver: Miguel R. ⭐ 4.93
    Distance: 18.4 km
    Total: $12.80 (charged to Visa 3921)

    Uber
    """,
    """<html><body><p>Hi Carlos,</p>
    <p>Your Uber receipt:</p>
    <p>Home → Airport | April 15, 2026<br>
    Total: <strong>$12.80</strong></p>
    </body></html>""", 65))

emails.append(eml(67,
    "verify@paypal-resolution-center.net", "seller@ebay.com",
    "Dispute opened against your account — respond now",
    """
    Dear Seller,

    A buyer has opened a dispute against your PayPal account for
    transaction #7K291830XA329847. Failure to respond in 7 days will
    result in automatic ruling against you.

    Respond to dispute: http://paypal-resolution-center.net/dispute?id=7K291830

    You must provide shipping proof and communications.

    PayPal Resolution Center
    """,
    """<html><body><p>Dear Seller,</p>
    <p>A dispute has been opened: <strong>#7K291830XA329847</strong>.</p>
    <p><a href="http://paypal-resolution-center.net/dispute?id=7K291830">Respond to dispute</a></p>
    </body></html>""", 66))

emails.append(eml(68,
    "admin@acmecorp.com", "newstaff@acmecorp.com",
    "Welcome to Acme Corp — your first day checklist",
    """
    Welcome aboard!

    We're thrilled to have you on the team. Here's what to do on
    your first day:

    1. Pick up your badge from Reception (Floor 1)
    2. Meet your buddy: James Morrison (james.morrison@acmecorp.com)
    3. Complete HR onboarding forms at https://hr.acmecorp.com/onboard
    4. IT will set up your laptop between 10–11 AM

    Looking forward to working with you!
    People Operations Team
    """,
    """<html><body><p>Welcome aboard!</p>
    <ol><li>Pick up badge at Reception (Floor 1)</li>
    <li>Meet your buddy: James Morrison</li>
    <li>Complete HR onboarding forms</li>
    <li>IT laptop setup 10–11 AM</li></ol>
    </body></html>""", 67))

emails.append(eml(69,
    "admin@adobe-subscription-alert.com", "designer@outlook.com",
    "Adobe Creative Cloud subscription paused",
    """
    Hi,

    Your Adobe Creative Cloud subscription has been paused due to a
    payment failure. To restore access to Photoshop, Illustrator, and
    other apps, please update your payment method.

    Update payment: http://adobe-subscription-alert.com/billing?uid=ADB2026x

    Your files and settings are safe but inaccessible until resolved.

    Adobe Customer Care
    """,
    """<html><body><p>Hi,</p>
    <p>Your Adobe CC subscription is <strong>paused</strong>.</p>
    <p><a href="http://adobe-subscription-alert.com/billing?uid=ADB2026x">Update payment method</a></p>
    </body></html>""", 68))

emails.append(eml(70,
    "no-reply@google.com", "workspace-user@company.com",
    "Security alert: New sign-in to your account",
    """
    Your Google Account was just signed in to from a new device.

    Device: MacBook Pro (macOS 15)
    Location: San Pedro Sula, Honduras
    Time: April 15, 2026, 8:32 AM

    If this was you, no action is needed.
    If not, secure your account: https://myaccount.google.com/security

    Google Account Team
    """,
    """<html><body><p>New sign-in to your Google Account:</p>
    <p>Device: MacBook Pro | San Pedro Sula | April 15, 2026</p>
    <p>Not you? <a href="https://myaccount.google.com/security">Secure your account</a></p>
    </body></html>""", 69))

emails.append(eml(71,
    "noreply@wellsfargo-securemail.info", "client@gmail.com",
    "Your online access has been locked",
    """
    Dear Wells Fargo Customer,

    Your online banking access has been locked after 3 consecutive
    failed sign-in attempts.

    Unlock your access: http://wellsfargo-securemail.info/unlock?cust=WF9921

    For security, this link is valid for 1 hour only.

    Wells Fargo Digital Banking
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Your online banking access is <strong>locked</strong>.</p>
    <p><a href="http://wellsfargo-securemail.info/unlock?cust=WF9921">Unlock now</a></p>
    </body></html>""", 70))

emails.append(eml(72,
    "newsletter@hbr.org", "executive@company.com",
    "HBR: Leading Through Uncertainty in 2026",
    """
    This week in Harvard Business Review:

    - "The AI Manager: Opportunity or Threat?"
    - "Why Quiet Quitting Returned in 2025"
    - "Resilience Strategies for Supply Chain Disruption"

    Read now: https://hbr.org/newsletter/2026-04

    Harvard Business Review
    """,
    """<html><body><p>This week on HBR:</p>
    <ul><li>"The AI Manager: Opportunity or Threat?"</li>
    <li>"Why Quiet Quitting Returned in 2025"</li>
    <li>"Resilience Strategies for Supply Chain Disruption"</li></ul>
    <p><a href="https://hbr.org/newsletter/2026-04">Read more</a></p>
    </body></html>""", 71))

emails.append(eml(73,
    "offers@amazon-prime-renewal.net", "member@gmail.com",
    "Your Amazon Prime membership is expiring soon",
    """
    Dear Prime Member,

    Your Amazon Prime membership expires in 3 days. To continue enjoying
    free delivery, Prime Video, and exclusive deals, renew now at a
    special rate of $9.99/month.

    Renew now: http://amazon-prime-renewal.net/renew?mbr=AMZ9921x

    Offer valid for existing members only.

    Amazon Prime Team
    """,
    """<html><body><p>Dear Prime Member,</p>
    <p>Your Prime membership expires in <strong>3 days</strong>.</p>
    <p><a href="http://amazon-prime-renewal.net/renew?mbr=AMZ9921x">Renew at $9.99/month</a></p>
    </body></html>""", 72))

emails.append(eml(74,
    "billing@digitalocean.com", "developer@company.com",
    "Invoice #DO-2026-03-8821 — $142.00",
    """
    Hi,

    Your DigitalOcean invoice for March 2026 is ready.

    Invoice: DO-2026-03-8821
    Amount: $142.00
    Due: April 30, 2026

    View invoice: https://cloud.digitalocean.com/account/billing

    DigitalOcean
    """,
    """<html><body><p>Hi,</p>
    <p>DigitalOcean invoice for March 2026: <strong>$142.00</strong></p>
    <p><a href="https://cloud.digitalocean.com/account/billing">View invoice</a></p>
    </body></html>""", 73))

emails.append(eml(75,
    "security@netflix-account-center.info", "subscriber@gmail.com",
    "Someone else is using your Netflix account",
    """
    Hi,

    We detected that your Netflix account is being accessed from
    an unfamiliar location. To protect your account, please verify
    your identity and change your password.

    Verify now: http://netflix-account-center.info/verify?acct=NF7x21

    If you recognize all active sessions, you can ignore this email.

    Netflix Account Security
    """,
    """<html><body><p>Hi,</p>
    <p>Unfamiliar access detected on your Netflix account.</p>
    <p><a href="http://netflix-account-center.info/verify?acct=NF7x21">Verify identity</a></p>
    </body></html>""", 74))

emails.append(eml(76,
    "alerts@pagerduty.com", "oncall@company.com",
    "[PagerDuty] CRITICAL: API response time > 5s",
    """
    CRITICAL alert triggered!

    Service: Production API Gateway
    Alert: Average response time exceeded 5000ms
    Triggered: April 15, 2026, 09:14 AM UTC
    Incident: INC-2026-04-8821

    Acknowledge: https://acmecorp.pagerduty.com/incidents/INC20260408821

    PagerDuty On-Call
    """,
    """<html><body style="background:#fff2f2">
    <p><strong>CRITICAL ALERT</strong></p>
    <p>Production API Gateway: response time &gt; 5s</p>
    <p>Incident: INC-2026-04-8821</p>
    <p><a href="https://acmecorp.pagerduty.com/incidents/INC20260408821">Acknowledge</a></p>
    </body></html>""", 75))

emails.append(eml(77,
    "promo@dating-elite-match.com", "user@hotmail.com",
    "Someone nearby likes your profile",
    """
    Hi,

    3 people near you have viewed your dating profile today.
    Upgrade to Premium to see who they are and message them for free.

    See who liked you: http://dating-elite-match.com/likes?uid=ELT9921

    Limited time: 50% off Premium for the next 24 hours.

    Elite Match
    """,
    """<html><body><p>Hi,</p>
    <p>3 people viewed your profile today!</p>
    <p><a href="http://dating-elite-match.com/likes?uid=ELT9921">See who liked you</a></p>
    <p>50% off Premium — 24 hours only.</p>
    </body></html>""", 76))

emails.append(eml(78,
    "manager@acmecorp.com", "employee@acmecorp.com",
    "Q1 team performance — well done",
    """
    Hi team,

    I wanted to take a moment to recognize the incredible work everyone
    put in during Q1. We shipped 3 major features ahead of schedule,
    reduced our bug backlog by 40%, and received our highest NPS from
    customers in company history.

    Let's celebrate at the team lunch on Friday (April 18, 12:30 PM).
    The company is picking up the tab.

    Thank you,
    James
    """,
    """<html><body><p>Hi team,</p>
    <p>Fantastic Q1! Highlights:</p>
    <ul><li>3 major features shipped early</li>
    <li>Bug backlog reduced 40%</li>
    <li>Highest-ever customer NPS</li></ul>
    <p>Team lunch Friday April 18, 12:30 PM. Company's treat.</p>
    </body></html>""", 77))

emails.append(eml(79,
    "support@apple-billing-update.com", "user@icloud.com",
    "Your Apple subscription payment failed",
    """
    Dear Apple Customer,

    We were unable to process your payment for iCloud+ 2TB storage.
    To avoid losing access to your photos and backups, update your
    payment method immediately.

    Update now: http://apple-billing-update.com/payment?uid=APL2026b

    Apple Billing Support
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Your iCloud+ payment <strong>failed</strong>.</p>
    <p><a href="http://apple-billing-update.com/payment?uid=APL2026b">Update payment method</a></p>
    </body></html>""", 78))

emails.append(eml(80,
    "support@github.com", "developer@company.com",
    "GitHub Actions: Workflow run failed — main branch",
    """
    Hi,

    A GitHub Actions workflow run failed:

    Repository: company/core-api
    Workflow: CI/CD Pipeline
    Branch: main
    Commit: a9f3c21 ("Merge PR #412: fix/auth-token-expiry")
    Error: Test suite failed — 2 tests failed

    View run: https://github.com/company/core-api/actions/runs/88219123

    GitHub Actions
    """,
    """<html><body><p>GitHub Actions workflow failed:</p>
    <p>Repo: company/core-api | Branch: main<br>
    Commit: a9f3c21</p>
    <p><a href="https://github.com/company/core-api/actions/runs/88219123">View run details</a></p>
    </body></html>""", 79))

# ── A81–A100 ──────────────────────────────────────────────────────────────────

emails.append(eml(81,
    "helpdesk@citibank-secure-login.com", "client@yahoo.com",
    "Citibank: Confirm your recent card transaction",
    """
    Dear Cardholder,

    A transaction of $1,299.00 was made on your Citibank card ending
    in 6632 at "Global Electronics Online" on April 14, 2026.

    If you did not make this purchase, please dispute it immediately:
    http://citibank-secure-login.com/dispute?tx=CIT2026x

    Citibank Fraud Prevention
    """,
    """<html><body><p>Dear Cardholder,</p>
    <p>Transaction of <strong>$1,299.00</strong> at Global Electronics Online.</p>
    <p><a href="http://citibank-secure-login.com/dispute?tx=CIT2026x">Dispute transaction</a></p>
    </body></html>""", 80))

emails.append(eml(82,
    "no-reply@heroku.com", "developer@company.com",
    "Deploy successful: core-api v2.4.1",
    """
    Hi,

    Your Heroku app deploy was successful.

    App: core-api-prod
    Version: v2.4.1
    Build: #182
    Duration: 3m 22s
    Released: April 15, 2026, 09:02 AM UTC

    Dashboard: https://dashboard.heroku.com/apps/core-api-prod

    Heroku
    """,
    """<html><body><p>Deploy successful!</p>
    <p>App: core-api-prod | Version: v2.4.1 | Build #182</p>
    <p><a href="https://dashboard.heroku.com/apps/core-api-prod">View dashboard</a></p>
    </body></html>""", 81))

emails.append(eml(83,
    "jobs@linkedin-career-alerts.net", "jobseeker@gmail.com",
    "Your profile was viewed by a recruiter at Google",
    """
    Hi,

    Your LinkedIn profile was viewed by a recruiter from Google today.
    Upgrade to LinkedIn Premium to message them directly and see who
    else viewed your profile.

    Upgrade now: http://linkedin-career-alerts.net/premium?ref=RCRT2026

    LinkedIn Jobs
    """,
    """<html><body><p>Hi,</p>
    <p>A Google recruiter viewed your profile!</p>
    <p><a href="http://linkedin-career-alerts.net/premium?ref=RCRT2026">Upgrade to Premium</a></p>
    </body></html>""", 82))

emails.append(eml(84,
    "advisor@acmecorp.com", "client@company.com",
    "Meeting notes from April 14 — follow-up items",
    """
    Hi,

    Thank you for the productive session yesterday. Here are the
    agreed follow-up items:

    1. Review the updated proposal by April 18 (your team)
    2. Sign NDA before the next call (your legal team)
    3. Schedule technical deep-dive for April 25 (both teams)

    Please confirm these items at your earliest convenience.

    Best regards,
    Luis Advisor
    """,
    """<html><body><p>Hi,</p>
    <p>Follow-up items from April 14:</p>
    <ol><li>Review updated proposal by April 18</li>
    <li>Sign NDA before next call</li>
    <li>Technical deep-dive April 25</li></ol>
    </body></html>""", 83))

emails.append(eml(85,
    "noreply@binance-security.info", "cryptotrader@gmail.com",
    "Withdrawal of 0.85 ETH requested — confirm or cancel",
    """
    Dear Binance User,

    A withdrawal request of 0.85 ETH (~$2,890 USD) has been submitted
    from your wallet to an external address.

    If you did NOT request this withdrawal, cancel it immediately:
    http://binance-security.info/cancel?tx=BNB2026eth

    This request will be processed in 30 minutes if not cancelled.

    Binance Security Team
    """,
    """<html><body><p>Dear User,</p>
    <p>Withdrawal of <strong>0.85 ETH (~$2,890)</strong> requested.</p>
    <p><a href="http://binance-security.info/cancel?tx=BNB2026eth">Cancel immediately</a></p>
    </body></html>""", 84))

emails.append(eml(86,
    "ops@acmecorp.com", "engineering@acmecorp.com",
    "Post-mortem: API outage April 13 — final report",
    """
    Hi team,

    The post-mortem for the April 13 API outage is finalized.

    Root cause: Memory leak in the connection pool under high load
    Duration: 47 minutes (02:18–03:05 AM UTC)
    Impact: ~12% of API requests failed; no data loss

    Action items:
    - Increase memory limits (done — PR #419)
    - Add pool exhaustion alert (owner: Ana, due Apr 20)
    - Load test in staging weekly (owner: DevOps, due Apr 25)

    Full report: https://wiki.acmecorp.com/postmortems/2026-04-13

    Ops Team
    """,
    """<html><body><p>Post-mortem: API outage April 13</p>
    <p>Root cause: Memory leak | Duration: 47 min | ~12% requests failed</p>
    <p>Action items assigned. <a href="https://wiki.acmecorp.com/postmortems/2026-04-13">Full report</a></p>
    </body></html>""", 85))

emails.append(eml(87,
    "promo@walmart-gift-card.com", "shopper@hotmail.com",
    "Claim your $500 Walmart gift card today",
    """
    Congratulations!

    You have been selected to receive a $500 Walmart gift card as part
    of our customer appreciation program.

    Claim your gift card: http://walmart-gift-card.com/claim?uid=WMT2026

    Complete a short 3-question survey to unlock your reward.
    Only 5 cards remaining!

    Walmart Customer Rewards
    """,
    """<html><body><p>Congratulations!</p>
    <p>You've won a <strong>$500 Walmart gift card</strong>!</p>
    <p><a href="http://walmart-gift-card.com/claim?uid=WMT2026">Claim now</a></p>
    <p>Only 5 remaining!</p>
    </body></html>""", 86))

emails.append(eml(88,
    "accounts@acmecorp.com", "vendor@supplier.com",
    "Payment processed — Invoice INV-2026-0092",
    """
    Dear Supplier,

    We have processed payment for Invoice INV-2026-0092.

    Amount: $8,750.00 USD
    Payment method: Bank Transfer
    Reference: ACM-PAY-2026-0092
    Expected arrival: 2–3 business days

    Please confirm receipt. Contact accounts@acmecorp.com with questions.

    Accounts Payable — Acme Corp
    """,
    """<html><body><p>Dear Supplier,</p>
    <p>Payment processed for Invoice INV-2026-0092: <strong>$8,750.00</strong></p>
    <p>Reference: ACM-PAY-2026-0092 | ETA: 2–3 business days</p>
    </body></html>""", 87))

emails.append(eml(89,
    "support@paypal-help-dispute.com", "buyer@gmail.com",
    "Your PayPal case #PP-2026-CR-8821 update",
    """
    Dear Customer,

    Your PayPal case #PP-2026-CR-8821 requires additional information
    before we can process your refund of $214.99.

    Provide information: http://paypal-help-dispute.com/case?id=PP2026CR8821

    Without this information your case will be closed in 3 days.

    PayPal Resolution Center
    """,
    """<html><body><p>Dear Customer,</p>
    <p>Case #PP-2026-CR-8821 requires additional info for your <strong>$214.99 refund</strong>.</p>
    <p><a href="http://paypal-help-dispute.com/case?id=PP2026CR8821">Provide information</a></p>
    </body></html>""", 88))

emails.append(eml(90,
    "do-not-reply@notion.so", "manager@company.com",
    "Your Notion workspace has 3 pending comments",
    """
    Hi,

    You have 3 unread comments in your Notion workspace:

    - Carlos commented on "Q2 Roadmap": "Should we push this to Q3?"
    - Ana replied on "API Design Doc": "Approved — looks good"
    - Maria added a comment to "Sprint 18 Retro"

    View comments: https://notion.so/inbox

    Notion
    """,
    """<html><body><p>You have 3 unread comments in Notion:</p>
    <ul><li>Carlos: "Should we push this to Q3?"</li>
    <li>Ana: "Approved — looks good"</li>
    <li>Maria: new comment on Sprint 18 Retro</li></ul>
    <p><a href="https://notion.so/inbox">View all</a></p>
    </body></html>""", 89))

emails.append(eml(91,
    "helpdesk@googlepay-verify.net", "user@gmail.com",
    "Google Pay: Unusual payment activity detected",
    """
    Dear Google Pay User,

    We detected a payment of $340.00 from your Google Pay account to
    an unrecognized merchant. For your security, we have temporarily
    held this transaction.

    Review and authorize: http://googlepay-verify.net/review?tx=GP2026x

    If you recognize this payment, confirm it. Otherwise, dispute it.

    Google Pay Security
    """,
    """<html><body><p>Dear Google Pay User,</p>
    <p>Unusual payment of <strong>$340.00</strong> held for review.</p>
    <p><a href="http://googlepay-verify.net/review?tx=GP2026x">Review transaction</a></p>
    </body></html>""", 90))

emails.append(eml(92,
    "newsletter@producthunt.com", "maker@gmail.com",
    "Top products this week on Product Hunt",
    """
    Hi,

    Here's what launched this week:

    #1 - Raycast AI Pro — AI command palette for macOS
    #2 - Supabase Vector — Postgres for AI apps
    #3 - Loom 3.0 — Async video with AI summaries

    See all: https://www.producthunt.com/

    Product Hunt
    """,
    """<html><body><p>Top launches this week:</p>
    <ol><li>Raycast AI Pro</li><li>Supabase Vector</li><li>Loom 3.0</li></ol>
    <p><a href="https://www.producthunt.com/">See all products</a></p>
    </body></html>""", 91))

emails.append(eml(93,
    "verify@chase-banking-secure.com", "client@yahoo.com",
    "Chase: Identity verification required",
    """
    Dear Valued Client,

    As part of our ongoing security procedures, we are required to
    verify the identity of all account holders. Please complete
    verification within 48 hours.

    Verify identity: http://chase-banking-secure.com/idv?cust=CHZ8821

    Failure to verify may result in restricted account access.

    Chase Security Operations
    """,
    """<html><body><p>Dear Client,</p>
    <p>Identity verification required within <strong>48 hours</strong>.</p>
    <p><a href="http://chase-banking-secure.com/idv?cust=CHZ8821">Verify now</a></p>
    </body></html>""", 92))

emails.append(eml(94,
    "noreply@grammarly.com", "writer@company.com",
    "Your Grammarly weekly writing stats",
    """
    Hi,

    Here's your Grammarly writing summary for this week:

    Words checked: 14,320
    Correctness issues fixed: 47
    Clarity suggestions accepted: 23
    Tone: Confident (most common)

    Keep writing: https://app.grammarly.com/

    Grammarly
    """,
    """<html><body><p>Your Grammarly stats this week:</p>
    <ul><li>Words checked: 14,320</li>
    <li>Issues fixed: 47</li>
    <li>Clarity accepted: 23</li></ul>
    <p><a href="https://app.grammarly.com/">Keep writing</a></p>
    </body></html>""", 93))

emails.append(eml(95,
    "alert@microsoft-account-secure.info", "user@outlook.com",
    "We blocked a sign-in attempt to your account",
    """
    Dear User,

    A sign-in attempt to your Microsoft account was blocked because
    it appeared suspicious.

    Location: Kyiv, Ukraine
    Device: Unknown Android device
    Time: April 15, 2026, 04:33 AM

    If this was you, verify here:
    http://microsoft-account-secure.info/verify?uid=MS2026x

    Microsoft Account Security
    """,
    """<html><body><p>Dear User,</p>
    <p>Suspicious sign-in blocked from <strong>Kyiv, Ukraine</strong>.</p>
    <p><a href="http://microsoft-account-secure.info/verify?uid=MS2026x">Review activity</a></p>
    </body></html>""", 94))

emails.append(eml(96,
    "invoices@freshbooks.com", "freelancer@gmail.com",
    "Invoice #2026-047 viewed by your client",
    """
    Hi,

    Great news! Your client Globex Industries viewed Invoice #2026-047
    ($3,200.00) today.

    Track payments: https://my.freshbooks.com/#/invoices

    FreshBooks
    """,
    """<html><body><p>Hi,</p>
    <p>Client viewed Invoice #2026-047 — <strong>$3,200.00</strong></p>
    <p><a href="https://my.freshbooks.com/#/invoices">Track payments</a></p>
    </body></html>""", 95))

emails.append(eml(97,
    "promo@pharma-discount-meds.com", "patient@hotmail.com",
    "Prescription medications — no prescription needed, 80% off",
    """
    Hi,

    Get your prescription medications delivered discreetly with no
    doctor's visit required. We carry Viagra, Xanax, Adderall and more.

    Shop now: http://pharma-discount-meds.com/catalog?promo=NOSCRIPT80

    80% off your first order. Ships in plain packaging.

    Online Pharmacy Group
    """,
    """<html><body><p>Hi,</p>
    <p>Prescription meds — <strong>no prescription needed</strong>. 80% off!</p>
    <p><a href="http://pharma-discount-meds.com/catalog?promo=NOSCRIPT80">Shop now</a></p>
    </body></html>""", 96))

emails.append(eml(98,
    "security@acmecorp.com", "staff@acmecorp.com",
    "Mandatory security awareness training — due April 30",
    """
    Dear Team Member,

    As part of our annual compliance program, all staff are required
    to complete the 2026 Security Awareness Training module by April 30.

    The training takes approximately 45 minutes and covers:
    - Phishing recognition
    - Password hygiene
    - Data handling procedures

    Access training: https://training.acmecorp.com/security2026

    Security & Compliance Team
    """,
    """<html><body><p>Dear Team Member,</p>
    <p>Complete <strong>Security Awareness Training</strong> by April 30, 2026.</p>
    <ul><li>Phishing recognition</li><li>Password hygiene</li><li>Data handling</li></ul>
    <p><a href="https://training.acmecorp.com/security2026">Access training</a></p>
    </body></html>""", 97))

emails.append(eml(99,
    "verify@paypal-account-limit.com", "user@gmail.com",
    "Your PayPal sending limit has been reached",
    """
    Dear PayPal User,

    You have reached your monthly sending limit of $2,000. To lift
    this restriction and continue sending payments, please verify
    your identity and link a bank account.

    Lift restriction: http://paypal-account-limit.com/lift?uid=PPL2026x

    PayPal Compliance Team
    """,
    """<html><body><p>Dear PayPal User,</p>
    <p>Monthly sending limit of <strong>$2,000</strong> reached.</p>
    <p><a href="http://paypal-account-limit.com/lift?uid=PPL2026x">Lift restriction</a></p>
    </body></html>""", 98))

emails.append(eml(100,
    "no-reply@uth.edu.hn", "graduate@uth.edu.hn",
    "Graduation ceremony — confirmation and logistics",
    """
    Dear Graduate,

    Congratulations! You are confirmed to participate in the
    UTH Class of 2026 Graduation Ceremony.

    Date: June 7, 2026, 10:00 AM
    Venue: Polideportivo UTH, San Pedro Sula
    Attire: Academic gown (available for collection at the registrar from May 20)
    Guest tickets: 2 per graduate (pick up at reception with student ID)

    Please confirm attendance by May 1 at:
    https://registrar.uth.edu.hn/graduation/confirm?id=UTH2026GRAD

    Congratulations and see you on the big day!
    UTH Academic Office
    """,
    """<html><body><p>Dear Graduate,</p>
    <p>You are confirmed for <strong>UTH Class of 2026 Graduation</strong>!</p>
    <p>June 7, 2026 | Polideportivo UTH, San Pedro Sula</p>
    <p>Confirm attendance by May 1:
    <a href="https://registrar.uth.edu.hn/graduation/confirm?id=UTH2026GRAD">Confirm here</a></p>
    </body></html>""", 99))

# ── Write all files ────────────────────────────────────────────────────────────
for i, content in enumerate(emails, start=1):
    path = os.path.join(OUT, f"A{i:02d}.eml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Written {len(emails)} .eml files to: {OUT}")
