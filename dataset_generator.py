import json
import random
import uuid

# Categories required
CATEGORIES = [
    "Delivery Delay", "Refund Request", "Return Request", "Damaged Product", "Wrong Product",
    "Password Reset", "Login Issue", "Payment Failure", "Subscription Cancellation", "Billing Problem",
    "Feature Request", "Account Deletion", "General Inquiry", "Shipping Address Change", "Order Status",
    "Coupon Problem", "Gift Card Issue", "Late Refund", "Duplicate Payment", "Technical Issue"
]

# Random components
CUSTOMERS = ["Rahul Sharma", "Priya Singh", "Amit Patel", "Neha Gupta", "Vikram Reddy", "Anjali Desai", "Karan Malhotra", "Riya Mehta", "Sanjay Kumar", "Sneha Joshi"]
PRODUCTS = ["Laptop", "Smartphone", "Wireless Headphones", "Smartwatch", "Mechanical Keyboard", "Monitor", "Gaming Mouse", "Tablet", "External SSD", "Router"]
ORDER_PREFIX = ["ORD", "INV", "TRX", "HVR"]

# Templates for each category
TEMPLATES = {
    "Delivery Delay": [
        ("Hello, I ordered a {product} (Order ID: {order_id}) on Monday, but it hasn't arrived yet. The tracking hasn't updated in 3 days. What's going on?", "Negative", "High", ["delivery", "delay", "order", "tracking"]),
        ("Hi team, my {product} was supposed to be delivered yesterday. Can you check the status of {order_id}? Thanks.", "Neutral", "Medium", ["delivery", "status", "order"]),
        ("I am extremely frustrated. My {order_id} containing the {product} is delayed by a week! Please resolve this immediately.", "Negative", "High", ["frustrated", "delay", "resolve"]),
        ("Hey, just checking on {order_id}. The {product} seems to be stuck in transit.", "Neutral", "Low", ["checking", "transit", "stuck"]),
        ("My order {order_id} for a {product} is late. I need this for work urgently. Please expedite.", "Negative", "High", ["late", "urgently", "expedite"])
    ],
    "Refund Request": [
        ("I would like to request a refund for {order_id}. The {product} did not meet my expectations.", "Neutral", "Medium", ["refund", "expectations", "order"]),
        ("Please process a refund for my recent purchase of {product}. Order number is {order_id}.", "Neutral", "Medium", ["process", "refund", "purchase"]),
        ("I'm very disappointed with the {product}. I demand a full refund for {order_id} immediately.", "Negative", "High", ["disappointed", "demand", "refund"]),
        ("Hi, I returned my {product} but haven't received my refund for {order_id} yet.", "Negative", "High", ["returned", "refund", "received"]),
        ("Can you help me get a refund for {order_id}? The {product} isn't what I wanted.", "Neutral", "Low", ["help", "refund", "wanted"])
    ],
    "Return Request": [
        ("I need to return the {product} I bought (Order {order_id}). How do I get a return label?", "Neutral", "Medium", ["return", "label", "order"]),
        ("The {product} is too small. I want to return {order_id}. Please advise.", "Neutral", "Medium", ["return", "small", "advise"]),
        ("I am returning order {order_id} because the {product} is not as described. Send instructions.", "Negative", "Medium", ["returning", "described", "instructions"]),
        ("Hi, what is your return policy for {product}? My order number is {order_id}.", "Neutral", "Low", ["policy", "return", "order"]),
        ("Please initiate a return for my {product} under order {order_id}.", "Neutral", "Medium", ["initiate", "return"])
    ],
    "Damaged Product": [
        ("My {product} arrived completely shattered! Order {order_id}. This is unacceptable.", "Negative", "High", ["shattered", "damaged", "unacceptable"]),
        ("Hi, I opened order {order_id} and the {product} has a huge scratch on it.", "Negative", "Medium", ["scratch", "damaged", "opened"]),
        ("The packaging was fine but the {product} inside (Order {order_id}) is broken.", "Negative", "High", ["broken", "packaging", "damaged"]),
        ("I received my {product} today (Order {order_id}) and it's damaged. How can we fix this?", "Neutral", "Medium", ["received", "damaged", "fix"]),
        ("Terrible experience. The {product} for {order_id} is completely unusable due to damage.", "Negative", "High", ["terrible", "unusable", "damage"])
    ],
    "Wrong Product": [
        ("I ordered a {product} but received something entirely different. Order {order_id}.", "Negative", "High", ["ordered", "received", "wrong", "different"]),
        ("This is not what I ordered! I wanted a {product}, but got a completely wrong item for {order_id}.", "Negative", "High", ["not", "wrong", "item"]),
        ("Order {order_id} is incorrect. I got the wrong model of {product}.", "Negative", "Medium", ["incorrect", "wrong", "model"]),
        ("Hi, you sent me the wrong {product}. My order is {order_id}. Please send the right one.", "Neutral", "Medium", ["sent", "wrong", "right"]),
        ("I think there was a mixup with {order_id}. I didn't order this {product}.", "Neutral", "Low", ["mixup", "didn't", "order"])
    ],
    "Password Reset": [
        ("I forgot my password and the reset link isn't working. Can you help?", "Neutral", "High", ["forgot", "password", "reset", "link"]),
        ("Please send a manual password reset link for my account.", "Neutral", "Medium", ["manual", "password", "reset"]),
        ("I can't access my account to check my {product} order. I need a password reset.", "Negative", "High", ["access", "account", "reset"]),
        ("Hi, I am not receiving the password reset emails. Please check.", "Negative", "Medium", ["receiving", "emails", "reset"]),
        ("Reset my password please. I am locked out.", "Neutral", "High", ["reset", "password", "locked"])
    ],
    "Login Issue": [
        ("I am trying to log in to track my {product} but it keeps saying invalid credentials.", "Negative", "High", ["log", "invalid", "credentials"]),
        ("My account is locked after too many attempts. Please unlock it.", "Negative", "High", ["locked", "attempts", "unlock"]),
        ("The login page is throwing a 500 error every time I try to sign in.", "Negative", "High", ["login", "error", "sign"]),
        ("I can't log in from my new phone. It asks for an OTP which never comes.", "Negative", "Medium", ["log", "phone", "OTP"]),
        ("Help! I am unable to login to my dashboard.", "Neutral", "Medium", ["help", "unable", "login"])
    ],
    "Payment Failure": [
        ("My card was charged for the {product} (Order {order_id}) but it says payment failed?", "Negative", "High", ["charged", "payment", "failed"]),
        ("I tried to buy a {product} but the checkout keeps failing with an error code.", "Negative", "Medium", ["buy", "checkout", "failing"]),
        ("Payment failed for {order_id} but money left my bank account. Fix this now.", "Negative", "High", ["payment", "failed", "money", "bank"]),
        ("Why is my credit card being declined for the {product} purchase?", "Negative", "Medium", ["credit", "declined", "purchase"]),
        ("I am getting a payment gateway error when trying to pay for {order_id}.", "Neutral", "High", ["gateway", "error", "pay"])
    ],
    "Subscription Cancellation": [
        ("I want to cancel my monthly subscription. Please stop charging me.", "Neutral", "Medium", ["cancel", "monthly", "subscription"]),
        ("Cancel my premium plan immediately. I don't use it anymore.", "Neutral", "High", ["cancel", "premium", "plan"]),
        ("How do I cancel my subscription? There's no button on the dashboard.", "Negative", "Medium", ["how", "cancel", "dashboard"]),
        ("Please process a cancellation for my account effective today.", "Neutral", "Medium", ["process", "cancellation", "effective"]),
        ("I am frustrated with the service. Cancel my subscription and delete my data.", "Negative", "High", ["frustrated", "cancel", "delete"])
    ],
    "Billing Problem": [
        ("I was double billed for my {product} purchase (Order {order_id}).", "Negative", "High", ["double", "billed", "purchase"]),
        ("There is a weird $5 charge on my invoice {order_id} that I don't recognize.", "Negative", "Medium", ["weird", "charge", "invoice"]),
        ("My invoice for {order_id} is missing the company VAT number. Please update it.", "Neutral", "Medium", ["invoice", "missing", "VAT"]),
        ("You charged me for a {product} even though I cancelled order {order_id}!", "Negative", "High", ["charged", "cancelled", "order"]),
        ("Please send a corrected bill for {order_id}. The total is wrong.", "Neutral", "Medium", ["corrected", "bill", "total"])
    ],
    "Feature Request": [
        ("It would be great if your app had a dark mode. Will you add it?", "Positive", "Low", ["great", "dark", "mode", "add"]),
        ("Can you integrate the {product} with Google Calendar in the next update?", "Neutral", "Low", ["integrate", "Google", "Calendar", "update"]),
        ("I really wish you had a bulk export feature for the invoices.", "Neutral", "Low", ["wish", "bulk", "export", "invoices"]),
        ("Please add support for multiple users on a single {product} license.", "Neutral", "Medium", ["support", "multiple", "users", "license"]),
        ("Feature request: Allow us to customize the dashboard layout.", "Neutral", "Low", ["feature", "request", "customize", "layout"])
    ],
    "Account Deletion": [
        ("I want to permanently delete my account and all associated data.", "Neutral", "High", ["permanently", "delete", "account", "data"]),
        ("Please close my account immediately. I no longer need your services.", "Neutral", "Medium", ["close", "account", "immediately"]),
        ("How do I delete my profile? I can't find the option anywhere.", "Negative", "Medium", ["delete", "profile", "option"]),
        ("Remove my email from your database and delete my account.", "Neutral", "Medium", ["remove", "email", "database", "delete"]),
        ("I am requesting a GDPR account deletion.", "Neutral", "High", ["requesting", "GDPR", "deletion"])
    ],
    "General Inquiry": [
        ("Do you offer bulk discounts if I order 50 units of the {product}?", "Neutral", "Low", ["bulk", "discounts", "units"]),
        ("Where are your {product}s manufactured?", "Neutral", "Low", ["manufactured", "where"]),
        ("Hi, I just wanted to know if the {product} comes with a warranty.", "Neutral", "Low", ["warranty", "comes"]),
        ("What are your customer support hours?", "Neutral", "Low", ["customer", "support", "hours"]),
        ("Can I use the {product} with a Mac?", "Neutral", "Low", ["use", "Mac", "compatibility"])
    ],
    "Shipping Address Change": [
        ("I need to change the shipping address for order {order_id} before it ships.", "Neutral", "High", ["change", "shipping", "address"]),
        ("Oops, I entered the wrong zip code for order {order_id}. Can you fix it?", "Neutral", "High", ["wrong", "zip", "code", "fix"]),
        ("Please update my delivery address for the {product} to my new office.", "Neutral", "Medium", ["update", "delivery", "address", "office"]),
        ("I am moving next week. Can you ship order {order_id} to my new address?", "Neutral", "High", ["moving", "ship", "new", "address"]),
        ("Change address for {order_id} immediately. It has my old apartment number.", "Negative", "High", ["change", "address", "immediately", "old"])
    ],
    "Order Status": [
        ("What is the status of my order {order_id} for the {product}?", "Neutral", "Low", ["status", "order"]),
        ("Has order {order_id} shipped yet? I placed it yesterday.", "Neutral", "Low", ["shipped", "placed", "yesterday"]),
        ("I need an update on my {product} purchase. Order ID is {order_id}.", "Neutral", "Medium", ["update", "purchase", "order"]),
        ("Can you tell me when {order_id} will be dispatched?", "Neutral", "Low", ["dispatched", "when"]),
        ("My order {order_id} says 'processing' for 3 days. Status please.", "Negative", "Medium", ["processing", "days", "status"])
    ],
    "Coupon Problem": [
        ("The discount code 'SAVE20' is not working on my {product} purchase.", "Negative", "Medium", ["discount", "code", "working", "purchase"]),
        ("I forgot to apply my 10% coupon to order {order_id}. Can you apply it retroactively?", "Neutral", "Medium", ["forgot", "apply", "coupon", "retroactively"]),
        ("Why does it say my promo code is invalid for the {product}?", "Negative", "Medium", ["promo", "code", "invalid"]),
        ("My welcome discount wasn't applied to order {order_id}.", "Negative", "Medium", ["welcome", "discount", "applied"]),
        ("I tried to use the holiday coupon but the checkout crashed.", "Negative", "High", ["holiday", "coupon", "checkout", "crashed"])
    ],
    "Gift Card Issue": [
        ("I can't redeem my $50 gift card. It says invalid code.", "Negative", "High", ["redeem", "gift", "card", "invalid"]),
        ("I purchased a gift card for a friend (Order {order_id}) but they never received the email.", "Negative", "High", ["purchased", "gift", "card", "received"]),
        ("Can I split my payment between a gift card and credit card for a {product}?", "Neutral", "Low", ["split", "payment", "gift", "card"]),
        ("What is the balance on my gift card? I want to buy a {product}.", "Neutral", "Low", ["balance", "gift", "card", "buy"]),
        ("My gift card expired yesterday! Can you extend it so I can buy the {product}?", "Neutral", "Medium", ["expired", "extend", "buy"])
    ],
    "Late Refund": [
        ("It's been 10 days since you approved my refund for {order_id} and I haven't seen the money.", "Negative", "High", ["days", "approved", "refund", "money"]),
        ("Where is my refund for the returned {product}? Order {order_id}.", "Negative", "High", ["where", "refund", "returned"]),
        ("You said the refund for {order_id} would take 3-5 days. It's been a week.", "Negative", "High", ["said", "refund", "days", "week"]),
        ("I am still waiting on the refund for order {order_id}. This is ridiculous.", "Negative", "High", ["waiting", "refund", "ridiculous"]),
        ("Please check the refund status for {order_id}. My bank says nothing is pending.", "Negative", "Medium", ["check", "refund", "status", "bank"])
    ],
    "Duplicate Payment": [
        ("I was charged twice for order {order_id}. Please reverse one of the charges.", "Negative", "High", ["charged", "twice", "reverse", "charges"]),
        ("My bank statement shows two identical payments for the {product}.", "Negative", "High", ["bank", "statement", "identical", "payments"]),
        ("I accidentally submitted the payment twice for {order_id}. Need a refund for the duplicate.", "Neutral", "Medium", ["accidentally", "submitted", "payment", "twice"]),
        ("You guys billed me 2 times for the {product}. Order {order_id}. Fix this.", "Negative", "High", ["billed", "times", "fix"]),
        ("Duplicate charge alert! Order {order_id} hit my card twice today.", "Negative", "High", ["duplicate", "charge", "alert", "hit"])
    ],
    "Technical Issue": [
        ("The website keeps freezing when I try to add the {product} to my cart.", "Negative", "Medium", ["website", "freezing", "cart"]),
        ("I am getting a 404 error when clicking on my order {order_id} link.", "Negative", "Medium", ["error", "clicking", "link"]),
        ("Your iOS app is crashing every time I open the {product} page.", "Negative", "High", ["iOS", "app", "crashing", "page"]),
        ("Images are not loading on the {product} description page.", "Neutral", "Low", ["images", "loading", "description"]),
        ("I can't download my invoice for {order_id}. The button does nothing.", "Negative", "Medium", ["download", "invoice", "button"])
    ]
}

def generate_expected_reply(category, customer, product, order_id):
    """Generate a realistic baseline expected reply."""
    first_name = customer.split()[0]
    replies = {
        "Delivery Delay": f"Hello {first_name},\n\nI apologize for the delay with your {product} (Order {order_id}). We are experiencing some unexpected shipping delays. I have escalated this with our courier, and it should arrive within the next 48 hours. Let me know if you need anything else.\n\nBest,\nSupport Team",
        "Refund Request": f"Hi {first_name},\n\nI'm sorry to hear the {product} didn't meet your expectations. I have processed the refund for order {order_id}. You should see the amount credited to your original payment method within 3-5 business days.\n\nBest,\nSupport Team",
        "Return Request": f"Hello {first_name},\n\nWe can certainly help you return your {product} (Order {order_id}). I have just emailed you a prepaid return shipping label. Once we receive the item, we will process your refund or replacement.\n\nBest,\nSupport Team",
        "Damaged Product": f"Dear {first_name},\n\nI am so sorry to hear that your {product} arrived damaged! That is not the experience we want for you. I am shipping a replacement for order {order_id} immediately via overnight delivery. You don't need to return the broken item.\n\nBest,\nSupport Team",
        "Wrong Product": f"Hi {first_name},\n\nI sincerely apologize for the mix-up with order {order_id}. We accidentally sent you the wrong item instead of the {product}. I've arranged for the correct item to be shipped out today, along with a return label for the incorrect item.\n\nBest,\nSupport Team",
        "Password Reset": f"Hello {first_name},\n\nI understand you're having trouble resetting your password. I have triggered a manual password reset email to your address. Please check your inbox (and spam folder) and click the link to create a new password.\n\nBest,\nSupport Team",
        "Login Issue": f"Hi {first_name},\n\nI'm sorry you are having trouble logging in. I have checked your account and reset your login attempts to unlock it. Please try logging in again, or let me know if you need a password reset.\n\nBest,\nSupport Team",
        "Payment Failure": f"Dear {first_name},\n\nI see the payment issue for the {product}. Sometimes transactions fail due to bank security blocks. Your card was not successfully charged for order {order_id}. Please try checking out again with a different card or PayPal.\n\nBest,\nSupport Team",
        "Subscription Cancellation": f"Hello {first_name},\n\nI have successfully cancelled your subscription as requested. You will not be charged going forward, but you will retain access until the end of your current billing cycle. We're sad to see you go!\n\nBest,\nSupport Team",
        "Billing Problem": f"Hi {first_name},\n\nI apologize for the billing confusion regarding order {order_id}. I've reviewed your account and corrected the invoice for your {product}. You'll receive the updated copy shortly, and we've refunded any overcharges.\n\nBest,\nSupport Team",
        "Feature Request": f"Hello {first_name},\n\nThanks for reaching out! That is a great suggestion for the {product}. I have forwarded your feature request to our product development team. We are always looking for ways to improve, so we appreciate your feedback.\n\nBest,\nSupport Team",
        "Account Deletion": f"Hi {first_name},\n\nPer your request, I have permanently deleted your account and all associated data from our systems. This action is irreversible. If you ever wish to return, you will need to create a new account.\n\nBest,\nSupport Team",
        "General Inquiry": f"Hello {first_name},\n\nThank you for your interest in our {product}. [Answer will be provided based on specific inquiry]. Let me know if you have any other questions and I'd be happy to help!\n\nBest,\nSupport Team",
        "Shipping Address Change": f"Hi {first_name},\n\nI've successfully updated the shipping address for order {order_id}. Your {product} will now be shipped to the new address provided. Let me know if you need further assistance!\n\nBest,\nSupport Team",
        "Order Status": f"Hello {first_name},\n\nThanks for checking in on order {order_id}. Your {product} is currently being packed in our warehouse and is scheduled to ship later today. You will receive an email with tracking information as soon as it leaves.\n\nBest,\nSupport Team",
        "Coupon Problem": f"Hi {first_name},\n\nI'm sorry you had trouble with the coupon code. I've manually applied the discount to your {product} purchase (Order {order_id}) and refunded the difference to your original payment method. \n\nBest,\nSupport Team",
        "Gift Card Issue": f"Hello {first_name},\n\nI apologize for the issue with the gift card. I've checked the balance and reset the code. You should now be able to apply it successfully towards your {product}. Let me know if it still gives you an error.\n\nBest,\nSupport Team",
        "Late Refund": f"Dear {first_name},\n\nI apologize for the delay in your refund for order {order_id}. I checked with our finance team and the refund was processed on our end, but it sometimes takes banks up to 10 days to post the funds. It should appear very soon.\n\nBest,\nSupport Team",
        "Duplicate Payment": f"Hi {first_name},\n\nI apologize for the duplicate charge on order {order_id}. I have immediately voided the second transaction for the {product}. You should see the funds returned to your account within 3-5 business days.\n\nBest,\nSupport Team",
        "Technical Issue": f"Hello {first_name},\n\nI'm sorry you are experiencing a technical issue with the {product} page. Our engineering team is aware of this bug and they are working on a fix right now. We appreciate your patience while we resolve this.\n\nBest,\nSupport Team"
    }
    return replies.get(category, "Thank you for reaching out. We will assist you shortly.")


def main():
    dataset = []
    
    # Generate 5 for each of the 20 categories to get 100 emails
    id_counter = 1
    
    for category in CATEGORIES:
        templates = TEMPLATES[category]
        for template, sentiment, priority, keywords in templates:
            customer = random.choice(CUSTOMERS)
            product = random.choice(PRODUCTS)
            order_id = f"{random.choice(ORDER_PREFIX)}{random.randint(10000, 99999)}"
            email_address = f"{customer.lower().replace(' ', '.')}@example.com"
            
            body = template.format(product=product, order_id=order_id)
            expected_reply = generate_expected_reply(category, customer, product, order_id)
            
            dataset.append({
                "id": id_counter,
                "category": category,
                "customer_name": customer,
                "customer_email": email_address,
                "email_body": body,
                "expected_reply": expected_reply,
                "priority": priority,
                "sentiment": sentiment,
                "keywords": keywords
            })
            id_counter += 1
            
    # Save to JSON
    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)
        
    print(f"Successfully generated {len(dataset)} realistic customer emails in dataset.json.")

if __name__ == "__main__":
    main()
