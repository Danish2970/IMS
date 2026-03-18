from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count
from .models import Location, Floor, Room, Item
from .forms import LocationForm, FloorForm, RoomForm, ItemForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from openpyxl import Workbook
from django.http import HttpResponse
from django.utils.dateparse import parse_date


# 1. Main Page: Show all Locations
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'management/location_list.html', {'locations': locations})


def add_location(request):
    # 1. Initialize the form based on request type
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()

    # 2. This ALWAYS returns a render object (Fixes the 'None' error)
    # 3. Ensure the template path is correct
    return render(request, 'management/add_location.html', {'form': form})

# 2. Floor Page: Show floors for a specific location
def floor_list(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    # Ensure you are filtering floors by the specific location
    floors = Floor.objects.filter(location=location)
    return render(request, 'management/floor_list.html', {
        'location': location,
        'floors': floors
    })


def add_floor(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if request.method == "POST":
        form = FloorForm(request.POST)
        if form.is_valid():
            floor = form.save(commit=False)
            floor.location = location  # Link floor to the location
            floor.save()
            return redirect('floor_list', location_id=location.id)
    else:
        form = FloorForm()  # <--- This line is CRITICAL for the GET request

    return render(request, 'management/add_floor.html', {
        'form': form,
        'location': location
    })
# 3. Room Views
def room_list(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    rooms = floor.rooms.all()
    return render(request, 'management/room_list.html', {'floor': floor, 'rooms': rooms})

def add_room(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.floor = floor
            room.save()
            return redirect('room_list', floor_id=floor.id)
    else:
        form = RoomForm()
    return render(request, 'management/add_room.html', {'form': form, 'floor': floor})

# 4. Item Views
def item_list(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    items = room.items.all()
    # TIP: It's better to pull these from Item.CATEGORY_CHOICES in models.py
    # but hardcoding for now is okay.
    categories = ['furniture', 'electronics', 'washroom', 'other']
    return render(request, 'management/item_list.html', {
        'room': room,
        'items': items,
        'categories': categories
    })

def add_item(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.room = room
            item.save()
            return redirect('item_list', room_id=room.id)
    else:
        form = ItemForm()
    return render(request, 'management/add_item.html', {'form': form, 'room': room})

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    room = item.room
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list', room_id=room.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'management/edit_item.html', {
        'form': form,
        'item': item,
        'room': room
    })

# 5. Delete Views
def delete_floor(request, floor_id):
    floor = get_object_or_404(Floor, id=floor_id)
    loc_id = floor.location.id
    floor.delete()
    return redirect('floor_list', location_id=loc_id)

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    f_id = room.floor.id
    room.delete()
    return redirect('room_list', floor_id=f_id)

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    r_id = item.room.id
    item.delete()
    return redirect('item_list', room_id=r_id)

# 6. Dashboard View
from django.shortcuts import render
from .models import Location, Floor, Room, Item

from django.shortcuts import render
from .models import Location, Floor, Room, Item


def dashboard(request):
    # 1. Capture ALL potential filter values from the URL
    loc_id = request.GET.get('location')
    floor_id = request.GET.get('floor')
    room_id = request.GET.get('room')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # 2. Prepare Dropdowns (Hierarchical)
    locations = Location.objects.all()
    floors = Floor.objects.filter(location_id=loc_id) if loc_id else Floor.objects.none()
    rooms = Room.objects.filter(floor_id=floor_id) if floor_id else Room.objects.none()

    # 3. BASE DATA: Start with every single item in the database
    # We use select_related to make the database query faster
    items = Item.objects.all().select_related('room__floor__location')

    # 4. DYNAMIC FILTERING (The "Subtraction" Process)

    # If a Location is picked, hide everything else
    if loc_id:
        items = items.filter(room__floor__location_id=loc_id)

    # If a Floor is picked, narrow it down further
    if floor_id:
        items = items.filter(room__floor_id=floor_id)

    # If a Room is picked, narrow it down to just that room
    if room_id:
        items = items.filter(room_id=room_id)

    # If a Date Range is picked, hide items outside those dates
    if start_date and end_date:
        items = items.filter(date_in__range=[start_date, end_date])

    # 5. Group the REMAINING items by category
    categories = items.values_list('category', flat=True).distinct()

    # 6. Context for the template
    context = {
        'locations': locations,
        'floors': floors,
        'rooms': rooms,
        'items': items,
        'categories': categories,
        'selected_location': loc_id,
        'selected_floor': floor_id,
        'selected_room': room_id,
        'start_date': start_date,
        'end_date': end_date,
        # Helper to show which room is active in the title
        'room_obj': Room.objects.filter(id=room_id).first() if room_id else None,
    }
    return render(request, 'management/dashboard.html', context)



def export_excel(request, room_id):
    room = Room.objects.get(id=room_id)

    # Create a workbook and a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventory"

    # Define the header row
    columns = ['Category', 'Item Name', 'Brand', 'Quantity', 'Date In']
    ws.append(columns)

    # Fetch data and add to rows
    items = Item.objects.filter(room_id=room_id)
    for item in items:
        ws.append([
            item.category,
            item.item_name,
            item.brand if item.brand else "-",
            item.quantity,
            str(item.date_in) if item.date_in else "-"
        ])

    # Prepare the response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="Inventory_Room_{room.room_number}.xlsx"'

    wb.save(response)
    return response


# PDF Export View
def export_pdf(request, room_id):
    room = Room.objects.get(id=room_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Inventory_Room_{room.room_number}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Inventory Report: Room {room.room_number}")
    p.setFont("Helvetica", 12)

    y = 700
    items = Item.objects.filter(room_id=room_id)

    p.drawString(100, y, "Item Name - Category - Qty")
    y -= 20

    for item in items:
        p.drawString(100, y, f"{item.item_name} | {item.category} | {item.quantity}")
        y -= 20
        if y < 50:  # Simple page break logic
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response