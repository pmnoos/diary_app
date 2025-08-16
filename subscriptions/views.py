from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from .models import SubscriptionPlan, UserSubscription, PaymentHistory
import logging

logger = logging.getLogger(__name__)

# Try to import Stripe, handle gracefully if not installed
try:
    import stripe
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    logger.warning("Stripe not installed. Payment processing will be disabled.")


@login_required
def subscription_plans(request):
    """Display available subscription plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    current_subscription = getattr(request.user, 'subscription', None)
    
    context = {
        'plans': plans,
        'current_subscription': current_subscription,
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
    }
    return render(request, 'subscriptions/plans.html', context)


@login_required
def manage_subscription(request):
    """Manage current subscription"""
    subscription = getattr(request.user, 'subscription', None)
    usage = getattr(request.user, 'usage', None)
    
    if not subscription:
        return redirect('subscription_plans')
    
    # Get payment history
    payments = PaymentHistory.objects.filter(user=request.user)[:10]
    
    context = {
        'subscription': subscription,
        'usage': usage,
        'payments': payments,
    }
    return render(request, 'subscriptions/manage.html', context)


@login_required
def upgrade_subscription(request, plan_id):
    """Upgrade to a premium subscription"""
    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    
    if request.method == 'POST':
        if not STRIPE_AVAILABLE:
            return JsonResponse({
                'error': 'Payment processing is currently unavailable. Please contact support.'
            }, status=400)
        
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan.name,
                            'description': f'Diary App - {plan.name}',
                        },
                        'unit_amount': int(plan.price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/subscriptions/success/'),
                cancel_url=request.build_absolute_uri('/subscriptions/plans/'),
                metadata={
                    'user_id': request.user.id,
                    'plan_id': plan.id,
                }
            )
            
            return JsonResponse({
                'checkout_url': checkout_session.url
            })
            
        except Exception as e:
            logger.error(f"Stripe checkout error: {e}")
            return JsonResponse({
                'error': 'Payment processing error. Please try again.'
            }, status=400)
    
    context = {
        'plan': plan,
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
        'stripe_available': STRIPE_AVAILABLE,
    }
    return render(request, 'subscriptions/upgrade.html', context)


@login_required
def subscription_success(request):
    """Handle successful payment"""
    messages.success(
        request, 
        'Payment successful! Your subscription has been upgraded.'
    )
    return redirect('manage_subscription')


@login_required
def cancel_subscription(request):
    """Cancel auto-renewal of subscription"""
    subscription = getattr(request.user, 'subscription', None)
    
    if subscription and request.method == 'POST':
        subscription.auto_renew = False
        subscription.save()
        
        messages.success(
            request,
            'Auto-renewal has been cancelled. Your subscription will remain '
            f'active until {subscription.end_date.strftime("%B %d, %Y")}.'
        )
    
    return redirect('manage_subscription')


def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    
    return JsonResponse({'status': 'success'})


def handle_successful_payment(session):
    """Process successful payment"""
    try:
        user_id = session['metadata']['user_id']
        plan_id = session['metadata']['plan_id']
        
        user = User.objects.get(id=user_id)
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # Update user subscription
        subscription, created = UserSubscription.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'end_date': timezone.now() + timezone.timedelta(days=plan.duration_days),
                'status': 'active',
                'auto_renew': True,
            }
        )
        
        if not created:
            subscription.plan = plan
            subscription.end_date = timezone.now() + timezone.timedelta(days=plan.duration_days)
            subscription.status = 'active'
            subscription.save()
        
        # Record payment
        PaymentHistory.objects.create(
            user=user,
            subscription=subscription,
            amount=plan.price,
            status='completed',
            payment_method='stripe',
            stripe_payment_id=session['payment_intent'],
            payment_date=timezone.now(),
        )
        
        logger.info(f"Subscription upgraded for user {user.username}")
        
    except Exception as e:
        logger.error(f"Error processing successful payment: {e}")


def handle_failed_payment(payment_intent):
    """Handle failed payment"""
    try:
        # Extract user info from payment_intent metadata
        user_id = payment_intent['metadata'].get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            subscription = getattr(user, 'subscription', None)
            
            if subscription:
                # Record failed payment
                PaymentHistory.objects.create(
                    user=user,
                    subscription=subscription,
                    amount=payment_intent['amount'] / 100,  # Convert from cents
                    status='failed',
                    payment_method='stripe',
                    stripe_payment_id=payment_intent['id'],
                    failure_reason=payment_intent.get('last_payment_error', {}).get('message', ''),
                )
                
                # Create failed payment reminder
                from .models import PaymentReminder
                PaymentReminder.objects.create(
                    user=user,
                    subscription=subscription,
                    reminder_type='failed_payment',
                    scheduled_date=timezone.now(),
                )
                
                logger.warning(f"Payment failed for user {user.username}")
        
    except Exception as e:
        logger.error(f"Error processing failed payment: {e}")
