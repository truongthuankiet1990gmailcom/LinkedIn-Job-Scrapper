# 🔐 Security Setup Instructions

## API Token Configuration

To use the data refresh functionality, you need to configure your Apify API token securely.

### Step 1: Get Your Apify API Token

1. Visit [Apify Console](https://console.apify.com/account/integrations)
2. Sign up or log in to your account
3. Navigate to **Integrations** → **API tokens**
4. Copy your API token

### Step 2: Local Development Setup

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file:**
   ```bash
   # Open .env file and replace with your actual token
   APIFY_API_TOKEN=your_actual_api_token_here
   ```

### Step 3: Streamlit Cloud Deployment

When deploying to Streamlit Cloud:

1. Go to your app settings in Streamlit Cloud
2. Navigate to **Secrets**
3. Add your environment variables:
   ```toml
   APIFY_API_TOKEN = "your_actual_api_token_here"
   ```

### Step 4: Other Deployment Platforms

#### Railway
1. Go to your project settings
2. Add environment variable: `APIFY_API_TOKEN`

#### Render
1. Go to Environment tab
2. Add environment variable: `APIFY_API_TOKEN`

#### Heroku
```bash
heroku config:set APIFY_API_TOKEN=your_actual_api_token_here
```

#### Docker
```bash
docker run -e APIFY_API_TOKEN=your_token your-image
```

## Security Best Practices

✅ **DO:**
- Use environment variables for API tokens
- Keep your .env file in .gitignore
- Use different tokens for development and production
- Regularly rotate your API tokens

❌ **DON'T:**
- Hardcode API tokens in source code
- Commit .env files to version control
- Share API tokens in public channels
- Use production tokens for development

## Troubleshooting

### Token Not Found Error
If you see "APIFY_API_TOKEN environment variable not found!", ensure:
1. Your .env file exists and contains the token
2. The token name is spelled correctly
3. There are no extra spaces or quotes
4. You've restarted your application after adding the token

### Invalid Token Error
If the API returns authentication errors:
1. Verify your token in Apify Console
2. Check if your account has sufficient credits
3. Ensure the token has the necessary permissions