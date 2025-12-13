from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
import os
import requests
import json
from datetime import datetime


def admin_required(view_func):
    """Decorator that requires both login AND admin user status (user must be in admin_users list)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        
        # Check if user is in admin_users list from FastAPI
        api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
        try:
            resp = requests.get(f"{api_base}/api/users", timeout=3)
            if resp.status_code == 200:
                admin_users = resp.json()
                admin_usernames = [u.get('username', '').lower() for u in admin_users]
                if request.user.username.lower() in admin_usernames:
                    return view_func(request, *args, **kwargs)
        except Exception:
            pass
        
        # User not in admin_users list - deny access
        return render(request, 'access_denied.html', {'message': 'You do not have admin access.'}, status=403)
    
    return wrapper


def index(request):
    # Try to fetch products from FastAPI service (server-side)
    products = []
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    # Note: FastAPI routers are mounted under /api
    try:
        resp = requests.get(f"{api_base}/api/products", timeout=3)
        if resp.status_code == 200:
            products = resp.json()
    except Exception:
        products = []

    # try to fetch rooms from API for homepage preview
    rooms_preview = []
    try:
        resp = requests.get(f"{api_base}/api/rooms", timeout=3)
        if resp.status_code == 200:
            rooms_preview = resp.json()[:3]
    except Exception:
        pass

    return render(request, 'index.html', {"rooms": rooms_preview, "testimonials": [], "products": products})

def rooms(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    rooms_list = []
    try:
        resp = requests.get(f"{api_base}/api/rooms", timeout=3)
        if resp.status_code == 200:
            rooms_list = resp.json()
    except Exception:
        pass
    
    # Apply filters from GET parameters
    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '1000')
    capacity = request.GET.get('capacity', '')
    amenities_param = request.GET.getlist('amenities')
    
    try:
        min_price = float(min_price) if min_price else 0
        max_price = float(max_price) if max_price else 1000
    except (ValueError, TypeError):
        min_price = 0
        max_price = 1000
    
    # Filter by price
    filtered_rooms = [r for r in rooms_list if min_price <= float(r.get('price', 0)) <= max_price]
    
    # Filter by capacity
    if capacity:
        try:
            capacity = int(capacity)
            filtered_rooms = [r for r in filtered_rooms if int(r.get('capacity', 0)) >= capacity]
        except (ValueError, TypeError):
            pass
    
    # Filter by amenities - for now use type as amenity indicator
    if amenities_param:
        filtered_rooms = [r for r in filtered_rooms if any(amenity.lower() in str(r).lower() for amenity in amenities_param)]
    
    return render(request, 'rooms.html', {
        "rooms": filtered_rooms,
        "min_price": min_price,
        "max_price": max_price,
        "capacity": capacity,
        "selected_amenities": amenities_param
    })

def room_details(request, room_id):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    room = None
    try:
        resp = requests.get(f"{api_base}/api/rooms/{room_id}", timeout=3)
        if resp.status_code == 200:
            room = resp.json()
    except Exception:
        pass
    return render(request, 'room_details.html', {"room": room})

def booking(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    rooms_list = []
    booking_success = False
    booking_error = None
    selected_room_id = None
    
    try:
        resp = requests.get(f"{api_base}/api/rooms", timeout=3)
        if resp.status_code == 200:
            rooms_list = resp.json()
    except Exception:
        pass
    
    # Get pre-selected room from query parameter
    if request.GET.get('room'):
        selected_room_id = request.GET.get('room')
    
    # Handle booking form submission
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            room_id = request.POST.get('room', '').strip()
            guests = request.POST.get('guests', '1').strip()
            checkin = request.POST.get('checkin', '').strip()
            checkout = request.POST.get('checkout', '').strip()
            special_requests = request.POST.get('special_requests', '').strip()
            
            # Validate required fields
            if not all([first_name, last_name, email, room_id, checkin, checkout]):
                booking_error = "Please fill in all required fields."
            else:
                # Get room details for pricing
                room_name = ""
                room_price = 0
                for room in rooms_list:
                    if str(room.get('id')) == room_id:
                        room_name = room.get('title', '')
                        room_price = float(room.get('price', 0))
                        break
                
                if not room_name:
                    booking_error = "Selected room not found."
                else:
                    # Calculate total from dates
                    checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
                    checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
                    nights = (checkout_date - checkin_date).days
                    
                    if nights <= 0:
                        booking_error = "Checkout date must be after check-in date."
                    else:
                        total = float(room_price * nights)
                        
                        # Create booking via FastAPI - match BookingSchema fields
                        booking_data = {
                            "guest_name": f"{first_name} {last_name}",
                            "room": room_name,
                            "checkin": checkin,
                            "checkout": checkout,
                            "nights": int(nights),
                            "total": total,
                            "status": "Pending"
                        }
                        
                        try:
                            post_resp = requests.post(f"{api_base}/api/bookings", json=booking_data, timeout=5)
                            if post_resp.status_code in [200, 201]:
                                booking_success = True
                            else:
                                booking_error = f"Booking service error (HTTP {post_resp.status_code}). Please try again."
                        except requests.exceptions.ConnectionError:
                            booking_error = "Cannot connect to booking service. Please check your internet connection."
                        except requests.exceptions.Timeout:
                            booking_error = "Booking service took too long to respond. Please try again."
        except ValueError:
            booking_error = "Invalid date format. Please use the date picker."
        except Exception as e:
            booking_error = f"Error processing booking: {str(e)}"
    
    return render(request, 'booking.html', {
        "rooms": rooms_list,
        "booking_success": booking_success,
        "booking_error": booking_error,
        "selected_room_id": selected_room_id
    })

@admin_required
def admin_dashboard(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    rooms_list = []
    bookings_list = []
    try:
        r = requests.get(f"{api_base}/api/rooms", timeout=3)
        if r.status_code == 200:
            rooms_list = r.json()
    except Exception:
        pass
    try:
        b = requests.get(f"{api_base}/api/bookings", timeout=3)
        if b.status_code == 200:
            bookings_list = b.json()
    except Exception:
        pass

    total_rooms = len(rooms_list)
    occupied_rooms = len([r for r in rooms_list if r.get("status") == "Occupied" or r.get("status") == "occupied" or r.get("status") == "Booked"])
    occupancy_rate = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0

    total_bookings = len(bookings_list)
    pending_bookings = len([b for b in bookings_list if b.get("status") == "Pending"])
    total_revenue = sum([b.get("total", 0) for b in bookings_list])
    
    # Calculate monthly bookings (simulate based on booking count - you can enhance this with date-based logic)
    # For now, distribute bookings across 6 months
    monthly_bookings = []
    if total_bookings > 0:
        per_month = max(1, total_bookings // 6)
        remainder = total_bookings % 6
        for i in range(6):
            count = per_month + (1 if i < remainder else 0)
            monthly_bookings.append(int(count * 8 + (i * 3)))  # Add variation
    else:
        monthly_bookings = [0, 0, 0, 0, 0, 0]
    
    # Calculate revenue trend (distribute total revenue across months)
    revenue_trend = []
    if total_revenue > 0:
        base_revenue = total_revenue / 6
        for i in range(6):
            trend_value = base_revenue * (0.8 + (i * 0.15))  # Upward trend
            revenue_trend.append(int(trend_value))
    else:
        revenue_trend = [0, 0, 0, 0, 0, 0]

    return render(request, 'admin_dashboard.html', {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "occupancy_rate": occupancy_rate,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "total_revenue": int(total_revenue),
        "monthly_bookings": monthly_bookings,
        "revenue_trend": revenue_trend,
        "recent_bookings": bookings_list,
    })

@admin_required
def admin_rooms(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    rooms_list = []
    try:
        r = requests.get(f"{api_base}/api/rooms", timeout=3)
        if r.status_code == 200:
            rooms_list = r.json()
    except Exception:
        pass
    total_rooms = len(rooms_list)
    occupied_rooms = len([r for r in rooms_list if r.get("status") == "Occupied" or r.get("status") == "occupied" or r.get("status") == "Booked"])
    available_rooms = total_rooms - occupied_rooms

    return render(request, 'admin_rooms.html', {
        "rooms": rooms_list,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms,
        "fastapi_url": api_base,
    })

@admin_required
def admin_bookings(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    bookings_list = []
    try:
        r = requests.get(f"{api_base}/api/bookings", timeout=3)
        if r.status_code == 200:
            bookings_list = r.json()
    except Exception:
        pass
    
    # Calculate stats from bookings
    total_bookings = len(bookings_list)
    confirmed_bookings = len([b for b in bookings_list if b.get("status") == "Confirmed"])
    pending_bookings = len([b for b in bookings_list if b.get("status") == "Pending"])
    total_revenue = sum([b.get("total", 0) for b in bookings_list])
    
    return render(request, 'admin_booking.html', {
        "bookings": bookings_list,
        "total_bookings": total_bookings,
        "confirmed_bookings": confirmed_bookings,
        "pending_bookings": pending_bookings,
        "total_revenue": total_revenue
    })

@admin_required
def admin_users(request):
    api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
    users_list = []
    try:
        r = requests.get(f"{api_base}/api/users", timeout=3)
        if r.status_code == 200:
            users_list = r.json()
    except Exception:
        pass
    total_users = len(users_list)
    return render(request, 'admin_users.html', {
        "users": users_list,
        "total_users": total_users,
        "fastapi_url": api_base
    })


@admin_required
def admin_settings(request):
    """Simple admin settings page that reads/writes a JSON file in the app folder."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    settings_path = os.path.join(base_dir, 'admin_settings.json')

    # default settings
    defaults = {
        "booking_auto_confirm": False,
        "notify_on_pending": True,
        "currency": "USD",
        "occupancy_alert_threshold": 80,
        "items_per_page": 10
    }

    settings_data = defaults.copy()
    try:
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as fh:
                settings_data.update(json.load(fh))
    except Exception:
        # ignore parse errors and keep defaults
        pass

    success = False
    error = None
    if request.method == 'POST':
        try:
            booking_auto_confirm = True if request.POST.get('booking_auto_confirm') == 'on' else False
            notify_on_pending = True if request.POST.get('notify_on_pending') == 'on' else False
            currency = request.POST.get('currency', 'USD').strip() or 'USD'
            occupancy_alert_threshold = int(request.POST.get('occupancy_alert_threshold', 80))
            items_per_page = int(request.POST.get('items_per_page', 10))

            new_settings = {
                "booking_auto_confirm": booking_auto_confirm,
                "notify_on_pending": notify_on_pending,
                "currency": currency,
                "occupancy_alert_threshold": occupancy_alert_threshold,
                "items_per_page": items_per_page
            }

            with open(settings_path, 'w', encoding='utf-8') as fh:
                json.dump(new_settings, fh, indent=2)

            settings_data = new_settings
            success = True
        except Exception as e:
            error = str(e)

    return render(request, 'admin_settings.html', {
        'settings': settings_data,
        'success': success,
        'error': error
    })


def login_view(request):
    """Custom login view for admin area."""
    from django.contrib.auth import authenticate, login as auth_login
    from django.shortcuts import redirect
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', '/staff-admin/')
            return redirect(next_url)
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """Logout view."""
    from django.contrib.auth import logout as auth_logout
    from django.shortcuts import redirect
    
    auth_logout(request)
    return redirect('index')
