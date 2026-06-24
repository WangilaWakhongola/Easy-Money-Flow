"""
M-Pesa API Integration Module
Handles authentication, transaction processing, and webhook handling
"""

import requests
import json
import base64
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class MPesaConfig:
    """M-Pesa API Configuration"""
    
    # Sandbox URLs
    SANDBOX_OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    SANDBOX_API_URL = "https://sandbox.safaricom.co.ke/mpesa"
    
    # Production URLs
    PRODUCTION_OAUTH_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    PRODUCTION_API_URL = "https://api.safaricom.co.ke/mpesa"
    
    # Endpoints
    STK_PUSH_ENDPOINT = "/stkpush/v1/processrequest"
    TRANSACTION_STATUS_ENDPOINT = "/transactionstatus/v1/query"
    ACCOUNT_BALANCE_ENDPOINT = "/accountbalance/v1/query"
    
    def __init__(self, environment='sandbox'):
        self.environment = environment
        self.oauth_url = self.SANDBOX_OAUTH_URL if environment == 'sandbox' else self.PRODUCTION_OAUTH_URL
        self.api_url = self.SANDBOX_API_URL if environment == 'sandbox' else self.PRODUCTION_API_URL


class MPesaClient:
    """M-Pesa API Client"""
    
    def __init__(self, consumer_key, consumer_secret, environment='sandbox'):
        """
        Initialize M-Pesa client
        
        Args:
            consumer_key: M-Pesa app consumer key
            consumer_secret: M-Pesa app consumer secret
            environment: 'sandbox' or 'production'
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.config = MPesaConfig(environment)
        self.access_token = None
        self.token_expiry = None
    
    def _get_access_token(self):
        """Get OAuth access token from M-Pesa"""
        try:
            auth = (self.consumer_key, self.consumer_secret)
            response = requests.get(
                self.config.oauth_url,
                auth=auth,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get('access_token')
            
            logger.info("Successfully obtained M-Pesa access token")
            return self.access_token
        
        except requests.RequestException as e:
            logger.error(f"Failed to get M-Pesa access token: {str(e)}")
            raise
    
    def _make_request(self, endpoint, payload):
        """Make authenticated request to M-Pesa API"""
        if not self.access_token:
            self._get_access_token()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = self.config.api_url + endpoint
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"M-Pesa API request failed: {str(e)}")
            raise
    
    def initiate_stk_push(self, phone_number, amount, account_ref, description):
        """
        Initiate STK Push (prompt user to enter M-Pesa PIN)
        
        Args:
            phone_number: Customer phone (e.g., '254700000000')
            amount: Amount in KES
            account_ref: Unique account reference
            description: Transaction description
        
        Returns:
            Response from M-Pesa API
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # For sandbox, use test credentials
        # In production, use your actual paybill/till number
        business_shortcode = "174379"  # Sandbox test code
        passkey = "bfb279f9aa9bdbcf158e97dd1a503017"  # Sandbox test passkey
        
        # Create password by concatenating shortcode + passkey + timestamp and base64 encoding
        password_string = f"{business_shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/api/mpesa/callback/",  # Update with your domain
            "AccountReference": account_ref,
            "TransactionDesc": description
        }
        
        return self._make_request(self.config.STK_PUSH_ENDPOINT, payload)
    
    def query_transaction_status(self, transaction_id):
        """
        Query status of a transaction
        
        Args:
            transaction_id: M-Pesa transaction ID
        
        Returns:
            Transaction status details
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_shortcode = "174379"
        passkey = "bfb279f9aa9bdbcf158e97dd1a503017"
        
        password_string = f"{business_shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": transaction_id
        }
        
        return self._make_request(self.config.TRANSACTION_STATUS_ENDPOINT, payload)
    
    def check_account_balance(self):
        """Check M-Pesa account balance"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_shortcode = "174379"
        passkey = "bfb279f9aa9bdbcf158e97dd1a503017"
        
        password_string = f"{business_shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        
        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "IdentifierType": "4",
            "Remarks": "Account Balance Check",
            "InitiatorName": "initiator",
            "SecurityCredential": "Your encrypted credential",  # Needs encryption
            "QueueTimeOutURL": "https://yourdomain.com/api/mpesa/timeout/",
            "ResultURL": "https://yourdomain.com/api/mpesa/result/"
        }
        
        return self._make_request(self.config.ACCOUNT_BALANCE_ENDPOINT, payload)


class MPesaTransactionProcessor:
    """Process and import M-Pesa transactions"""
    
    @staticmethod
    def parse_callback_data(callback_data):
        """
        Parse M-Pesa callback webhook data
        
        Args:
            callback_data: JSON data from M-Pesa webhook
        
        Returns:
            dict with parsed transaction details
        """
        try:
            result = callback_data.get('Result', {})
            
            if result.get('ResultCode') != 0:
                return None
            
            params = result.get('ResultParameters', {}).get('ResultParameter', [])
            param_dict = {p['Key']: p['Value'] for p in params}
            
            return {
                'transaction_id': result.get('TransactionID'),
                'amount': Decimal(str(param_dict.get('Amount', 0))),
                'date': datetime.strptime(
                    param_dict.get('TransactionDate', ''),
                    '%Y%m%d%H%M%S'
                ).date(),
                'phone': param_dict.get('PhoneNumber', ''),
                'description': param_dict.get('Description', 'M-Pesa Transaction'),
            }
        
        except Exception as e:
            logger.error(f"Error parsing M-Pesa callback: {str(e)}")
            return None


# Example usage:
"""
from .mpesa_integration import MPesaClient

# Initialize client
client = MPesaClient(
    consumer_key='your_consumer_key',
    consumer_secret='your_consumer_secret',
    environment='sandbox'
)

# Initiate payment prompt
response = client.initiate_stk_push(
    phone_number='254700000000',
    amount=1000,
    account_ref='USER001',
    description='Lunch payment'
)

# Check transaction status
status = client.query_transaction_status('transaction_id')

# Check account balance
balance = client.check_account_balance()
"""
