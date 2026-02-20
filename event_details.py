#!/usr/bin/env python3
"""
Event Details - Fetch detailed information about a specific event
"""

import requests
import json

# Headers needed to bypass bots
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US',
    'Referer': 'https://fixr.co/',
    'FIXR-Platform': 'web',
    'FIXR-Platform-Version': 'Firefox/146.0',
    'FIXR-App-Version': '7.51.28',
    'FIXR-Tracking': '{}',
    'FIXR-Channel': 'fixr-website',
    'FIXR-Channel-Meta': 'e30=',
    'Origin': 'https://fixr.co',
}

SALES_ACCOUNT_ID = 41647474


def add_to_cart(event_id, ticket_id, ticket_name, ticket_currency):
    """Add a ticket to cart via conversions API"""
    url = "https://api.fixr.co/conversions"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0',
        'Accept': 'application/json; version=3.0',
        'Content-Type': 'application/json',
        'Authorization': 'Token 4bf9094f12f39d62639d9f3b0264abb3b6c81f94',
        'Cookie': 'cf_clearance=cwmM4mcWRiiu_Bs.t__u.eU6VGIvaB5.ww0E5O8SWZ0-1766449010-1.2.1.1-1vJeKcnnp4p4Pdw4kzgQCUCBn5SVbi93mJrCEVMO_Ov0f9bAZnq4ikzpUGifrfrKKFWhK8SbjEPFcAwWz59LdlStq39pQGusqcrAA5hSGm1nU3GfGCcFSaRfT8KjiUsT1UbOjKe5P0egN7mB2lczd_Xh2rylqTvUmAKVEEU.DrKsBaQpf9KXKZntvn8fErsqlxaHSzQJCvcW_q63h0fmAGhnvg4v2kC_jcGKdVx5SA5LbGueZ8RVe0cscccWVAoA; _gcl_au=1.1.1989132894.1766420873.1542140396.1766420911.1766420922; _scid=QhTIXLYGgYOKij7IITS4klcphN8JJ0Li; _ga_MNL5HL4LPJ=GS2.1.s1766497128$o6$g1$t1766503145$j58$l0$h0; _ga=GA1.1.1989132894.1766420873; _gat_UA-64cf00ed=1; _scid_r=QhTIXLYGgYOKij7IITS4klcphN8JJ0Li7CzFDQ; _fbp=fb.1.1766420953058.252236166999856554; _gid=GA1.2.772500220.1766422802; intercom-id-dvlcx7gb=005dd919-c414-4bd8-bc5a-69d8c369442f; intercom-session-dvlcx7gb=; intercom-device-id-dvlcx7gb=61b270ad-cffe-4fa0-b3f1-f27c89a49adf; __hssc=59433138.15.1766497138372; __hssrc=1; _uetsid=2b106980df5311f0924785647d57573e; _uetvid=2b107b30df5311f08e5d5974ec7ac36c',
    }
    
    payload = {
        "event_type": "AddToCart",
        "event_id": f"9d270a09-3f17-4d4b-b2f4-98930ec908f5-1136098-{event_id}",
        "sales_account_id": SALES_ACCOUNT_ID,
        "data": {
            "content_name": ticket_name,
            "content_ids": [str(ticket_id)],
            "content_type": "product",
            "currency": ticket_currency
        }
    }
    
    try:
        print(f"[PROCESSING] Preparing cart request with payload and headers...", flush=True)
        response = requests.post(url, headers=headers, json=payload)
        print(f"[RESPONSE] Add to cart status code: {response.status_code}", flush=True)
        
        if response.status_code >= 400:
            print(f"[ERROR] Response: {response.text}", flush=True)
        else:
            print(f"[SUCCESS] ✅ Ticket successfully added to cart", flush=True)
        
        return response.status_code
    except Exception as e:
        print(f"[ERROR] Error adding to cart: {str(e)}", flush=True)
        return None


def get_event_details(event_id):
    """Get detailed information about a specific event"""
    url = f"https://api.fixr.co/api/v2/app/event/{event_id}"
    
    response = requests.get(url, headers=HEADERS)
    
    # Always show response, even if there's an error
    print(f"[API] Event details status code: {response.status_code}", flush=True)
    
    try:
        data = response.json()
        print(f"[API] Event details response received:\n{json.dumps(data, indent=2)}", flush=True)
        print_event_details(data)
    except:
        print(f"[API] Event details response (text):\n{response.text}", flush=True)
        data = None
    
    response.raise_for_status()
    return data


def print_event_details(event_data):
    """Print formatted event details"""
    if not event_data or not isinstance(event_data, dict):
        return
    
    print(f"\n{'='*80}", flush=True)
    print(f"[DETAILS] 📋 EVENT DETAILS", flush=True)
    print(f"{'='*80}\n", flush=True)
    
    # Basic info
    print(f"Name: {event_data.get('name', 'N/A')}", flush=True)
    print(f"ID: {event_data.get('id', 'N/A')}", flush=True)
    
    # Description
    description = event_data.get('description', '')
    if description:
        desc_short = description[:200] + "..." if len(description) > 200 else description
        print(f"Description: {desc_short}", flush=True)
    
    # Dates
    start_time = event_data.get('start_time')
    end_time = event_data.get('end_time')
    if start_time:
        print(f"Start: {start_time}", flush=True)
    if end_time:
        print(f"End: {end_time}", flush=True)
    
    # Venue
    venue = event_data.get('venue')
    if venue:
        if isinstance(venue, dict):
            print(f"Venue: {venue.get('name', 'N/A')}", flush=True)
            address = venue.get('address', {})
            if isinstance(address, dict):
                city = address.get('city', '')
                country = address.get('country', '')
                if city or country:
                    print(f"Location: {city}, {country}", flush=True)
        else:
            print(f"Venue: {venue}", flush=True)
    
    # Sold out status
    is_sold_out = event_data.get('is_sold_out', False)
    sold_out_status = "🔴 SOLD OUT" if is_sold_out else "🟢 AVAILABLE"
    print(f"Status: {sold_out_status}", flush=True)
    
    # Prices
    min_price = event_data.get('min_price')
    max_price = event_data.get('max_price')
    if min_price is not None or max_price is not None:
        if min_price == max_price:
            price_str = f"£{min_price:.2f}" if min_price else "Free"
        else:
            price_str = f"£{min_price:.2f}" if min_price else "Free"
            if max_price and max_price != min_price:
                price_str += f" - £{max_price:.2f}"
        print(f"Price: {price_str}", flush=True)
    
    # Event status
    status = event_data.get('status')
    if status:
        print(f"Event Status: {status}", flush=True)
    
    # URL
    event_url = event_data.get('url') or event_data.get('fixr_url')
    if event_url:
        print(f"URL: {event_url}", flush=True)
    
    # Image
    image_url = event_data.get('image_url') or event_data.get('image')
    if image_url:
        print(f"Image: {image_url}", flush=True)
    
    # Tickets info
    tickets = event_data.get('tickets', [])
    if tickets:
        print(f"\n🎫 TICKETS ({len(tickets)} types):", flush=True)
        print(f"[PARSING] {'-'*76}", flush=True)
        
        first_available_ticket = None
        
        for i, ticket in enumerate(tickets, 1):
            if isinstance(ticket, dict):
                ticket_id = ticket.get('id', 'N/A')
                ticket_name = ticket.get('name', 'N/A')
                ticket_price = ticket.get('price')
                ticket_currency = ticket.get('currency', '£')
                ticket_max_per_user = ticket.get('max_per_user')
                ticket_sold_out = ticket.get('sold_out', False)
                
                status_icon = "🔴" if ticket_sold_out else "🟢"
                
                price_str = f"{ticket_currency}{ticket_price:.2f}" if ticket_price is not None else "Free"
                
                print(f"  [{i}] {status_icon} {ticket_name}", flush=True)
                print(f"      ID: {ticket_id}", flush=True)
                print(f"      Price: {price_str}", flush=True)
                
                if ticket_max_per_user is not None:
                    print(f"      Max per user: {ticket_max_per_user}", flush=True)
                
                print(f"      Sold Out: {'Yes' if ticket_sold_out else 'No'}", flush=True)
                print(f"", flush=True)
                
                # Store first available ticket
                if first_available_ticket is None and not ticket_sold_out:
                    first_available_ticket = {
                        'id': ticket_id,
                        'name': ticket_name,
                        'currency': ticket_currency,
                        'index': i
                    }
        
        # Add first available ticket to cart
        if first_available_ticket:
            event_id = event_data.get('id', '')
            start_time = event_data.get('start_time', 'N/A')
            print(f"\n[ACTION] 🛒 ADDING TO CART:", flush=True)
            print(f"   Event Date/Time: {start_time}", flush=True)
            print(f"   Ticket: [{first_available_ticket['index']}] {first_available_ticket['name']}", flush=True)
            print(f"   ID: {first_available_ticket['id']}", flush=True)
            print(f"", flush=True)
            add_to_cart(event_id, first_available_ticket['id'], first_available_ticket['name'], first_available_ticket['currency'])
    
    print(f"\n{'='*80}\n", flush=True)

