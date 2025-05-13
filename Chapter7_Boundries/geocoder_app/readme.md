# Geocoder Console App

This is a simple Python console application that uses the [Maps.co Geocoding API](https://geocode.maps.co/) to fetch the latitude and longitude of any place name entered by the user.

## Setup Instructions

### Getting the Code

```bash
git checkout assignment7-geocode_api
cd Chapter7_Boundries/geocoder_app
```

### Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

3. Create a `.env` file in the root directory with the following contents:
   ```
   API_KEY=your_api_key_here (you can get by logging in geocode website)
   BASE_URL=https://geocode.maps.co/search
   ```
   Replace `your_api_key_here` with your actual API key.

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Run the app with:
```bash
python run.py
```

## Example Usage

```bash
Enter place name: SilkBoard

Result:
Latitude: 12.9174705
Longitude: 77.62379964367692
```