from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from ..models import Payment
from ..forms import PaymentForm
from ..core import parser


def validate_twitter_account_or_account_number_exists(account_number: str, twitter_id: int):
    """Same twitter account id or account number cannot be used again
    Args:
        account_number (str): TNB public key
        twitter_id (int): Id of a specific twitter account
    Returns:
        False: If account_number or twitter_id already exists
        account_number, twitter_id: Account object, Twitter ID in the else case
    """

    if Payment.objects.filter(user_twitter_id=twitter_id).exists() \
            or Payment.objects.filter(account_number=account_number).exists():
        return False
    else:
        return True


@user_passes_test(lambda u: u.is_staff)
def faucet_view(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            url_str = form.cleaned_data['url']
            amount = form.cleaned_data['amount']
            post = parser.process(url_str, amount)
            if post:
                receiver_account_number = post.get_account_number()
                user_id = post.get_user()
                account = validate_twitter_account_or_account_number_exists(receiver_account_number, user_id)

                if account:
                    post_model, created = Payment.objects.get_or_create(
                        account_number=receiver_account_number,
                        user_twitter_id=user_id,
                        amount=amount,
                    )
                    messages.success(
                        request,
                        (f'SUCCESS! {amount} faucet funds'
                         f' transferred to {receiver_account_number}.'))
                else:
                    messages.error(
                        request,
                        ('Same account number or twitter id cannot be used again! '
                        ' Try again with a new one :P')
                    )
            else:
                messages.error(
                    request,
                    ('Failed to extract information!'
                    ' Make sure post is public,'
                    ' contains #TNBFaucet and your account number')
                )
        else:
            messages.error(
                request,
                'Form invalid! Please provide correct details!'
            )
    
    context = {
        'form': form
    }

    return render(request, 'parser_form.html', context)
