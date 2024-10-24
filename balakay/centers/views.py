from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Section, Center, Schedule, Category, Booking, FavoriteSection
from users.models import Client
from .forms import BookingForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

def home_view(request):
    categories = Category.objects.prefetch_related('sections').all()
    return render(request, 'centers/home.html', {'categories': categories})

def section_view(request, id):
    section = get_object_or_404(Section, id=id)
    schedules = Schedule.objects.filter(section=section)
    return render(request, 'centers/section.html', {"section": section, "schedules": schedules})

def book_schedule_view(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    # Check if the user has already booked this schedule for any of their children
    existing_bookings = Booking.objects.filter(schedule=schedule, user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        
        if form.is_valid():
            if existing_bookings.filter(user=request.user).exists():
                form.add_error(None, 'You have already booked this schedule for this child.')
            else:
                booking = form.save(commit=False)
                booking.schedule = schedule
                booking.user = request.user
                booking.save()
                schedule.total_slots -= 1
                schedule.save()

                return redirect(reverse('booking_success'))
    else:
        form = BookingForm(user=request.user)

    return render(request, 'centers/book_schedule.html', {'form': form, 'schedule': schedule})

def booking_success_view(request):
    return render(request, 'centers/booking_success.html')



def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == Booking.PENDING:
        booking.status = Booking.CANCELLED
        booking.cancelled_at = timezone.now()
        booking.save()

    return redirect('my-schedule')

def center_list_view(request):
    query = request.GET.get('q', '')

    centers = Center.objects.all()
    if query:
        centers = centers.filter(Q(name__icontains=query) | Q(id__icontains=query))

    return render(request, 'centers/center_list.html', {
        'centers': centers,
        'query': query,
    })

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('schedule')
    return render(request, 'centers/my_schedule.html', {'bookings': bookings})

def center_details(request, center_id):
    center = get_object_or_404(Center, id=center_id)
    schedules = Schedule.objects.filter(section__center=center)

    return render(request, 'centers/center_details.html', {'center': center, 'schedules': schedules})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    schedule = booking.schedule


    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            booking.status = Booking.CONFIRMED
            booking.confirmed_at = timezone.now()
        elif action == 'cancel':
            booking.status = Booking.CANCELLED
            booking.cancelled_at = timezone.now()
            schedule.total_slots += 1
            schedule.save()

        booking.save()
        return redirect(reverse('booking_detail', args=[booking.id]))

    return render(request, 'centers/booking_detail.html', {'booking': booking})


@login_required
def add_favorite_section(request, id):
    section = get_object_or_404(Section, id=id)
    client = request.user.client

    favorite, created = FavoriteSection.objects.get_or_create(client=client, section=section)

    if created:
        message = "Section added to favorites!"
    else:
        message = "Section is already in favorites."

    return redirect('section', id=id)


@login_required
def remove_favorite_section(request, id):
    section = get_object_or_404(Section, id=id)
    client = request.user.client

    FavoriteSection.objects.filter(client=client, section=section).delete()

    message = "Section removed from favorites."

    return redirect('section', id=id)


@login_required
def favorite_sections_view(request):
    client = request.user.client
    favorite_sections = FavoriteSection.objects.filter(client=client).select_related('section')

    return render(request, 'centers/favorite_sections.html', {'favorite_sections': favorite_sections})
