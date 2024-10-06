

# Create your views here.
import requests
from .models import discussion_forum, Userdata,Category,Quiz,Object
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from astropy.time import Time
from math import radians, sin, cos
from astropy.coordinates import get_body
from astropy.coordinates import solar_system_ephemeris
import spacy





'''def discussion(request):
    messages = discussion_forum.objects.all()
    return render(request, 'discussion.html', {'messages': messages})'''

'''def adddiscussion(request):
    logid = request.session['logid']
    title_dis=request.POST.get("discussion_title")
    cont=request.POST.get("content")
    user = Userdata.objects.get(id=logid)
    insertdata = discussion_forum(discussion_title=title_dis,content=cont,user_id=user,upvote=0,downvote=0)
    insertdata.save()
    return redirect('/discussion')'''


def adddiscussion(request):
    if request.method == 'POST':
        discussion_title = request.POST.get('discussion_title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        # Get the username from the session
        username = request.session.get('logusername')  # Retrieve username from session

        if not username:
            messages.error(request, 'You need to be logged in to add a discussion.')
            return redirect('discussion')  # Redirect to the discussion page

        try:
            # Fetch the Userdata instance using the username from the session
            user = Userdata.objects.get(username=username)
        except Userdata.DoesNotExist:
            messages.error(request, 'User does not exist in the Userdata model.')
            return redirect('discussion')

        # Create a new discussion
        new_discussion = discussion_forum.objects.create(
            discussion_title=discussion_title,
            content=content,
            user_id=user,  # Assign the Userdata instance
            category_id=category_id,  # Use category_id directly
            upvote=0,  # Initialize upvotes
            downvote=0  # Initialize downvotes
        )

        messages.success(request, 'Discussion posted successfully!')  # Optional success message
        return redirect('discussion')  # Redirect back to the discussion page

    return redirect('discussion')  # Handle GET request or invalid case

def lat_lon_to_cartesian(lat, lon, altitude=420):  # Altitude in kilometers
    # Radius of Earth in kilometers
    radius_earth = 6371.0  # Mean radius of the Earth

    # Convert latitude and longitude from degrees to radians
    lat_rad = radians(lat)
    lon_rad = radians(lon)

    # Calculate Cartesian coordinates
    x = (radius_earth + altitude) * cos(lat_rad) * cos(lon_rad)
    y = (radius_earth + altitude) * cos(lat_rad) * sin(lon_rad)
    z = (radius_earth + altitude) * sin(lat_rad)

    return x, y, z




'''def planets(request):
    # API URLs
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    response = requests.get(url)

    if response.status_code != 200:
        return render(request, 'index.html', {'error': 'Failed to fetch data from the API.'})

    bodies_data = response.json()

    # Initialize a list to hold planet data with coordinates
    planet_data = []

    # Using solar system ephemeris to get planet positions
    current_time = Time.now()  # Get the current time
    with solar_system_ephemeris.set('builtin'):
        for body in bodies_data['bodies']:
            if body.get('isPlanet', False):
                # Get the planetary position
                planet_position = get_body(body['englishName'].lower(), current_time)
                x, y, z = planet_position.cartesian.x.value, planet_position.cartesian.y.value, planet_position.cartesian.z.value

                # Initialize moon-related variables
                moon_names = []

                # Collect details about moons
                if 'moons' in body and body['moons'] is not None:
                    for moon in body['moons']:
                        # Extract the moon name from the moon object
                        if 'moon' in moon:
                            moon_names.append(moon['moon'])  # Add the moon name

                # Append planet data with coordinates and details
                planet_data.append({
                    'id': body.get('id', 'N/A'),
                    'moons': moon_names,  # List of moon names
                    'moon_count': len(moon_names),  # Count of moons
                    'name': body.get('englishName', 'Unknown'),
                    'x': x,
                    'y': y,
                    'z': z,
                    'mass': body.get('mass', {}).get('massValue', 'N/A'),  # Mass if available
                    'diameter': body.get('meanDiameter', 'N/A'),  # Diameter if available
                    'is_reference': body.get('englishName', '').lower() == 'earth'  # Mark Earth as the reference
                })

    # Render the data to the template
    return render(request, 'planets.html', {'planets': planet_data})'''

def planets(request):
    # API URLs
    url = "https://api.le-systeme-solaire.net/rest/bodies/"
    response = requests.get(url)

    if response.status_code != 200:
        return render(request, 'index.html', {'error': 'Failed to fetch data from the API.'})

    bodies_data = response.json()

    # Initialize a list to hold planet data with coordinates
    planet_data = []

    # Dictionary mapping planet names to image URLs
    planet_images = {
        'Mercury': 'images/mercury.gif',
        'Venus': 'images/venus.gif',
        'Earth': 'images/earth.gif',
        'Mars': 'images/mars.gif',
        'Jupiter': 'images/jupiter.gif',
        'Saturn': 'images/saturn2.gif',
        'Uranus': 'images/uranus2.gif',
        'Neptune': 'images/neptune.gif',
    }

    # Using solar system ephemeris to get planet positions
    current_time = Time.now()  # Get the current time
    with solar_system_ephemeris.set('builtin'):
        for body in bodies_data['bodies']:
            if body.get('isPlanet', False):
                # Get the planetary position
                planet_position = get_body(body['englishName'].lower(), current_time)
                x, y, z = planet_position.cartesian.x.value, planet_position.cartesian.y.value, planet_position.cartesian.z.value

                # Initialize moon-related variables
                moon_names = []

                # Collect details about moons
                if 'moons' in body and body['moons'] is not None:
                    for moon in body['moons']:
                        # Extract the moon name from the moon object
                        if 'englishName' in moon:  # Check if 'englishName' exists
                            moon_names.append(moon['englishName'])  # Add the moon name
                        else:
                            moon_names.append(moon.get('name', 'Unnamed'))  # Fallback to another field if necessary

                # Add the image URL for the planet
                image_url = planet_images.get(body.get('englishName', ''), 'static/images/default.jpg')

                # Append planet data with coordinates and details
                planet_data.append({
                    'id': body.get('id', 'N/A'),
                    'moons': moon_names,  # List of moon names
                    'moon_count': len(moon_names),  # Count of moons
                    'name': body.get('englishName', 'Unknown'),
                    'x': x,
                    'y': y,
                    'z': z,
                    'mass': body.get('mass', {}).get('massValue', 'N/A'),  # Mass if available
                    'diameter': body.get('meanDiameter', 'N/A'),  # Diameter if available
                    'is_reference': body.get('englishName', '').lower() == 'earth',  # Mark Earth as the reference
                    'image_url': image_url  # Add the image URL
                })

    # Render the data to the template
    return render(request, 'planets.html', {'planets': planet_data})




def checklogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    try:
        checkuser = Userdata.objects.get(username=username, password=password)
        request.session['logid'] = checkuser.id
        request.session['logusername'] = checkuser.username
        request.session['logemail'] = checkuser.email
        request.session['logadmin'] = checkuser.is_admin
    except:
        checkuser = None

    if checkuser is not None:
        if checkuser.is_admin is False:
            return redirect('/')
        else:
            return redirect('/')

    else:
        messages.error(request, "INVALID EMAIL OR PASSWORD. PLEASE TRY AGAIN")
        return redirect('/')

    messages.success(request, 'Login successfull !!')
    return render(request, "index.html")


def upvote(request, id):
    message = discussion_forum.objects.get(id=id)
    message.upvote += 1
    message.save()
    return redirect('/discussion')

def downvote(request, id):
    message = discussion_forum.objects.get(id=id)
    message.downvote += 1
    message.save()
    return redirect('/discussion')

def login(request):
    return render(request, "login.html")



def discussion(request):
    categories = Category.objects.all()  # Fetch all categories
    selected_category = None
    category_id = request.GET.get('category')  # Get category from query parameters

    if category_id:  # Check if category_id is provided
        selected_category = get_object_or_404(Category, id=category_id)  # Get the selected category
        messages = discussion_forum.objects.filter(category=selected_category).order_by('-created_at').select_related('user_id')
    else:
        messages = discussion_forum.objects.all().order_by('-created_at').select_related('user_id')

    paginator = Paginator(messages, 5)  # Show 5 discussions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'discussion.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
    })
def indexpage(request):
    response = ''
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = generate_response(user_input)  # Call your function to generate the response
    return render(request, "index.html", {'response': response})


def adduserdata(request):
    name=request.POST.get("name")
    email = request.POST.get("email")
    username = request.POST.get("username")
    #profile_picture = request.FILES.get["profile_pic"]
    password= request.POST.get("password")

    insertdata = Userdata(name=name,email=email,username=username,profile_picture=None,password=password,is_admin=False )
    insertdata.save()
    messages.success(request,"registration successfull")
    return redirect('/')


def register_page(request):
    return render(request, "registartion.html")


'''def add_reply(request, id):
    # Check if the request is a POST request
    if request.method == "POST":
        content = request.POST.get("contentr")  # Get the reply content

        # Get the discussion post to which the reply belongs
        discussion_post = get_object_or_404(discussion_forum, id=id)

        # Get the Userdata instance for the logged-in user
        userdata_instance = get_object_or_404(Userdata, username=request.user.username)

        # Create a new reply instance
        reply = discussion_forum(
            content=content,
            user_id=userdata_instance,  # Assign the Userdata instance here
            parent=discussion_post,  # Set the parent to the current discussion post
            upvote=0,  # Initial upvotes for replies can be 0
            downvote=0,  # Initial downvotes for replies can be 0
        )

        # Save the reply
        reply.save()

        # Provide a success message
        messages.success(request, "Reply added successfully.")

        # Redirect back to the discussion post (or wherever you want)
        return redirect('/discussion')  # Adjust this to your actual redirect URL

    # If not a POST request, you can handle it accordingly (e.g., return an error or redirect)
    messages.error(request, "Invalid request method.")
    return redirect('/discussion')  # Redirect back to the forum'''



def add_reply(request, id):
    # Check if the request is a POST request
    if request.method == "POST":
        content = request.POST.get("reply_content")  # Get the reply content

        # Get the discussion post to which the reply belongs
        discussion_post = get_object_or_404(discussion_forum, id=id)

        # Get the Userdata instance for the logged-in user
        userdata_instance = get_object_or_404(Userdata, username=request.user.username)

        # Create a new reply instance
        reply = discussion_forum(
            content=content,
            user_id=userdata_instance,  # Assign the Userdata instance here
            parent=discussion_post,  # Set the parent to the current discussion post
            upvote=0,  # Initial upvotes for replies can be 0
            downvote=0,  # Initial downvotes for replies can be 0
            category=discussion_post.category  # Set the category to the parent discussion's category
        )

        # Save the reply
        reply.save()

        # Provide a success message
        messages.success(request, "Reply added successfully.")

        # Redirect back to the discussion post (or wherever you want)
        return redirect('/discussion')  # Adjust this to your actual redirect URL

    # If not a POST request, you can handle it accordingly (e.g., return an error or redirect)
    messages.error(request, "Invalid request method.")
    return redirect('/discussion')  # Redirect back to the forum


def logoutpage(request):
    try:
        del request.session['logid']
        del request.session['logemail']
    except:
        pass
    return redirect('/')


def quiz(request, symbol):
    context = {
        'name': symbol
    }
    return render(request, 'quiz_home.html', context)



def solar(request):
    return render(request,'nasa_home.html')

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')

# API for solar system data
API_URL = "https://api.le-systeme-solaire.net/rest/bodies/"

def get_planet_data(planet_name):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()['bodies']
        for planet in data:
            if planet['englishName'].lower() == planet_name.lower():
                return {
                    'name': planet['englishName'],
                    'distance_from_sun': planet['semimajorAxis'],  # in km
                    'mass': planet['mass']['massValue'] if 'mass' in planet else None,
                    'gravity': planet['gravity'],
                    'diameter': planet['meanRadius'] * 2,  # diameter in km
                    'density': planet['density'],
                    'orbital_period': planet['sideralOrbit'],  # in days
                }
    return None

def calculate_distance_between(planets):
    distance = abs(planets[0]['distance_from_sun'] - planets[1]['distance_from_sun'])
    return distance

def generate_response(user_input):
    planets = ['earth', 'mars', 'neptune']
    user_input_lower = user_input.lower()

    # Check if the user asks about distances
    if "distance" in user_input_lower:
        planet_names = []
        for planet in planets:
            if planet in user_input_lower:
                planet_names.append(planet)

        if len(planet_names) == 2:  # Only proceed if two planets are mentioned
            planet_data = []
            for name in planet_names:
                data = get_planet_data(name)
                if data:
                    planet_data.append(data)

            if len(planet_data) == 2:
                distance = calculate_distance_between(planet_data)
                return f"The distance between {planet_data[0]['name']} and {planet_data[1]['name']} is approximately {distance:.2f} km."
            else:
                return "I couldn't find data for one of the planets."

    # Handle requests for general planet information
    for planet in planets:
        if planet in user_input_lower or f"what is {planet}" in user_input_lower or f"tell me about {planet}" in user_input_lower:
            planet_data = get_planet_data(planet)
            if planet_data:
                return (f"{planet_data['name']} has a gravity of {planet_data['gravity']} m/s², a mass of {planet_data['mass']} kg, "
                        f"a diameter of {planet_data['diameter']} km, a density of {planet_data['density']} g/cm³, "
                        f"it is {planet_data['distance_from_sun']:.2f} km from the Sun, and it takes {planet_data['orbital_period']} days to complete an orbit.")
            else:
                return f"I couldn't find any data for {planet}."

    # Handle individual planet information requests
    if any(planet in user_input_lower for planet in planets):
        for planet in planets:
            if planet in user_input_lower:
                planet_data = get_planet_data(planet)
                if planet_data:
                    if "mass" in user_input_lower:
                        return f"The mass of {planet_data['name']} is {planet_data['mass']} kg."
                    if "gravity" in user_input_lower:
                        return f"The gravity on {planet_data['name']} is {planet_data['gravity']} m/s²."
                    if "diameter" in user_input_lower:
                        return f"The diameter of {planet_data['name']} is {planet_data['diameter']} km."
                    if "density" in user_input_lower:
                        return f"The density of {planet_data['name']} is {planet_data['density']} g/cm³."
                    if "orbital period" in user_input_lower:
                        return f"{planet_data['name']} takes {planet_data['orbital_period']} days to complete its orbit."
                else:
                    return f"I couldn't find any data for {planet}."

    return "I'm not sure how to help with that."

# Main chatbot view
def chatbot(request):
    response = ''
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = generate_response(user_input)
    return render(request, 'chatbot.html', {'response': response})