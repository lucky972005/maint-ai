# MaintAI - Setup Guide

## Prerequisites

1. **Supabase Account** - Create a free account at https://supabase.com
2. **OpenAI API Key** - Get an API key from https://platform.openai.com/account/api-keys
3. **Node.js 18+** - Ensure Node.js is installed

## Database Setup

### 1. Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Choose a name (e.g., "maintai")
4. Choose a region close to you
5. Set a strong password
6. Wait for project to be created (2-3 minutes)

### 2. Run Database Migrations

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy the contents of `supabase/migrations/0001_init.sql`
4. Paste and run the SQL script
5. This creates all required tables and RLS policies

### 3. Seed Database

1. In the SQL Editor, run `supabase/seed.sql`
2. This will create demo factories, machines, parts, and procedures
3. Note: You'll need to create auth users first (see below)

### 4. Create Auth Users

In Supabase dashboard:
1. Go to Authentication → Users
2. Click "Add user" → "Create new user"
3. Create these users with password `demo123456`:
   - admin@demo.com (Admin role)
   - supervisor@demo.com (Supervisor role)
   - tech1@demo.com (Technician role)
   - tech2@demo.com (Technician role)
   - tech3@demo.com (Technician role)

4. After creating users, run the seed script again to link profiles

### 5. Get Environment Variables

From your Supabase project dashboard:
1. Go to Settings → API
2. Copy:
   - Project URL (NEXT_PUBLIC_SUPABASE_URL)
   - anon public key (NEXT_PUBLIC_SUPABASE_ANON_KEY)

## Environment Configuration

Create or update `.env.local` in your project root:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# OpenAI Configuration (optional - for AI features)
OPENAI_API_KEY=your-openai-api-key
AI_PROVIDER=openai
OPENAI_MODEL=gpt-4o

# Alternative: Google Gemini (optional)
# GEMINI_API_KEY=your-gemini-api-key
# AI_PROVIDER=gemini
```

## Install Dependencies

```bash
npm install
```

## Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

## Authentication Flow

1. Navigate to `/login` or `/signup`
2. Use demo credentials:
   - Email: admin@demo.com
   - Password: demo123456
3. After login, you'll be redirected to dashboard

## Features

- **Dashboard**: Overview of machines, maintenance status, and alerts
- **Machine Scanner**: QR code scanning to identify machines
- **AI Identification**: Camera-based machine identification
- **Repair Procedures**: Step-by-step maintenance guides
- **Parts Inventory**: Track spare parts and stock levels
- **Fault Reports**: Report and track machine issues
- **Maintenance Logs**: History of all maintenance work
- **Manuals**: Access machine documentation

## Troubleshooting

### Camera not working on mobile
- Use HTTPS (required for camera access)
- For local development, use ngrok: `ngrok http 3000`

### Database connection errors
- Verify environment variables are set correctly
- Check Supabase project is active
- Ensure RLS policies allow access

### AI features not working
- Verify OpenAI API key is valid
- Check API key has credits available
- Ensure AI_PROVIDER is set correctly

## Production Deployment

1. Set up production Supabase project
2. Update environment variables
3. Build the application: `npm run build`
4. Deploy to Vercel, Netlify, or similar platform
5. Update Supabase CORS settings to allow your domain

## Security Notes

- Never commit `.env.local` to version control
- Use Supabase Row Level Security (RLS) policies
- Rotate API keys regularly
- Enable 2FA on Supabase account
