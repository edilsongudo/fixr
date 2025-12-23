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


def get_event_details(event_id):
    """Get detailed information about a specific event"""
    url = f"https://api.fixr.co/api/v2/app/event/{event_id}"
    
    response = requests.get(url, headers=HEADERS)
    
    # Always show response, even if there's an error
    print(f"Event Details Status: {response.status_code}", flush=True)
    
    try:
        data = response.json()
        print(f"Event Details Response:\n{json.dumps(data, indent=2)}", flush=True)
        print_event_details(data)
    except:
        print(f"Event Details Response (text):\n{response.text}", flush=True)
        data = None
    
    response.raise_for_status()
    return data


def print_event_details(event_data):
    """Print formatted event details"""
    if not event_data or not isinstance(event_data, dict):
        return
    
    print(f"\n{'='*80}", flush=True)
    print(f"📋 EVENT DETAILS", flush=True)
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
    sold_out_status = "🔴 SOLD OUT" if is_sold_out else "🟢 Available"
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
        print(f"\nTickets ({len(tickets)} types):", flush=True)
        for ticket in tickets[:5]:  # Show first 5 ticket types
            if isinstance(ticket, dict):
                ticket_name = ticket.get('name', 'N/A')
                ticket_price = ticket.get('price')
                ticket_available = ticket.get('available', False)
                status_icon = "🟢" if ticket_available else "🔴"
                price_str = f"£{ticket_price:.2f}" if ticket_price else "Free"
                print(f"  {status_icon} {ticket_name} - {price_str}", flush=True)
    
    print(f"\n{'='*80}\n", flush=True)

