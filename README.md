Project structure:
```
│
├─ backend/           
│   ├─ scraper.py
│   ├─ sentiment.py
│   └─ functions_aux.py
│
├─ frontend/         
│   └─ ui_main.py
│
├─ main.py            
├─ requirements.txt   
├─ .env               
├─ .gitignore
└─ LICENSE
```


## How to Obtain Reddit API Keys

To use this application, you need your own Reddit API keys. Follow these steps:

1. **Go to Reddit's App Preferences:**
   - Open your browser and navigate to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).

2. **Create a New Application:**
   - Scroll down to the **“Developed Applications”** section.
   - Click on **“Create Another App”**.

3. **Fill in Application Details:**
   - **Name:** Give your app a name (anything you like, e.g., `ScrapingSentimentApp`).
   - **App type:** Select **“script”**.
   - **Description:** (Optional) Add a short description.
   - **About URL:** Leave blank or add a link (optional).
   - **Redirect URI:** Enter `http://localhost:8080` (this is required, even if not used).

4. **Save the Application:**
   - Click **“Create app”**.
   - Your new application will appear in the list with the following credentials:
     - **client_id** → the string below the app name.
     - **client_secret** → the string labeled **“secret”**.
     - **user_agent** → a descriptive string for your app (e.g., `ScrapingSentiment/0.1 by YourRedditUsername`).

5. **Add Keys to `.env` File:**
   - In the root of project, create a file named `.env` if it does not exist.
   - Add your keys like this:

```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=your_user_agent_here
```


DEMO: The user enters a topic or keyword, and the app performs sentiment analysis on Reddit comments to return a general appreciation percentage for that topic. The model used is VADER

![App Demo](assets/demo.gif)


## Upcoming Features

- Search filters.  
- Improved search functionality.  
- Option to choose a different sentiment analysis model. 
