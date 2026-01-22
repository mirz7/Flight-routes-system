
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Min
from .models import Route, Airport
from .forms import (
    RouteForm, SearchNthNodeForm, 
    LongestRouteForm, ShortestRouteBetweenForm
)


def add_route(request):
    """
    View for adding a new airport route.
    """
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route added successfully!')
            return redirect('add_route')
    else:
        form = RouteForm()
    
    # Display all existing routes
    routes = Route.objects.all()
    
    return render(request, 'routes/add_route.html', {
        'form': form,
        'routes': routes
    })


def find_nth_node(request):
    """
    Question 1: Find the Nth Left or Right Node in an Airport Route.
    Returns the airport that is the Nth node in the specified direction from the given airport.
    """
    result = None
    
    if request.method == 'POST':
        form = SearchNthNodeForm(request.POST)
        if form.is_valid():
            airport = form.cleaned_data['airport']
            direction = form.cleaned_data['direction']
            n = form.cleaned_data['n']
            
            # Get all routes from the airport in the specified direction
            routes = Route.objects.filter(
                from_airport=airport,
                direction=direction
            ).select_related('to_airport').order_by('to_airport__position')
            
            if routes.count() >= n:
                # Get the Nth route (n-1 because of zero-indexing)
                nth_route = routes[n - 1]
                result = {
                    'success': True,
                    'airport': airport,
                    'direction': direction,
                    'n': n,
                    'found_airport': nth_route.to_airport,
                    'duration': nth_route.duration
                }
            else:
                result = {
                    'success': False,
                    'message': f'Only {routes.count()} {direction} route(s) found from {airport.code}. Cannot find {n}th node.'
                }
    else:
        form = SearchNthNodeForm()
    
    return render(request, 'routes/find_nth_node.html', {
        'form': form,
        'result': result
    })


def find_longest_route(request):
    """
    Question 2: Find the Longest Node based on duration in the Airport.
    Returns the route with the maximum duration from the given airport.
    """
    result = None
    
    if request.method == 'POST':
        form = LongestRouteForm(request.POST)
        if form.is_valid():
            airport = form.cleaned_data['airport']
            
            # Find the longest route from this airport
            longest_route = Route.objects.filter(
                from_airport=airport
            ).select_related('to_airport').order_by('-duration').first()
            
            if longest_route:
                result = {
                    'success': True,
                    'airport': airport,
                    'longest_route': longest_route,
                    'to_airport': longest_route.to_airport,
                    'direction': longest_route.direction,
                    'duration': longest_route.duration
                }
            else:
                result = {
                    'success': False,
                    'message': f'No routes found from {airport.code}.'
                }
    else:
        form = LongestRouteForm()
    
    return render(request, 'routes/find_longest_route.html', {
        'form': form,
        'result': result
    })


def find_shortest_route_between(request):
    """
    Question 3: Find the Shortest Node based on duration Between Two Airports.
    Returns the route with minimum duration between two airports.
    """
    result = None
    
    if request.method == 'POST':
        form = ShortestRouteBetweenForm(request.POST)
        if form.is_valid():
            from_airport = form.cleaned_data['from_airport']
            to_airport = form.cleaned_data['to_airport']
            
            # Find the shortest direct route between the two airports
            shortest_route = Route.objects.filter(
                from_airport=from_airport,
                to_airport=to_airport
            ).order_by('duration').first()
            
            if shortest_route:
                result = {
                    'success': True,
                    'from_airport': from_airport,
                    'to_airport': to_airport,
                    'shortest_route': shortest_route,
                    'direction': shortest_route.direction,
                    'duration': shortest_route.duration
                }
            else:
                result = {
                    'success': False,
                    'message': f'No direct route found from {from_airport.code} to {to_airport.code}.'
                }
    else:
        form = ShortestRouteBetweenForm()
    
    return render(request, 'routes/find_shortest_route.html', {
        'form': form,
        'result': result
    })


def home(request):
    """
    Home page with links to all features.
    """
    return render(request, 'routes/home.html')