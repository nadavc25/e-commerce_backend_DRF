import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def send_order_notification(order):
    print("try send email")
    try:
        subject = f"New Order #{order.id}"
        message = f"Order #{order.id} has been created.\n\nDetails:\n\n"
        
        # Add user information
        message += f"User: {order.user.username}\n"
        message += f"Email: {order.user.email}\n"
        message += f"Phone number: {order.phone_number}\n\n"

        # Add shipping address
        message += "Shipping Address:\n"
        shipping_address = order.shipping_address
        message += f"{shipping_address['line1']}\n"
        if shipping_address.get('line2'):
            message += f"{shipping_address['line2']}\n"
        message += f"{shipping_address['city']}, {shipping_address['state']}, {shipping_address['postal_code']}\n"
        message += f"{shipping_address['country']}\n\n"

        # Add billing address
        # message += "Billing Address:\n"
        # billing_address = order.billing_address
        # message += f"{billing_address['line1']}\n"
        # if billing_address.get('line2'):
        #     message += f"{billing_address['line2']}\n"
        # message += f"{billing_address['city']}, {billing_address['state']}, {billing_address['postal_code']}\n"
        # message += f"{billing_address['country']}\n\n"

        # Add order items
        counter = 1
        for item in order.items.all():
            message += (
                f"Item {counter}:\n"
                f"Product: {item.product.name}\n"
                f"Quantity: {item.quantity}\n"
                f"Price: {item.price_at_purchase}\n"
                f"Size: {item.size}\n"
                f"Custom Name: {item.custom_name}\n"
                f"Custom Number: {item.custom_number}\n"
                f"Notes: {item.notes}\n\n"
            )
            counter += 1
        
        # Add total price
        message += f"Total Price: {order.total_price}\n"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Ensure this is set in your settings.py
            fail_silently=False,
        )
        logger.info(f"Order notification email sent for order #{order.id}")
    except Exception as e:
        logger.error(f"Failed to send order notification email for order #{order.id}: {e}")
        raise

def generate_firebase_storage_url(image_name):
    print(f"generate_firebase_storage_url")
    base_url = "https://firebasestorage.googleapis.com/v0/b/sport-jersey-e-commerce.appspot.com/o/"
    end_url = "?alt=media"
    url = f"{base_url}{image_name}{end_url}"
    print("gen", url)
    # Correct the URL format
    corrected_url = url.replace("/o/http://", "/o/")

    print(corrected_url)
    print(f"generate_firebase_storage_url")
    return corrected_url
