"""Disabled local MCP payment placeholders; none are registered with the model."""
from dataclasses import dataclass

@dataclass
class PaymentRequest:
    amount: str
    currency: str
    merchant_reference: str

def stripe_sandbox(request: PaymentRequest):
    raise NotImplementedError('Stripe MCP sandbox not yet implemented')

def paypal_sandbox(request: PaymentRequest):
    raise NotImplementedError('PayPal MCP sandbox not yet implemented')

def square_sandbox(request: PaymentRequest):
    raise NotImplementedError('Square MCP sandbox not yet implemented')
