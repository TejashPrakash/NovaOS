"""Weather skill for NovaOS AI layer."""

import requests
from ai.skills.base import Skill, SkillError, string_parameters
from ai.providers import Tool


def get_weather(kernel, location: str = "") -> str:
    """Get current weather for a location."""
    
    if not location:
        raise SkillError("get_weather needs a location")
    
    try:
        # Using a free weather API (you can replace with your preferred API)
        # This is a simplified example - you may want to use a proper weather API
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=metric")
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Weather in {location}: {temp}°C, {description}"
        else:
            return f"Could not fetch weather for {location}"
            
    except Exception as e:
        return f"Weather service unavailable: {str(e)}"


SKILLS = (
    Skill(
        tool=Tool(
            name="get_weather",
            description="Get current weather information for a location.",
            parameters=string_parameters(
                location="City name, e.g. London, New York, Tokyo"
            ),
        ),
        run=get_weather,
    ),
)