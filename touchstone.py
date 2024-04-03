# Importing Necessary Modules
import os
import requests
import pandas as pd
import datetime
import sys

# Reference: https://openweathermap.org/API
# Save your API key here after creating key from OpenWeatherMap
# API_KEY = "276070469248398c9abdb316f27dd0a5"

def get_weather_data(api_key, city, state_code):
  # Construct the API request URL using the provided parameters
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state_code.strip()},US&appid={api_key}"
  # Send the API request and get the response
  response = requests.get(url)

  # Check if the API request was successful (status code 200)
  if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the relevant weather data and format it
    weather_data = {
        'City': data["name"],
        'Weather': data["weather"][0]["description"],
        'Feels Like': round((data["main"]["feels_like"] - 273.15) * 1.8 + 32),
        'Temperature': round((data["main"]["temp"] - 273.15) * 1.8 + 32),
        'Humidity': data["main"]["humidity"],
        'Wind Speed': round(data["wind"]["speed"] * 2.237),
        'Datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Return the weather data
    return weather_data
  else:
    # Print an error message and return None if the API request failed
    print(f"Error retrieving data: HTTP {response.status_code} - {response.reason}")
    return None

def save_to_csv(filename, weather_data):
  # Create a Pandas DataFrame from the weather data
  df = pd.DataFrame(weather_data, index=[0])
  # Check if the file already exists
  header = not os.path.isfile(filename)
  # Append the data to the CSV file, writing the header if the file is new
  df.to_csv(filename, mode='a', index=False, header=header)

def get_user_input():
  while True:
    # Prompt the user to enter a city and state
    city_state = input("Enter a city and state (e.g. Madison, IN): ")
    try:
        # Split the input into city and state_code
        city, state_code = city_state.split(",")
        # Prompt the user to enter the API key
        api_key = input(
            "Enter your API key from OpenWeatherMap (https://openweathermap.org/): ")
        # Return the city, state_code, and api_key
        return city.strip(), state_code.strip(), api_key
    except ValueError:
        # If the input format is invalid, print an error message and re-prompt the user
        print("Invalid format. Please enter the city and state abbreviations separated by a comma.")

def main():
  while True:
    # Display the menu options
    print("\nMenu:")
    print("1. Get Weather Data")
    print("2. Instructions for Obtaining API Key")
    print("3. Exit")

    # Prompt the user to enter their choice
    choice = input("Enter your choice: ")

    if choice == "1":
      # Get the user input for city, state, and API key
      city, state_code, api_key = get_user_input()
      # Retrieve the weather data using the provided information
      weather_data = get_weather_data(api_key, city, state_code)

      # If the weather data was successfully retrieved
      if weather_data is not None:
        # Construct the filename for the CSV file
        filename = f"{weather_data['City']}_{state_code.strip()}_Weather_Data.csv"
        # Save the weather data to the CSV file
        save_to_csv(filename, weather_data)

        # Display the retrieved weather information to the user
        print(f"\nCity: {weather_data['City']}")
        print(f"Weather: {weather_data['Weather']}")
        print(f"Feels Like: {weather_data['Feels Like']}F")
        print(f"Temperature: {weather_data['Temperature']}F")
        print(f"Humidity: {weather_data['Humidity']}%")
        print(f"Wind Speed: {weather_data['Wind Speed']}mph")
        print(f"Data saved to {filename}")
      else:
        # If the weather data could not be retrieved, print an error message
        print(f"Failed to retrieve weather data for {city}, {state_code}.")

    elif choice == "2":
      # Display the instructions for obtaining an API key
      print("\nInstructions for Obtaining API Key:")
      print(
          "1. Go to the OpenWeatherMap website (https://openweathermap.org/).")
      print("2. Sign up for a free account.")
      print("3. Once logged in, find your API key on the 'API Keys' page.")
      input("Press Enter to return to the main menu...")

    elif choice == "3":
      # Exit the program
      print("\nExiting the program. Goodbye!")
      sys.exit()

    else:
      # If an invalid choice is entered, print an error message
      print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
  # Call the main function to start the program
  main()