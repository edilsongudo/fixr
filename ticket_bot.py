#!/usr/bin/env python3
"""
Ticket Bot - Simple bot to search events on Fixr
"""

import os
import time
import random
import requests
import json
from dotenv import load_dotenv
from event_details import get_event_details

load_dotenv()

# Headers needed to bypass bots
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:146.0) Gecko/20100101 Firefox/146.0',
    'Accept': 'application/json; version=3.0',
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


def search_events(limit=50):
    """Search events on Fixr API"""
    # Get coordinates from environment variables
    lat = float(os.getenv('FIXR_LAT', '-25.9655'))
    lon = float(os.getenv('FIXR_LON', '32.5832'))
    
    url = "https://api.fixr.co/search/events"
    params = {
        'lat': lat,
        'lon': lon,
        'limit': limit,
        'offset': 0,
        'ordering': 'distance',
        'min_boost': 1
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    # Always show response, even if there's an error
    print(f"[API] Status code: {response.status_code}", flush=True)
    
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2)}", flush=True)
    except:
        print(f"Response (text):\n{response.text}", flush=True)
        data = None
    
    response.raise_for_status()
    return data


if __name__ == "__main__":
    # Random intervals between requests (in seconds)
    min_interval = int(os.getenv('POLL_INTERVAL_MIN', '60'))
    max_interval = int(os.getenv('POLL_INTERVAL_MAX', '75'))
    
    # Get coordinates
    lat = float(os.getenv('FIXR_LAT', '-25.9655'))
    lon = float(os.getenv('FIXR_LON', '32.5832'))
    
    print(f"[BOT STARTED] 🚀 Bot is running...", flush=True)
    print(f"[CONFIG] Random interval between {min_interval}s and {max_interval}s", flush=True)
    print(f"[CONFIG] Search coordinates: lat={lat}, lon={lon}\n", flush=True)
    
    while True:
        try:
            print(f"[SEARCHING] 🔍 Searching for events...", flush=True)
            data = search_events()
            
            if data and isinstance(data, dict):
                events = data.get('results', [])
                print(f"[RESULTS] ✅ Found {len(events)} events\n", flush=True)
                
                # Find first available event
                first_available_event = None
                print(f"[PARSING] 📊 Parsing event details...\n", flush=True)
                
                for event in events:
                    print(f"• {event.get('name', 'N/A')}", flush=True)
                    print(f"  ID: {event.get('id')}", flush=True)
                    
                    # Venue
                    if event.get('venue'):
                        venue = event['venue']
                        if isinstance(venue, dict):
                            print(f"  Venue: {venue.get('name', 'N/A')}", flush=True)
                    
                    # Sold out status
                    is_sold_out = event.get('is_sold_out', False)
                    sold_out_status = "🔴 SOLD OUT" if is_sold_out else "🟢 AVAILABLE"
                    print(f"  Status: {sold_out_status}", flush=True)
                    
                    # Prices
                    min_price = event.get('min_price')
                    max_price = event.get('max_price')
                    if min_price is not None or max_price is not None:
                        if min_price == max_price:
                            price_str = f"£{min_price:.2f}" if min_price else "Free"
                        else:
                            price_str = f"£{min_price:.2f}" if min_price else "Free"
                            if max_price and max_price != min_price:
                                price_str += f" - £{max_price:.2f}"
                        print(f"  Price: {price_str}", flush=True)
                    
                    # Dates
                    start_time = event.get('start_time')
                    end_time = event.get('end_time')
                    if start_time:
                        print(f"  Start: {start_time}", flush=True)
                    if end_time:
                        print(f"  End: {end_time}", flush=True)
                    
                    # Status
                    status = event.get('status')
                    if status:
                        print(f"  Event Status: {status}", flush=True)
                    
                    # URL
                    event_url = event.get('url') or event.get('fixr_url')
                    if event_url:
                        print(f"  URL: {event_url}", flush=True)
                    
                    # Track first available event
                    if not first_available_event and not is_sold_out:
                        first_available_event = event
                    
                    print(flush=True)
                
                # Get details of first available event
                if first_available_event:
                    # event_id = first_available_event.get('id')
                    event_id = 378646080
                    print(f"\n[FETCHING] 📋 Fetching details for first available event (ID: {event_id})...\n", flush=True)
                    try:
                        event_details = get_event_details(event_id)
                        if event_details:
                            print(f"\n[SUCCESS] ✅ Event details retrieved successfully\n", flush=True)
                    except Exception as e:
                        print(f"[ERROR] ❌ Error fetching event details: {e}\n", flush=True)
                else:
                    print(f"\n[INFO] ⚠️  No available events found at this moment\n", flush=True)
            
            # Random interval before next request
            interval = random.randint(min_interval, max_interval)
            print(f"\n[WAITING] ⏳ Waiting {interval}s before next request...\n", flush=True)
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\n[STOP] 👋 Bot stopped by user.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] ❌ Error: {e}", flush=True)
            interval = random.randint(min_interval, max_interval)
            print(f"[RETRY] 🔄 Retrying in {interval}s...\n", flush=True)
            time.sleep(interval)
